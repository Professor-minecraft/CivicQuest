import sys
import io
from pathlib import Path
from PIL import Image

backend_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(backend_dir))

from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal
from app.models import User, Submission, Project

client = TestClient(app)

def run_tests():
    print("=== Running CivicQuest Backend API Tests ===")

    # 1. Root
    res = client.get("/")
    assert res.status_code == 200, f"Root failed: {res.text}"
    print("[PASS] 1. Root health check")

    # 2. Admin login
    res = client.post("/api/auth/login", json={"email": "admin@gg", "password": "admin"})
    assert res.status_code == 200, f"Admin login failed: {res.text}"
    admin_data = res.json()
    admin_token = admin_data["access_token"]
    assert admin_data["user"]["role"] == "ADMIN"
    print("[PASS] 2. Admin login (admin@gg)")

    # 3. Auditor login
    res = client.post("/api/auth/login", json={"email": "auditor@gg", "password": "auditor"})
    assert res.status_code == 200, f"Auditor login failed: {res.text}"
    auditor_data = res.json()
    auditor_token = auditor_data["access_token"]
    assert auditor_data["user"]["role"] == "AUDITOR"
    print("[PASS] 3. Auditor login (auditor@gg)")

    # 4. Citizen registration
    import uuid
    test_email = f"citizen_{uuid.uuid4().hex[:6]}@example.com"
    res = client.post("/api/auth/register", json={
        "name": "Arjun Tester",
        "email": test_email,
        "password": "secretpassword"
    })
    assert res.status_code == 201, f"Registration failed: {res.text}"
    user_data = res.json()
    user_token = user_data["access_token"]
    assert user_data["user"]["role"] == "USER"
    print(f"[PASS] 4. Citizen registration ({test_email} strictly assigned role=USER)")

    # 5. User cannot access auditor or admin endpoints
    headers_user = {"Authorization": f"Bearer {user_token}"}
    res = client.get("/api/audits/pending", headers=headers_user)
    assert res.status_code == 403, f"Expected 403 for user accessing auditor API, got {res.status_code}"
    res = client.get("/api/admin/stats", headers=headers_user)
    assert res.status_code == 403, f"Expected 403 for user accessing admin API, got {res.status_code}"
    print("[PASS] 5. Role-based access control (USER received 403 on Auditor & Admin routes)")

    # 6. List projects
    res = client.get("/api/projects?limit=5")
    assert res.status_code == 200
    projects = res.json()["projects"]
    assert len(projects) > 0, "No projects returned"
    sample_project = projects[0]
    assert "location_source" in sample_project
    assert "location_accuracy" in sample_project
    print(f"[PASS] 6. Projects listed successfully (Found {res.json()['total']} total works, sample location_source: {sample_project['location_source']})")

    # 7. Citizen verification submission with real image
    img_byte_arr = io.BytesIO()
    img = Image.new("RGB", (200, 200), color=(73, 109, 137))
    img.save(img_byte_arr, format="JPEG")
    img_byte_arr.seek(0)

    files = {
        "photo": ("site_evidence.jpg", img_byte_arr.getvalue(), "image/jpeg")
    }
    data = {
        "project_id": sample_project["id"],
        "observation": "Completed",
        "notes": "Verified the site condition in person. High quality construction and accessible paths.",
        "check_in_type": "gps",
        "gps_latitude": 12.9716,
        "gps_longitude": 77.5946,
        "gps_accuracy": 15.0
    }
    res = client.post("/api/submissions", headers=headers_user, data=data, files=files)
    assert res.status_code == 201, f"Submission failed: {res.text}"
    sub_data = res.json()
    assert sub_data["status"] == "PENDING"
    assert "gps_verification_status" in sub_data
    submission_id = sub_data["id"]
    print(f"[PASS] 7. Citizen verification submitted (Status: PENDING, GPS quality: {sub_data.get('gps_verification_status')}, ID: {submission_id})")

    # 8. User sees notification
    res = client.get("/api/notifications", headers=headers_user)
    assert res.status_code == 200
    notifications = res.json()
    assert any(n["type"] == "SUBMISSION_RECEIVED" for n in notifications)
    print("[PASS] 8. Notification created for citizen")

    # 9. Auditor approves submission
    headers_auditor = {"Authorization": f"Bearer {auditor_token}"}
    res = client.get("/api/audits/pending", headers=headers_auditor)
    assert res.status_code == 200
    pending_list = res.json()
    assert any(p["id"] == submission_id for p in pending_list)

    res = client.post(
        f"/api/audits/{submission_id}/approve",
        headers=headers_auditor,
        json={"decision": "approved", "feedback": "Well photographed and matches site record."}
    )
    assert res.status_code == 200, f"Approve failed: {res.text}"
    approved_sub = res.json()
    assert approved_sub["status"] == "APPROVED"
    print(f"[PASS] 9. Auditor approved submission {submission_id}")

    # 10. Verify XP awarded to citizen (+150 XP)
    res = client.get("/api/auth/me", headers=headers_user)
    assert res.status_code == 200
    user_me = res.json()
    assert user_me["xp"] == 150, f"Expected 150 XP, got {user_me['xp']}"
    assert user_me["level"] == 1
    print(f"[PASS] 10. Citizen rewarded +150 XP (Current XP: {user_me['xp']}, Level: {user_me['level']})")

    # 11. Leaderboard includes citizen
    res = client.get("/api/leaderboard")
    assert res.status_code == 200
    leaders = res.json()["leaders"]
    assert any(l["id"] == user_me["id"] and l["xp"] == 150 for l in leaders)
    print("[PASS] 11. Real database leaderboard verified")

    # 12. Admin stats
    headers_admin = {"Authorization": f"Bearer {admin_token}"}
    res = client.get("/api/admin/stats", headers=headers_admin)
    assert res.status_code == 200
    stats = res.json()
    assert stats["approved_reviews"] >= 1
    assert stats["total_xp_awarded"] >= 150
    print(f"[PASS] 12. Admin statistics verified: {stats}")

    print("\nALL 12 BACKEND TESTS PASSED SUCCESSFULLY!")

if __name__ == "__main__":
    run_tests()
