from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import get_db
from app.models import User, UserRole, Submission, SubmissionStatus
from app.schemas import LeaderboardResponse, LeaderboardUser

router = APIRouter(prefix="/api/leaderboard", tags=["Leaderboard"])

@router.get("", response_model=LeaderboardResponse)
def get_leaderboard(
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """
    Get top ranking citizens ordered by XP from real database records.
    """
    # Count approved submissions per user
    approved_counts = dict(
        db.query(
            Submission.user_id,
            func.count(Submission.id)
        ).filter(
            Submission.status == SubmissionStatus.APPROVED
        ).group_by(Submission.user_id).all()
    )

    # Fetch users ordered by XP descending
    users = db.query(User).filter(
        User.role == UserRole.USER
    ).order_by(User.xp.desc(), User.created_at.asc()).limit(limit).all()

    leaders = [
        LeaderboardUser(
            id=u.id,
            name=u.name,
            xp=u.xp,
            level=u.level,
            role=u.role,
            approved_count=approved_counts.get(u.id, 0)
        )
        for u in users
    ]

    return LeaderboardResponse(leaders=leaders)
