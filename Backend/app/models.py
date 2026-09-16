import uuid
from sqlalchemy import (
    Column, Integer, String, Text, Float, Boolean, DateTime, ForeignKey, Enum
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class UserRole:
    USER = "USER"
    AUDITOR = "AUDITOR"
    ADMIN = "ADMIN"

class SubmissionStatus:
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(150), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(20), default=UserRole.USER, nullable=False, index=True)
    xp = Column(Integer, default=0, nullable=False)
    level = Column(Integer, default=1, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    submissions = relationship("Submission", back_populates="user", foreign_keys="Submission.user_id")
    audits = relationship("AuditRecord", back_populates="auditor", foreign_keys="AuditRecord.auditor_id")
    notifications = relationship("Notification", back_populates="user", cascade="all, delete-orphan")
    certificates = relationship("Certificate", back_populates="user", cascade="all, delete-orphan")

class Project(Base):
    __tablename__ = "projects"

    id = Column(String(50), primary_key=True, index=True)
    sr_no = Column(Integer, nullable=True, index=True)
    work_category = Column(String(255), nullable=True, index=True)
    work = Column(String(500), nullable=True)
    state = Column(String(100), nullable=True, index=True)
    ida = Column(String(255), nullable=True)
    work_description = Column(Text, nullable=True)
    mp_name = Column(String(255), nullable=True)
    constituency = Column(String(150), nullable=True, index=True)
    image = Column(String(500), nullable=True)
    completion_date = Column(String(100), nullable=True)
    amount_disbursed = Column(Float, nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    location_source = Column(String(50), default="MISSING")  # EXACT_DATASET, GEOCODED, APPROXIMATE, MISSING
    location_accuracy = Column(String(50), nullable=True)  # EXACT, APPROXIMATE, CONSTITUENCY_CENTROID, MISSING
    status = Column(String(50), default="Completed")  # Completed, Ongoing
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    submissions = relationship("Submission", back_populates="project", cascade="all, delete-orphan")

class LocationCache(Base):
    __tablename__ = "location_cache"

    id = Column(Integer, primary_key=True, autoincrement=True)
    query_key = Column(String(255), unique=True, index=True, nullable=False)
    project_id = Column(String(50), nullable=True, index=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    location_source = Column(String(50), nullable=False, default="MISSING")
    location_accuracy = Column(String(50), nullable=True)
    geocoded_at = Column(DateTime(timezone=True), server_default=func.now())

class Submission(Base):
    __tablename__ = "submissions"

    id = Column(String(60), primary_key=True, default=lambda: f"sub-{uuid.uuid4().hex[:12]}")
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    project_id = Column(String(50), ForeignKey("projects.id"), nullable=False, index=True)
    photo_url = Column(String(500), nullable=False)
    file_name = Column(String(255), nullable=True)
    observation = Column(String(50), nullable=False)  # Completed, Ongoing, Not done
    notes = Column(Text, nullable=False)
    check_in_type = Column(String(20), default="gps")  # gps, simulated
    gps_latitude = Column(Float, nullable=True)
    gps_longitude = Column(Float, nullable=True)
    gps_accuracy = Column(Float, nullable=True)
    distance_from_project = Column(Float, nullable=True)
    gps_verification_status = Column(String(50), default="UNVERIFIED", nullable=True)  # VERIFIED, LIMITED, NO_COORDINATES, SIMULATED
    status = Column(String(20), default=SubmissionStatus.PENDING, index=True, nullable=False)
    submitted_at = Column(DateTime(timezone=True), server_default=func.now())
    reviewed_at = Column(DateTime(timezone=True), nullable=True)
    reviewed_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    review_feedback = Column(Text, nullable=True)

    user = relationship("User", back_populates="submissions", foreign_keys=[user_id])
    project = relationship("Project", back_populates="submissions")
    reviewer = relationship("User", foreign_keys=[reviewed_by])
    audit_records = relationship("AuditRecord", back_populates="submission", cascade="all, delete-orphan")

class AuditRecord(Base):
    __tablename__ = "audit_records"

    id = Column(Integer, primary_key=True, autoincrement=True)
    submission_id = Column(String(60), ForeignKey("submissions.id"), nullable=False, index=True)
    auditor_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    decision = Column(String(20), nullable=False)  # APPROVED, REJECTED
    feedback = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    submission = relationship("Submission", back_populates="audit_records")
    auditor = relationship("User", back_populates="audits", foreign_keys=[auditor_id])

class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    title = Column(String(200), nullable=False)
    message = Column(Text, nullable=False)
    type = Column(String(50), nullable=False)  # SUBMISSION_RECEIVED, SUBMISSION_APPROVED, etc.
    is_read = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="notifications")

class Certificate(Base):
    __tablename__ = "certificates"

    id = Column(String(60), primary_key=True, default=lambda: f"cert-{uuid.uuid4().hex[:12]}")
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    citizen_name = Column(String(150), nullable=False)
    achievement = Column(String(255), nullable=False)
    approved_verifications_count = Column(Integer, default=5, nullable=False)
    issue_date = Column(DateTime(timezone=True), server_default=func.now())
    certificate_code = Column(String(100), unique=True, index=True, nullable=False)

    user = relationship("User", back_populates="certificates")
