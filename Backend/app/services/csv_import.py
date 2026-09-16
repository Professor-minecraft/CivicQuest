import logging
import math
from pathlib import Path
from typing import Optional, Dict, Any, Generator, Tuple, List
import pandas as pd
from sqlalchemy.orm import Session

from app.models import Project, LocationCache
from app.config import settings
from app.services.geocoding import geocoding_service

logger = logging.getLogger("civicquest.csv_import")

# Hierarchy of location sources (higher value = higher priority)
LOCATION_PRIORITY: Dict[str, int] = {
    "EXACT_DATASET": 4,
    "TRUSTED_SOURCE": 3,
    "GEOCODED": 2,
    "APPROXIMATE": 1,
    "MISSING": 0,
}

# Predefined reference coordinates for Indian districts/constituencies.
# Explicitly tagged as APPROXIMATE and CONSTITUENCY_CENTROID.
# Never claimed as exact work-site coordinates.
APPROXIMATE_COORDINATES: Dict[str, Tuple[float, float]] = {
    "ARARIA": (26.1511, 87.4984),
    "FARIDKOT": (30.6769, 74.7583),
    "FARIDKOT(SC)": (30.6769, 74.7583),
    "KOLLAM": (8.8932, 76.6141),
    "BANGALORE": (12.9716, 77.5946),
    "BENGALURU": (12.9716, 77.5946),
    "BANGALORE CENTRAL": (12.9702, 77.6106),
    "BANGALORE SOUTH": (12.9352, 77.5684),
    "BANGALORE NORTH": (13.0358, 77.5970),
    "BANGALORE RURAL": (13.1986, 77.7066),
    "NEW DELHI": (28.6139, 77.2090),
    "MUMBAI": (19.0760, 72.8777),
    "MUMBAI SOUTH": (18.9388, 72.8354),
    "MUMBAI NORTH": (19.2183, 72.8597),
    "CHENNAI": (13.0827, 80.2707),
    "CHENNAI CENTRAL": (13.0827, 80.2707),
    "HYDERABAD": (17.3850, 78.4867),
    "KOLKATA": (22.5726, 88.3639),
    "KOLKATA SOUTH": (22.5186, 88.3426),
    "KOLKATA NORTH": (22.5958, 88.3726),
    "PUNE": (18.5204, 73.8567),
    "PATNA": (25.5941, 85.1376),
    "LUCKNOW": (26.8467, 80.9462),
    "JAIPUR": (26.9124, 75.7873),
    "AHMEDABAD": (23.0225, 72.5714),
    "CHANDIGARH": (30.7333, 76.7794),
    "AMRITSAR": (31.6340, 74.8723),
    "VARANASI": (25.3176, 82.9739),
    "BHOPAL": (23.2599, 77.4126),
    "INDORE": (22.7196, 75.8577),
    "NAGPUR": (21.1458, 79.0882),
    "KANPUR": (26.4499, 80.3319),
    "THIRUVANANTHAPURAM": (8.5241, 76.9366),
    "COIMBATORE": (11.0168, 76.9558),
    "MADURAI": (9.9252, 78.1198),
    "VIJAYAWADA": (16.5062, 80.6480),
    "VISAKHAPATNAM": (17.6868, 83.2185),
    "GUWAHATI": (26.1445, 91.7362),
    "RANCHI": (23.3441, 85.3096),
    "BHUBANESWAR": (20.2961, 85.8245),
    "DEHRADUN": (30.3165, 78.0322),
    "SHIMLA": (31.1048, 77.1734),
}

def clean_amount(val: Any) -> Optional[float]:
    if val is None or (isinstance(val, float) and math.isnan(val)):
        return None
    cleaned = str(val).replace(",", "").replace("₹", "").replace("?", "").strip()
    try:
        return float(cleaned)
    except ValueError:
        return None

def clean_string(val: Any) -> Optional[str]:
    if val is None or (isinstance(val, float) and math.isnan(val)):
        return None
    s = str(val).strip()
    if s.lower() in ("", "n/a", "null", "none", "nan"):
        return None
    return s

def clean_coordinate(val: Any) -> Optional[float]:
    if val is None or (isinstance(val, float) and math.isnan(val)):
        return None
    try:
        f = float(val)
        return f if not math.isnan(f) else None
    except (ValueError, TypeError):
        return None

# Load comprehensive 543 Parliamentary Constituency Centroids dataset
CENTROIDS_FILE = settings.BASE_DIR / "data" / "constituency_centroids.json" if hasattr(settings, "BASE_DIR") else Path(__file__).resolve().parent.parent.parent / "data" / "constituency_centroids.json"
PC_CENTROIDS: Dict[str, Tuple[float, float]] = {}
if CENTROIDS_FILE.exists():
    try:
        import json
        with open(CENTROIDS_FILE, "r", encoding="utf-8") as f:
            _raw = json.load(f)
            for k, v in _raw.items():
                PC_CENTROIDS[k.strip().upper()] = (v["lat"], v["lng"])
    except Exception as e:
        logger.warning(f"Error loading constituency centroids file: {e}")

def resolve_project_coordinates(
    constituency: Optional[str],
    state: Optional[str],
    ida: Optional[str],
    row_lat: Optional[float] = None,
    row_lng: Optional[float] = None,
    db: Optional[Session] = None
) -> Tuple[Optional[float], Optional[float], str, Optional[str]]:
    """
    Determine coordinates according to the strict priority hierarchy:
    1. EXACT_DATASET: exact coordinates directly supplied in dataset
    2. GEOCODED: cached geocoded location
    3. APPROXIMATE: constituency / district centroid reference
    4. MISSING: no fabricated coordinates
    Returns: (lat, lng, location_source, location_accuracy)
    """
    import re

    # 1. Dataset supplied exact coordinates
    if row_lat is not None and row_lng is not None:
        if -90 <= row_lat <= 90 and -180 <= row_lng <= 180 and (row_lat != 0 or row_lng != 0):
            return row_lat, row_lng, "EXACT_DATASET", "EXACT"

    # 2. Check full Parliamentary Constituency centroids (covers all Indian constituencies)
    if constituency:
        norm = constituency.strip().upper()
        if norm in PC_CENTROIDS:
            lat, lng = PC_CENTROIDS[norm]
            return lat, lng, "APPROXIMATE", "CONSTITUENCY_CENTROID"
        clean_norm = re.sub(r'\s*\((?:SC|ST)\)\s*', '', norm).strip()
        if clean_norm in PC_CENTROIDS:
            lat, lng = PC_CENTROIDS[clean_norm]
            return lat, lng, "APPROXIMATE", "CONSTITUENCY_CENTROID"

    # 3. Check cached coordinates in PostgreSQL LocationCache
    cache_key = f"{constituency or ''}|{state or ''}".strip().lower()
    if cache_key and cache_key != "|":
        cached = geocoding_service.get_cached_coordinates(cache_key, db=db)
        if cached and cached[0] is not None and cached[1] is not None:
            return cached[0], cached[1], cached[2], cached[3]

    # 4. Reference dictionary for Indian districts/cities
    if constituency:
        norm = constituency.strip().upper()
        if norm in APPROXIMATE_COORDINATES:
            lat, lng = APPROXIMATE_COORDINATES[norm]
            return lat, lng, "APPROXIMATE", "CONSTITUENCY_CENTROID"
        for k, coords in APPROXIMATE_COORDINATES.items():
            if k in norm:
                return coords[0], coords[1], "APPROXIMATE", "CONSTITUENCY_CENTROID"

    if ida:
        norm_ida = ida.strip().upper()
        for k, coords in APPROXIMATE_COORDINATES.items():
            if k in norm_ida:
                return coords[0], coords[1], "APPROXIMATE", "DISTRICT_CENTROID"

    # 5. Never fabricate coordinates
    return None, None, "MISSING", "MISSING"

def parse_csv_stream_pandas(
    csv_path: Path,
    chunksize: int = 1000,
    db: Optional[Session] = None
) -> Generator[Dict[str, Any], None, None]:
    """
    Reads and parses the completed works CSV in chunks using pandas.
    Handles optional latitude/longitude columns for future datasets.
    """
    for chunk in pd.read_csv(csv_path, chunksize=chunksize, encoding="utf-8-sig", low_memory=False):
        # Normalize column names for flexible detection
        col_map = {c.strip(): c for c in chunk.columns}
        
        # Check for optional exact coordinate columns
        lat_col = next((col_map[c] for c in col_map if c.lower() in ("latitude", "lat")), None)
        lng_col = next((col_map[c] for c in col_map if c.lower() in ("longitude", "long", "lng")), None)
        
        # Check for amount column
        amt_col = next((col_map[c] for c in col_map if "amount disbursed" in c.lower()), None)
        
        # Category column
        cat_col = next((col_map[c] for c in col_map if "work category" in c.lower()), None)
        
        # Work name column
        work_col = next((col_map[c] for c in col_map if c.strip().lower() == "work"), None)
        
        # MP name column
        mp_col = next((col_map[c] for c in col_map if "parliament" in c.lower() or "mp" in c.lower()), None)

        for _, row in chunk.iterrows():
            sr_no_raw = row.get("Sr. No.")
            try:
                sr_no = int(sr_no_raw) if pd.notna(sr_no_raw) and str(sr_no_raw).isdigit() else None
            except Exception:
                sr_no = None

            work_name = clean_string(row.get(work_col) if work_col else row.get("Work"))
            category = clean_string(row.get(cat_col) if cat_col else row.get("Work Category"))
            state = clean_string(row.get("State"))
            ida = clean_string(row.get("IDA"))
            description = clean_string(row.get("Work Description"))
            mp_name = clean_string(row.get(mp_col) if mp_col else row.get("Hon'ble Members of Parliament"))
            constituency = clean_string(row.get("Constituency"))
            image = clean_string(row.get("Image"))
            completion_date = clean_string(row.get("Completion Date"))
            
            amount_raw = row.get(amt_col) if amt_col else None
            amount = clean_amount(amount_raw)

            row_lat = clean_coordinate(row.get(lat_col)) if lat_col else None
            row_lng = clean_coordinate(row.get(lng_col)) if lng_col else None

            project_id = f"MPLADS-{sr_no}" if sr_no is not None else f"MPLADS-ROW-{abs(hash(work_name or '')) % 10000000}"

            lat, lng, location_source, location_accuracy = resolve_project_coordinates(
                constituency=constituency,
                state=state,
                ida=ida,
                row_lat=row_lat,
                row_lng=row_lng,
                db=db
            )

            yield {
                "id": project_id,
                "sr_no": sr_no,
                "work_category": category or "Infrastructure",
                "work": work_name or "Government Development Work",
                "state": state,
                "ida": ida,
                "work_description": description,
                "mp_name": mp_name,
                "constituency": constituency,
                "image": image,
                "completion_date": completion_date,
                "amount_disbursed": amount,
                "latitude": lat,
                "longitude": lng,
                "location_source": location_source,
                "location_accuracy": location_accuracy,
                "status": "Completed"
            }

def import_csv_to_db(
    db: Session,
    csv_path: Optional[Path] = None,
    limit: Optional[int] = None,
    batch_size: int = 500
) -> Dict[str, Any]:
    """
    Import works from CSV into database with pandas, batching, and priority protection.
    Never overwrites a trusted coordinate with an inferior approximate coordinate.
    """
    target_path = csv_path or settings.resolved_csv_path
    if not target_path.exists():
        # Check alternative common filename
        alt = target_path.parent / "Works Completed.csv"
        if alt.exists():
            target_path = alt
        else:
            raise FileNotFoundError(f"CSV file not found at {target_path}")

    total_read = 0
    total_inserted = 0
    total_updated = 0
    batch: List[Dict[str, Any]] = []

    logger.info(f"Beginning CSV import from {target_path} (limit={limit})...")

    for item in parse_csv_stream_pandas(target_path, db=db):
        total_read += 1
        batch.append(item)

        if len(batch) >= batch_size:
            inserted, updated = _flush_batch(db, batch)
            total_inserted += inserted
            total_updated += updated
            batch = []
            logger.info(f"Processed {total_read} records ({total_inserted} inserted, {total_updated} updated)...")

        if limit and total_read >= limit:
            break

    if batch:
        inserted, updated = _flush_batch(db, batch)
        total_inserted += inserted
        total_updated += updated

    logger.info(f"CSV import complete. Total: {total_read}, Inserted: {total_inserted}, Updated: {total_updated}")
    return {
        "total_processed": total_read,
        "inserted": total_inserted,
        "updated": total_updated
    }

def _flush_batch(db: Session, batch: List[Dict[str, Any]]) -> Tuple[int, int]:
    inserted = 0
    updated = 0
    ids = [item["id"] for item in batch]
    existing_projects = {p.id: p for p in db.query(Project).filter(Project.id.in_(ids)).all()}

    for data in batch:
        p_id = data["id"]
        if p_id in existing_projects:
            proj = existing_projects[p_id]
            # Protect location hierarchy: never overwrite higher priority location with lower priority
            existing_prio = LOCATION_PRIORITY.get((proj.location_source or "").upper(), 0)
            incoming_prio = LOCATION_PRIORITY.get((data.get("location_source") or "").upper(), 0)

            for k, v in data.items():
                if k in ("latitude", "longitude", "location_source", "location_accuracy"):
                    if incoming_prio >= existing_prio:
                        setattr(proj, k, v)
                else:
                    setattr(proj, k, v)
            updated += 1
        else:
            proj = Project(**data)
            db.add(proj)
            inserted += 1

    db.commit()
    return inserted, updated
