from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import or_, func

from app.database import get_db
from app.models import Project
from app.schemas import ProjectOut, ProjectListResponse

router = APIRouter(prefix="/api/projects", tags=["Government Works"])

@router.get("/summary-stats")
def get_summary_stats(db: Session = Depends(get_db)):
    """
    Returns dynamic summary statistics directly from database records.
    """
    total_works = db.query(func.count(Project.id)).scalar() or 0
    total_states = db.query(func.count(func.distinct(Project.state))).filter(Project.state.isnot(None)).scalar() or 0
    total_constituencies = db.query(func.count(func.distinct(Project.constituency))).filter(Project.constituency.isnot(None)).scalar() or 0
    completed_works = db.query(func.count(Project.id)).filter(Project.status == "Completed").scalar() or 0
    ongoing_works = db.query(func.count(Project.id)).filter(Project.status == "Ongoing").scalar() or 0

    return {
        "total_works": total_works,
        "total_states": total_states,
        "total_constituencies": total_constituencies,
        "completed_works": completed_works,
        "ongoing_works": ongoing_works
    }

@router.get("/nearby")
def get_nearby_projects(
    lat: float = Query(..., description="User latitude"),
    lng: float = Query(..., description="User longitude"),
    radius_km: float = Query(25.0, ge=1.0, le=200.0),
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db)
):
    """
    Returns works within radius_km using spatial bounding box + Haversine calculation.
    """
    import math
    delta_lat = radius_km / 111.0
    delta_lng = radius_km / (111.0 * max(0.01, math.cos(math.radians(lat))))

    candidates = (
        db.query(
            Project.id,
            Project.work,
            Project.work_category,
            Project.state,
            Project.constituency,
            Project.mp_name,
            Project.status,
            Project.amount_disbursed,
            Project.latitude,
            Project.longitude,
            Project.location_source,
            Project.location_accuracy,
            Project.completion_date,
            Project.work_description
        )
        .filter(
            Project.latitude.between(lat - delta_lat, lat + delta_lat),
            Project.longitude.between(lng - delta_lng, lng + delta_lng)
        )
        .all()
    )

    def haversine(lat1, lon1, lat2, lon2):
        R = 6371.0
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
        return R * 2 * math.asin(math.sqrt(a))

    results = []
    for c in candidates:
        d = haversine(lat, lng, float(c.latitude), float(c.longitude))
        if d <= radius_km:
            results.append({
                "id": c.id,
                "work": c.work,
                "work_category": c.work_category,
                "state": c.state,
                "constituency": c.constituency,
                "mp_name": c.mp_name,
                "status": c.status,
                "amount_disbursed": float(c.amount_disbursed) if c.amount_disbursed else None,
                "latitude": float(c.latitude),
                "longitude": float(c.longitude),
                "location_source": c.location_source,
                "location_accuracy": c.location_accuracy,
                "completion_date": c.completion_date,
                "work_description": c.work_description,
                "distance_km": round(d, 2)
            })

    results.sort(key=lambda x: x["distance_km"])
    return results[:limit]

@router.get("", response_model=ProjectListResponse)
def list_projects(
    state: Optional[str] = Query(None, description="Filter by state"),
    constituency: Optional[str] = Query(None, description="Filter by constituency"),
    category: Optional[str] = Query(None, description="Filter by work category"),
    status: Optional[str] = Query(None, description="Filter by status (Ongoing, Completed)"),
    search: Optional[str] = Query(None, description="Search query across work name, description, MP"),
    has_coords: Optional[bool] = Query(None, description="Filter only projects with coordinates"),
    page: int = Query(1, ge=1),
    limit: int = Query(50, ge=1, le=500),
    db: Session = Depends(get_db)
):
    """
    List government works (MPLADS records) with search and filters.
    """
    query = db.query(Project)

    if state and state.strip() and state != "All":
        query = query.filter(Project.state.ilike(f"%{state.strip()}%"))
    if constituency and constituency.strip() and constituency != "All":
        query = query.filter(Project.constituency.ilike(f"%{constituency.strip()}%"))
    if category and category.strip() and category != "All categories":
        query = query.filter(Project.work_category.ilike(f"%{category.strip()}%"))
    if status and status.strip() and status != "All works":
        query = query.filter(Project.status.ilike(status.strip()))
    if has_coords is True:
        query = query.filter(Project.latitude.isnot(None), Project.longitude.isnot(None))
    elif has_coords is False:
        query = query.filter(or_(Project.latitude.is_(None), Project.longitude.is_(None)))

    if search and search.strip():
        term = f"%{search.strip()}%"
        query = query.filter(
            or_(
                Project.work.ilike(term),
                Project.work_description.ilike(term),
                Project.constituency.ilike(term),
                Project.mp_name.ilike(term)
            )
        )

    total = query.count()
    projects = query.offset((page - 1) * limit).limit(limit).all()

    return ProjectListResponse(
        total=total,
        page=page,
        limit=limit,
        projects=[ProjectOut.model_validate(p) for p in projects]
    )

@router.get("/states")
def get_available_states(db: Session = Depends(get_db)):
    """
    Returns list of all states with recorded works counts.
    """
    results = (
        db.query(Project.state, func.count(Project.id).label("count"))
        .filter(Project.state.isnot(None))
        .group_by(Project.state)
        .order_by(func.count(Project.id).desc())
        .all()
    )
    return [{"state": r[0], "count": r[1]} for r in results if r[0]]

@router.get("/map-hubs")
def get_map_hubs(db: Session = Depends(get_db)):
    """
    Returns aggregated constituency hubs for the entire nation (all 504 constituencies).
    Lightweight payload (~45KB) representing all 35,292 completed works.
    """
    from sqlalchemy import func
    hubs = (
        db.query(
            Project.constituency,
            Project.state,
            Project.mp_name,
            func.count(Project.id).label("work_count"),
            func.sum(Project.amount_disbursed).label("total_disbursed"),
            func.avg(Project.latitude).label("lat"),
            func.avg(Project.longitude).label("lng")
        )
        .filter(Project.latitude.isnot(None), Project.longitude.isnot(None))
        .group_by(Project.constituency, Project.state, Project.mp_name)
        .all()
    )
    return [
        {
            "constituency": h.constituency,
            "state": h.state,
            "mp_name": h.mp_name,
            "work_count": h.work_count,
            "total_disbursed": float(h.total_disbursed) if h.total_disbursed else 0.0,
            "lat": float(h.lat),
            "lng": float(h.lng)
        }
        for h in hubs if h.lat and h.lng
    ]

@router.get("/map-works")
def get_map_works(
    state: Optional[str] = Query(None),
    constituency: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    limit: int = Query(36000, ge=1, le=50000),
    db: Session = Depends(get_db)
):
    """
    Lightweight endpoint returning coordinates and metadata for map rendering.
    """
    query = db.query(
        Project.id,
        Project.work,
        Project.work_category,
        Project.state,
        Project.constituency,
        Project.mp_name,
        Project.status,
        Project.amount_disbursed,
        Project.latitude,
        Project.longitude,
        Project.location_source,
        Project.location_accuracy,
        Project.completion_date,
        Project.work_description
    ).filter(Project.latitude.isnot(None), Project.longitude.isnot(None))

    if state and state.strip() and state != "All states":
        query = query.filter(Project.state.ilike(f"%{state.strip()}%"))
    if constituency and constituency.strip() and constituency != "All":
        query = query.filter(Project.constituency.ilike(f"%{constituency.strip()}%"))
    if category and category.strip() and category != "All categories":
        query = query.filter(Project.work_category.ilike(f"%{category.strip()}%"))
    if search and search.strip():
        term = f"%{search.strip()}%"
        query = query.filter(
            or_(
                Project.work.ilike(term),
                Project.work_description.ilike(term),
                Project.constituency.ilike(term),
                Project.mp_name.ilike(term)
            )
        )

    results = query.limit(limit).all()
    return [
        {
            "id": r.id,
            "work": r.work,
            "work_category": r.work_category,
            "state": r.state,
            "constituency": r.constituency,
            "mp_name": r.mp_name,
            "status": r.status,
            "amount_disbursed": float(r.amount_disbursed) if r.amount_disbursed else None,
            "latitude": float(r.latitude),
            "longitude": float(r.longitude),
            "location_source": r.location_source,
            "location_accuracy": r.location_accuracy,
            "completion_date": r.completion_date,
            "work_description": r.work_description
        }
        for r in results
    ]

@router.get("/geojson")
def get_projects_geojson(
    state: Optional[str] = Query(None),
    limit: int = Query(500, ge=1, le=2000),
    db: Session = Depends(get_db)
):
    """
    Generates standard GeoJSON FeatureCollection of project points using GeoPandas.
    """
    import json
    import geopandas as gpd
    from shapely.geometry import Point

    query = db.query(Project).filter(Project.latitude.isnot(None), Project.longitude.isnot(None))
    if state and state.strip() and state != "All states":
        query = query.filter(Project.state.ilike(f"%{state.strip()}%"))
    
    projects = query.limit(limit).all()
    if not projects:
        return {"type": "FeatureCollection", "features": []}

    records = [
        {
            "id": p.id,
            "work": p.work,
            "category": p.work_category,
            "state": p.state,
            "constituency": p.constituency,
            "status": p.status,
            "amount_disbursed": p.amount_disbursed,
            "location_source": p.location_source,
            "location_accuracy": p.location_accuracy,
            "geometry": Point(p.longitude, p.latitude)
        }
        for p in projects
    ]
    gdf = gpd.GeoDataFrame(records, crs="EPSG:4326")
    return json.loads(gdf.to_json())

@router.get("/{project_id}", response_model=ProjectOut)
def get_project(project_id: str, db: Session = Depends(get_db)):
    """
    Retrieve single government work details.
    """
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Government work record not found."
        )
    return ProjectOut.model_validate(project)
