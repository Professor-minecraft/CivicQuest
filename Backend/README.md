# CivicQuest Backend — Civic Verification Platform

Production REST API backend built with Python, FastAPI, PostgreSQL/SQLAlchemy, and Pydantic.

## Prerequisites

- Python 3.10+ (tested on Python 3.14)
- PostgreSQL (optional: falls back to local SQLite if PostgreSQL credentials are not yet entered)

---

## 1. Quick Setup (Windows PowerShell)

```powershell
# Navigate to Backend folder
cd Backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

---

## 2. Environment Configuration

Copy `.env.example` to `.env`:

```powershell
cp .env.example .env
```

Edit `Backend/.env` to configure your PostgreSQL credentials:

```env
DATABASE_URL=postgresql+psycopg://postgres:YOUR_PASSWORD@localhost:5432/civicquest
JWT_SECRET=YOUR_SUPER_SECRET_RANDOM_KEY
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

---

## 3. Initialize Database & Seed Accounts

Run the database seeder to create tables and default accounts:

```powershell
python scripts/seed_db.py
```

### Default Accounts

- **Admin**:
  - Email: `admin@gg`
  - Password: `admin`
  - Role: `ADMIN` (Password hashed with bcrypt)
- **Auditor**:
  - Email: `auditor@gg`
  - Password: `auditor`
  - Role: `AUDITOR` (Password hashed with bcrypt)

---

## 4. Import MPLADS CSV Dataset

To import the 35,293 completed works records:

```powershell
# Import first 200 records for fast testing:
python scripts/import_csv.py --limit 200

# Or import all 35,293 records:
python scripts/import_csv.py
```

---

## 5. Run the Backend Server

```powershell
uvicorn app.main:app --reload --port 8000
```

The API will be available at:
- **API Base**: `http://localhost:8000`
- **Interactive Swagger Docs**: `http://localhost:8000/docs`
- **ReDoc Documentation**: `http://localhost:8000/redoc`

---

## 6. Architecture & Core Endpoints

| Method | Endpoint | Access | Purpose |
|--------|----------|--------|---------|
| `POST` | `/api/auth/register` | Public | Citizen signup (strictly assigns `role = USER`) |
| `POST` | `/api/auth/login` | Public | Authenticates `USER`, `AUDITOR`, `ADMIN` |
| `GET`  | `/api/auth/me` | Authenticated | Current user profile |
| `GET`  | `/api/projects` | Public | List government works with state/constituency/category filters |
| `GET`  | `/api/projects/{id}` | Public | Detailed work information |
| `POST` | `/api/submissions` | `USER` | Upload photo & GPS verification (`PENDING`) |
| `GET`  | `/api/submissions/my` | `USER` | Get logged-in citizen's quests and feedback |
| `GET`  | `/api/audits/pending` | `AUDITOR`, `ADMIN` | List submissions awaiting audit |
| `POST` | `/api/audits/{id}/approve` | `AUDITOR`, `ADMIN` | Approve verification (`+150 XP`, audit record, notification) |
| `POST` | `/api/audits/{id}/reject` | `AUDITOR`, `ADMIN` | Reject verification with mandatory feedback |
| `GET`  | `/api/leaderboard` | Public | Real database citizen rankings by XP |
| `GET`  | `/api/notifications` | Authenticated | User notification feed |
| `GET`  | `/api/certificates` | `USER` | Unlocked citizen certificates |
| `GET`  | `/api/certificates/{id}/download` | `USER` | Download generated ReportLab PDF certificate |
| `GET`  | `/api/admin/stats` | `ADMIN` | Platform metrics overview |
| `GET`  | `/api/admin/users` | `ADMIN` | User directory and role management |
| `POST` | `/api/admin/import-csv` | `ADMIN` | Trigger background CSV import |
