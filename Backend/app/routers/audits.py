from datetime import datetime, timezone
from typing import List, Optional
import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import get_db
from app.models import (
    User, UserRole, Project, Submission, SubmissionStatus,
    AuditRecord, Notification, Certificate
)
from app.schemas import SubmissionOut, AuditDecisionRequest, AuditRecordOut
from app.dependencies import require_role
from app.config import settings

router = APIRouter(prefix="/api/audits", tags=["Auditor Workspace"])

AUDITOR_ROLES = [UserRole.AUDITOR, UserRole.ADMIN]

@router.get("/pending", response_model=List[SubmissionOut])
def get_pending_submissions(
    current_user: User = Depends(require_role(*AUDITOR_ROLES)),
    db: Session = Depends(get_db)
):
    """
    List all pending citizen submissions awaiting auditor review.
    Accessible only by AUDITOR or ADMIN.
    """
    pending = db.query(Submission).filter(
        Submission.status == SubmissionStatus.PENDING
    ).order_by(Submission.submitted_at.asc()).all()
    return [SubmissionOut.model_validate(s) for s in pending]

@router.get("/history", response_model=List[SubmissionOut])
def get_audit_history(
    limit: int = 50,
    current_user: User = Depends(require_role(*AUDITOR_ROLES)),
    db: Session = Depends(get_db)
):
    """
    List reviewed submissions history.
    Accessible only by AUDITOR or ADMIN.
    """
    history = db.query(Submission).filter(
        Submission.status.in_([SubmissionStatus.APPROVED, SubmissionStatus.REJECTED])
    ).order_by(Submission.reviewed_at.desc()).limit(limit).all()
    return [SubmissionOut.model_validate(s) for s in history]

@router.post("/{submission_id}/approve", response_model=SubmissionOut)
def approve_submission(
    submission_id: str,
    data: Optional[AuditDecisionRequest] = None,
    current_user: User = Depends(require_role(*AUDITOR_ROLES)),
    db: Session = Depends(get_db)
):
    """
    Approve citizen verification in a single atomic transaction:
    1. Mark submission APPROVED
    2. Record auditor decision, timestamp, and feedback
    3. Award +150 XP to citizen (guaranteed once per project)
    4. Recalculate level
    5. Check certificate unlock milestone (5 approved verifications)
    6. Generate audit record and user notifications
    """
    submission = db.query(Submission).filter(Submission.id == submission_id).first()
    if not submission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Submission not found."
        )

    if submission.status == SubmissionStatus.APPROVED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This submission has already been approved."
        )

    submitter = db.query(User).filter(User.id == submission.user_id).first()
    if not submitter:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Citizen account associated with submission not found."
        )

    feedback = (data.feedback if data and data.feedback else "").strip()
    now = datetime.now(timezone.utc)

    # 1. Update submission
    submission.status = SubmissionStatus.APPROVED
    submission.reviewed_at = now
    submission.reviewed_by = current_user.id
    submission.review_feedback = feedback or "Evidence verified and approved by community auditor."

    # 2. Record audit log
    audit_log = AuditRecord(
        submission_id=submission.id,
        auditor_id=current_user.id,
        decision="APPROVED",
        feedback=submission.review_feedback
    )
    db.add(audit_log)

    # 3. Prevent duplicate XP awards: check if citizen already received XP for this project
    already_awarded_for_project = db.query(Submission).filter(
        Submission.user_id == submitter.id,
        Submission.project_id == submission.project_id,
        Submission.status == SubmissionStatus.APPROVED,
        Submission.id != submission.id
    ).count() > 0

    xp_awarded = 0
    if not already_awarded_for_project:
        xp_awarded = settings.APPROVAL_XP
        submitter.xp += xp_awarded
        submitter.level = (submitter.xp // settings.LEVEL_XP) + 1

    # 4. Create approval notification
    xp_text = f"+{xp_awarded} XP awarded!" if xp_awarded > 0 else "Verified (project already rewarded)."
    notif = Notification(
        user_id=submitter.id,
        title=f"Verification Approved! {xp_text}",
        message=f"Your review for '{submission.project.work if submission.project else submission.project_id}' was approved by auditor {current_user.name}. {submission.review_feedback}",
        type="SUBMISSION_APPROVED"
    )
    db.add(notif)

    # 5. Check Certificate threshold (5 approved verifications)
    approved_count = db.query(Submission).filter(
        Submission.user_id == submitter.id,
        Submission.status == SubmissionStatus.APPROVED
    ).count() + 1  # Including this one

    if approved_count >= settings.CERTIFICATE_THRESHOLD:
        existing_cert = db.query(Certificate).filter(Certificate.user_id == submitter.id).first()
        if not existing_cert:
            cert_code = f"CIVICQUEST-{submitter.id:04d}-{uuid.uuid4().hex[:6].upper()}"
            cert = Certificate(
                id=f"cert-{uuid.uuid4().hex[:12]}",
                user_id=submitter.id,
                citizen_name=submitter.name,
                achievement="Changemaker — 5 Approved Verifications",
                approved_verifications_count=approved_count,
                certificate_code=cert_code
            )
            db.add(cert)
            cert_notif = Notification(
                user_id=submitter.id,
                title="Participation Certificate Unlocked!",
                message=f"Congratulations! You completed {approved_count} approved verifications and unlocked the CivicQuest Civic Participation Certificate ({cert_code}).",
                type="CERTIFICATE_UNLOCKED"
            )
            db.add(cert_notif)

    db.commit()
    db.refresh(submission)
    return SubmissionOut.model_validate(submission)

@router.post("/{submission_id}/reject", response_model=SubmissionOut)
def reject_submission(
    submission_id: str,
    data: AuditDecisionRequest,
    current_user: User = Depends(require_role(*AUDITOR_ROLES)),
    db: Session = Depends(get_db)
):
    """
    Reject citizen verification with mandatory explanatory feedback.
    No XP awarded. Creates audit record and notification.
    """
    submission = db.query(Submission).filter(Submission.id == submission_id).first()
    if not submission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Submission not found."
        )

    feedback = (data.feedback or "").strip()
    if len(feedback) < 5:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A rejection reason of at least 5 characters is required."
        )

    now = datetime.now(timezone.utc)
    submission.status = SubmissionStatus.REJECTED
    submission.reviewed_at = now
    submission.reviewed_by = current_user.id
    submission.review_feedback = feedback

    audit_log = AuditRecord(
        submission_id=submission.id,
        auditor_id=current_user.id,
        decision="REJECTED",
        feedback=feedback
    )
    db.add(audit_log)

    notif = Notification(
        user_id=submission.user_id,
        title="Evidence review update",
        message=f"Your submission for '{submission.project.work if submission.project else submission.project_id}' was reviewed. Auditor feedback: {feedback}",
        type="SUBMISSION_REJECTED"
    )
    db.add(notif)

    db.commit()
    db.refresh(submission)
    return SubmissionOut.model_validate(submission)
