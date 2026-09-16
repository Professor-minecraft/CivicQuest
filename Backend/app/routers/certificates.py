from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User, Certificate, Submission, SubmissionStatus
from app.schemas import CertificateOut
from app.dependencies import get_current_user
from app.services.certificates import generate_certificate_pdf
from app.config import settings

router = APIRouter(prefix="/api/certificates", tags=["Certificates"])

@router.get("", response_model=List[CertificateOut])
def get_user_certificates(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get all unlocked participation certificates for the logged-in user.
    """
    certs = db.query(Certificate).filter(Certificate.user_id == current_user.id).all()
    return [CertificateOut.model_validate(c) for c in certs]

@router.get("/{certificate_id}/download")
def download_certificate_pdf(
    certificate_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Download the CivicQuest participation certificate as a generated PDF.
    Verifies ownership or auditor/admin permission.
    """
    cert = db.query(Certificate).filter(Certificate.id == certificate_id).first()
    if not cert:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Certificate not found."
        )

    if cert.user_id != current_user.id and current_user.role not in ["AUDITOR", "ADMIN"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to download this certificate."
        )

    pdf_buffer = generate_certificate_pdf(
        citizen_name=cert.citizen_name,
        achievement=cert.achievement,
        verifications_count=cert.approved_verifications_count,
        issue_date=cert.issue_date,
        certificate_code=cert.certificate_code
    )

    filename = f"CivicQuest_Certificate_{cert.certificate_code}.pdf"
    return StreamingResponse(
        pdf_buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'}
    )
