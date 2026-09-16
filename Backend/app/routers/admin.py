from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, BackgroundTasks, status
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import get_db
from app.models import User, UserRole, Project, Submission, SubmissionStatus, AuditRecord
from app.schemas import AdminStatsOut, UserOut, SubmissionOut, AdminUserUpdate, ProjectListResponse, ProjectOut
from app.dependencies import require_role
from app.services.csv_import import import_csv_to_db

router = APIRouter(prefix="/api/admin", tags=["Admin Panel"])

@router.get("/stats", response_model=AdminStatsOut)
def get_admin_stats(
    current_user: User = Depends(require_role(UserRole.ADMIN)),
    db: Session = Depends(get_db)
):
    """
    Get system-wide platform statistics for admin dashboard.
    """
    total_projects = db.query(func.count(Project.id)).scalar() or 0
    total_users = db.query(func.count(User.id)).filter(User.role == UserRole.USER).scalar() or 0
    total_auditors = db.query(func.count(User.id)).filter(User.role == UserRole.AUDITOR).scalar() or 0
    pending_reviews = db.query(func.count(Submission.id)).filter(Submission.status == SubmissionStatus.PENDING).scalar() or 0
    approved_reviews = db.query(func.count(Submission.id)).filter(Submission.status == SubmissionStatus.APPROVED).scalar() or 0
    rejected_reviews = db.query(func.count(Submission.id)).filter(Submission.status == SubmissionStatus.REJECTED).scalar() or 0
    total_xp = db.query(func.sum(User.xp)).scalar() or 0

    return AdminStatsOut(
        total_projects=total_projects,
        total_users=total_users,
        total_auditors=total_auditors,
        pending_reviews=pending_reviews,
        approved_reviews=approved_reviews,
        rejected_reviews=rejected_reviews,
        total_xp_awarded=total_xp
    )

@router.get("/users", response_model=List[UserOut])
def list_users(
    role: Optional[str] = Query(None, description="Filter by role (USER, AUDITOR, ADMIN)"),
    current_user: User = Depends(require_role(UserRole.ADMIN)),
    db: Session = Depends(get_db)
):
    """
    List all platform users with role filtering.
    """
    query = db.query(User)
    if role:
        query = query.filter(User.role == role)
    return [UserOut.model_validate(u) for u in query.order_by(User.id.asc()).all()]

@router.patch("/users/{user_id}", response_model=UserOut)
def update_user_role(
    user_id: int,
    data: AdminUserUpdate,
    current_user: User = Depends(require_role(UserRole.ADMIN)),
    db: Session = Depends(get_db)
):
    """
    Promote/demote user roles (e.g. appoint new AUDITOR).
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")

    if data.role:
        user.role = data.role
    db.commit()
    db.refresh(user)
    return UserOut.model_validate(user)

@router.get("/submissions", response_model=List[SubmissionOut])
def list_all_submissions(
    status_filter: Optional[str] = Query(None),
    limit: int = Query(50, ge=1, le=200),
    current_user: User = Depends(require_role(UserRole.ADMIN)),
    db: Session = Depends(get_db)
):
    """
    View all submissions across the platform.
    """
    query = db.query(Submission)
    if status_filter and status_filter != "all":
        query = query.filter(Submission.status == status_filter.upper())
    submissions = query.order_by(Submission.submitted_at.desc()).limit(limit).all()
    return [SubmissionOut.model_validate(s) for s in submissions]

@router.post("/import-csv")
def trigger_csv_import(
    background_tasks: BackgroundTasks,
    limit: Optional[int] = Query(None, description="Optional record limit for testing"),
    current_user: User = Depends(require_role(UserRole.ADMIN)),
    db: Session = Depends(get_db)
):
    """
    Trigger batch import of works_completed.csv dataset.
    """
    # Run synchronously if limit is small (<= 500) for instant feedback, or in background
    if limit and limit <= 500:
        result = import_csv_to_db(db, limit=limit)
        return {"status": "completed", "result": result}

    background_tasks.add_task(import_csv_to_db, db, limit=limit)
    return {
        "status": "queued",
        "message": f"CSV import job started in background (limit={limit or 'all'})."
    }
