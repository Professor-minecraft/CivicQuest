"""
Verification script for CivicQuest Authentication Gate, Role-based Access, and Map APIs.
"""
import sys
import io
import requests

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

API_BASE = "http://127.0.0.1:8000"
FRONTEND_BASE = "http://localhost:3000"

def test_all():
    print("--- 1. Testing Frontend Public Availability ---")
    r_fe = requests.get(FRONTEND_BASE)
    assert r_fe.status_code == 200, f"Frontend failed: {r_fe.status_code}"
    assert "CivicQuest" in r_fe.text, "CivicQuest branding not found in HTML"
    print("✓ Frontend serves CivicQuest HTML successfully (HTTP 200)")

    print("\n--- 2. Testing Map & Dynamic Stats Endpoints ---")
    r_stats = requests.get(f"{API_BASE}/api/projects/summary-stats")
    assert r_stats.status_code == 200, f"Stats failed: {r_stats.status_code}"
    stats = r_stats.json()
    print(f"✓ Summary stats: {stats}")
    assert stats["total_works"] > 30000
    assert stats["total_states"] > 25
    assert stats["total_constituencies"] > 400

    r_map = requests.get(f"{API_BASE}/api/projects/map-works?limit=5")
    assert r_map.status_code == 200
    works = r_map.json()
    assert len(works) > 0
    w0 = works[0]
    assert "latitude" in w0 and w0["latitude"] is not None
    assert "longitude" in w0 and w0["longitude"] is not None
    assert "location_source" in w0
    print(f"✓ Map works endpoint returned valid coordinates: {w0['work']} @ ({w0['latitude']}, {w0['longitude']}) [{w0['location_source']}]")

    r_nearby = requests.get(f"{API_BASE}/api/projects/nearby?lat=18.67&lng=78.09&radius_km=50")
    assert r_nearby.status_code == 200
    nearby_works = r_nearby.json()
    print(f"✓ Nearby works endpoint returned {len(nearby_works)} works within 50km radius")

    print("\n--- 3. Testing Backend Route Protection (Unauthenticated) ---")
    r_unauth_sub = requests.post(f"{API_BASE}/api/submissions", data={})
    assert r_unauth_sub.status_code == 401, f"Expected 401, got {r_unauth_sub.status_code}"
    print("✓ Unauthenticated submission access correctly blocked (HTTP 401)")

    r_unauth_auditor = requests.get(f"{API_BASE}/api/audits/pending")
    assert r_unauth_auditor.status_code == 401, f"Expected 401, got {r_unauth_auditor.status_code}"
    print("✓ Unauthenticated auditor access correctly blocked (HTTP 401)")

    r_unauth_admin = requests.get(f"{API_BASE}/api/admin/stats")
    assert r_unauth_admin.status_code == 401, f"Expected 401, got {r_unauth_admin.status_code}"
    print("✓ Unauthenticated admin access correctly blocked (HTTP 401)")

    print("\n--- 4. Testing Public Registration (Always USER role) ---")
    reg_email = "test_citizen_verifier_99@civicquest.org"
    r_reg = requests.post(
        f"{API_BASE}/api/auth/register",
        json={"name": "Priya Sharma", "email": reg_email, "password": "SecureCitizen123!"}
    )
    if r_reg.status_code == 400 and ("already registered" in r_reg.text or "already exists" in r_reg.text):
        # Already registered in previous test run, login instead
        r_log = requests.post(f"{API_BASE}/api/auth/token", data={"username": reg_email, "password": "SecureCitizen123!"})
        reg_data = r_log.json()
    else:
        assert r_reg.status_code in (200, 201), f"Register failed: {r_reg.text}"
        reg_data = r_reg.json()

    user_token = reg_data["access_token"]
    user_headers = {"Authorization": f"Bearer {user_token}"}
    r_me = requests.get(f"{API_BASE}/api/auth/me", headers=user_headers)
    assert r_me.status_code == 200
    user_profile = r_me.json()
    assert user_profile["role"] == "USER", f"Expected USER role, got {user_profile['role']}"
    print(f"✓ Citizen registration succeeded: {user_profile['name']} with backend-enforced role={user_profile['role']}")

    # Citizen token cannot access auditor or admin endpoints
    r_cit_auditor = requests.get(f"{API_BASE}/api/audits/pending", headers=user_headers)
    assert r_cit_auditor.status_code == 403, f"Citizen must be 403 for auditor desk, got {r_cit_auditor.status_code}"
    print("✓ Citizen token blocked from Auditor endpoints (HTTP 403 Forbidden)")

    r_cit_admin = requests.get(f"{API_BASE}/api/admin/stats", headers=user_headers)
    assert r_cit_admin.status_code == 403, f"Citizen must be 403 for admin panel, got {r_cit_admin.status_code}"
    print("✓ Citizen token blocked from Admin endpoints (HTTP 403 Forbidden)")

    print("\n--- 5. Testing Auditor Role Authentication & Isolation ---")
    r_aud_login = requests.post(f"{API_BASE}/api/auth/token", data={"username": "auditor@gg", "password": "auditor"})
    assert r_aud_login.status_code == 200, f"Auditor login failed: {r_aud_login.text}"
    aud_token = r_aud_login.json()["access_token"]
    aud_headers = {"Authorization": f"Bearer {aud_token}"}
    r_aud_me = requests.get(f"{API_BASE}/api/auth/me", headers=aud_headers)
    assert r_aud_me.json()["role"] == "AUDITOR"
    r_aud_subs = requests.get(f"{API_BASE}/api/audits/pending", headers=aud_headers)
    assert r_aud_subs.status_code == 200
    print(f"✓ Auditor authenticated: {r_aud_me.json()['name']} (role={r_aud_me.json()['role']}), accessed auditor desk (HTTP 200)")

    r_aud_admin = requests.get(f"{API_BASE}/api/admin/stats", headers=aud_headers)
    assert r_aud_admin.status_code == 403
    print("✓ Auditor token blocked from Admin endpoints (HTTP 403 Forbidden)")

    print("\n--- 6. Testing Admin Role Authentication & Access ---")
    r_adm_login = requests.post(f"{API_BASE}/api/auth/token", data={"username": "admin@gg", "password": "admin"})
    assert r_adm_login.status_code == 200, f"Admin login failed: {r_adm_login.text}"
    adm_token = r_adm_login.json()["access_token"]
    adm_headers = {"Authorization": f"Bearer {adm_token}"}
    r_adm_me = requests.get(f"{API_BASE}/api/auth/me", headers=adm_headers)
    assert r_adm_me.json()["role"] == "ADMIN"
    r_adm_stats = requests.get(f"{API_BASE}/api/admin/stats", headers=adm_headers)
    assert r_adm_stats.status_code == 200
    print(f"✓ Admin authenticated: {r_adm_me.json()['name']} (role={r_adm_me.json()['role']}), accessed admin stats (HTTP 200)")

    print("\n==============================================")
    print("ALL VERIFICATIONS COMPLETED SUCCESSFULLY!")
    print("==============================================")

if __name__ == "__main__":
    try:
        test_all()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
