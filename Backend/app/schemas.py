from datetime import datetime
from typing import Optional, List, Any
from pydantic import BaseModel, EmailStr, Field

# --- Auth & User Schemas ---

class UserRegister(BaseModel):
    name: str = Field(..., min_length=2, max_length=150)
    email: str = Field(..., min_length=3, max_length=255)
    password: str = Field(..., min_length=4, max_length=100)

class UserLogin(BaseModel):
    email: str
    password: str

class UserOut(BaseModel):
    id: int
    name: str
    email: str
    role: str
    xp: int
    level: int
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut

# --- Project Schemas ---

class ProjectOut(BaseModel):
    id: str
    sr_no: Optional[int] = None
    work_category: Optional[str] = None
    work: Optional[str] = None
    state: Optional[str] = None
    ida: Optional[str] = None
    work_description: Optional[str] = None
    mp_name: Optional[str] = None
    constituency: Optional[str] = None
    image: Optional[str] = None
    completion_date: Optional[str] = None
    amount_disbursed: Optional[float] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    location_source: Optional[str] = "MISSING"
    location_accuracy: Optional[str] = None
    status: Optional[str] = "Completed"

    class Config:
        from_attributes = True

class ProjectListResponse(BaseModel):
    total: int
    page: int
    limit: int
    projects: List[ProjectOut]

# --- Submission Schemas ---

class SubmissionOut(BaseModel):
    id: str
    user_id: int
    project_id: str
    photo_url: str
    file_name: Optional[str] = None
    observation: str
    notes: str
    check_in_type: str
    gps_latitude: Optional[float] = None
    gps_longitude: Optional[float] = None
    gps_accuracy: Optional[float] = None
    distance_from_project: Optional[float] = None
    gps_verification_status: Optional[str] = None
    status: str
    submitted_at: datetime
    reviewed_at: Optional[datetime] = None
    reviewed_by: Optional[int] = None
    review_feedback: Optional[str] = None
    project: Optional[ProjectOut] = None

    class Config:
        from_attributes = True

# --- Audit Schemas ---

class AuditDecisionRequest(BaseModel):
    decision: str = Field(..., pattern="^(approved|rejected)$")
    feedback: Optional[str] = ""

class AuditRecordOut(BaseModel):
    id: int
    submission_id: str
    auditor_id: int
    decision: str
    feedback: str
    created_at: datetime

    class Config:
        from_attributes = True

# --- Gamification & Leaderboard Schemas ---

class LeaderboardUser(BaseModel):
    id: int
    name: str
    xp: int
    level: int
    role: str
    approved_count: int

class LeaderboardResponse(BaseModel):
    leaders: List[LeaderboardUser]

# --- Notification Schemas ---

class NotificationOut(BaseModel):
    id: int
    title: str
    message: str
    type: str
    is_read: bool
    created_at: datetime

    class Config:
        from_attributes = True

# --- Certificate Schemas ---

class CertificateOut(BaseModel):
    id: str
    citizen_name: str
    achievement: str
    approved_verifications_count: int
    issue_date: datetime
    certificate_code: str

    class Config:
        from_attributes = True

# --- Admin Schemas ---

class AdminStatsOut(BaseModel):
    total_projects: int
    total_users: int
    total_auditors: int
    pending_reviews: int
    approved_reviews: int
    rejected_reviews: int
    total_xp_awarded: int

class AdminUserUpdate(BaseModel):
    role: Optional[str] = Field(None, pattern="^(USER|AUDITOR|ADMIN)$")
