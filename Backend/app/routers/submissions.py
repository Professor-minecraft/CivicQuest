import os
import uuid
from pathlib import Path
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, status
from sqlalchemy.orm import Session
from PIL import Image
import io

from app.database import get_db
from app.models import User, UserRole, Project, Submission, SubmissionStatus, Notification
from app.schemas import SubmissionOut
from app.dependencies import get_current_user
from app.config import settings
from app.services.geocoding import calculate_haversine_distance

router = APIRouter(prefix="/api/submissions", tags=["Citizen Submissions"])

ALLOWED_IMAGE_TYPES = {"image/jpeg", "image/png", "image/webp", "image/jpg"}

@router.post("", response_model=SubmissionOut, status_code=status.HTTP_201_CREATED)
async def submit_verification(
    project_id: str = Form(...),
    observation: str = Form(...),  # Completed, Ongoing, Not done
    notes: str = Form(...),
    check_in_type: str = Form("gps"),  # gps, simulated
    gps_latitude: Optional[float] = Form(None),
    gps_longitude: Optional[float] = Form(None),
    gps_accuracy: Optional[float] = Form(None),
    photo: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Submit a citizen verification for a government work.
    Only logged-in USER can contribute.
    Validates photo with Pillow, computes Haversine distance, and queues as PENDING for auditor.
    """
    # Verify project exists
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Referenced government work does not exist."
        )

    # Check for active non-rejected submission on this project by this user
    existing = db.query(Submission).filter(
        Submission.user_id == current_user.id,
        Submission.project_id == project_id,
        Submission.status.in_([SubmissionStatus.PENDING, SubmissionStatus.APPROVED])
    ).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You already have an active or approved submission for this work."
        )

    # Validate observation value
    if observation not in ["Completed", "Ongoing", "Not done"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Observation must be 'Completed', 'Ongoing', or 'Not done'."
        )

    if len(notes.strip()) < 10:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Field notes must be at least 10 characters long."
        )

    # Validate file type and contents
    content_type = photo.content_type or ""
    if content_type.lower() not in ALLOWED_IMAGE_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid image format. Allowed formats: JPEG, PNG, WebP."
        )

    file_bytes = await photo.read()
    if len(file_bytes) > settings.MAX_FILE_SIZE_BYTES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Image file exceeds maximum limit of {settings.MAX_FILE_SIZE_BYTES // (1024*1024)} MB."
        )

    # Validate actual image structure with Pillow
    try:
        image_stream = io.BytesIO(file_bytes)
        with Image.open(image_stream) as img:
            img.verify()
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Uploaded file is corrupted or not a valid image."
        )

    # Save to disk safely with unique UUID filename
    ext = os.path.splitext(photo.filename or "")[1].lower()
    if ext not in [".jpg", ".jpeg", ".png", ".webp"]:
        ext = ".jpg"

    safe_filename = f"{uuid.uuid4().hex}{ext}"
    dest_path = settings.resolved_upload_dir / safe_filename
    with open(dest_path, "wb") as f:
        f.write(file_bytes)

    photo_url = f"/uploads/{safe_filename}"

    # Calculate distance and evaluate GPS verification quality independently on the server
    distance_from_project = None
    gps_verification_status = "SIMULATED" if check_in_type == "simulated" else "NO_COORDINATES"
    if check_in_type == "gps" and gps_latitude is not None and gps_longitude is not None:
        from app.services.geocoding import evaluate_gps_verification
        gps_verification_status, distance_from_project = evaluate_gps_verification(
            gps_lat=gps_latitude,
            gps_lng=gps_longitude,
            project_lat=project.latitude,
            project_lng=project.longitude,
            location_source=project.location_source,
            max_verified_distance_meters=200.0
        )

    submission_id = f"sub-{uuid.uuid4().hex[:12]}"
    submission = Submission(
        id=submission_id,
        user_id=current_user.id,
        project_id=project.id,
        photo_url=photo_url,
        file_name=photo.filename,
        observation=observation,
        notes=notes.strip(),
        check_in_type=check_in_type,
        gps_latitude=gps_latitude,
        gps_longitude=gps_longitude,
        gps_accuracy=gps_accuracy,
        distance_from_project=distance_from_project,
        gps_verification_status=gps_verification_status,
        status=SubmissionStatus.PENDING
    )
    db.add(submission)

    # Create persistent notification for citizen
    notif = Notification(
        user_id=current_user.id,
        title="Evidence submitted for review",
        message=f"Your verification for '{project.work[:60]}' has been queued. An auditor will review your submission shortly.",
        type="SUBMISSION_RECEIVED"
    )
    db.add(notif)
    db.commit()
    db.refresh(submission)

    return SubmissionOut.model_validate(submission)

@router.get("/my", response_model=List[SubmissionOut])
def get_my_submissions(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get all verification quests submitted by the logged-in citizen.
    """
    submissions = db.query(Submission).filter(
        Submission.user_id == current_user.id
    ).order_by(Submission.submitted_at.desc()).all()
    return [SubmissionOut.model_validate(s) for s in submissions]
