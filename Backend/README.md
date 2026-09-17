<div align="center">

# ⚡ CivicQuest — Backend Service
### *FastAPI Backend Powering CivicQuest's Civic Verification Platform*

<p align="center">
  <b>High-performance asynchronous REST API, geospatial resolution engine, and administrative backend for civic oversight.</b><br />
  Built with Python 3.10+, FastAPI, PostgreSQL, SQLAlchemy 2.0, Pydantic, and Folium.
</p>

<p align="center">
  <a href="https://civicquest-backend.onrender.com"><img src="https://img.shields.io/badge/Live_API-Render-46E3B7?style=for-the-badge&logo=render&logoColor=white" alt="Live API Base" /></a>
  <a href="https://civicquest-backend.onrender.com/docs"><img src="https://img.shields.io/badge/OpenAPI_Swagger-Docs-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="Swagger UI" /></a>
  <a href="https://civicquest-backend.onrender.com/redoc"><img src="https://img.shields.io/badge/ReDoc-API_Reference-FF5722?style=for-the-badge&logo=redoc&logoColor=white" alt="ReDoc" /></a>
  <a href="https://civicquest-backend.onrender.com/map"><img src="https://img.shields.io/badge/Interactive_Map-Folium-199900?style=for-the-badge&logo=leaflet&logoColor=white" alt="Folium Map" /></a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/FastAPI-0.115+-009688?style=flat-square&logo=fastapi&logoColor=white" alt="FastAPI" />
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/PostgreSQL-15+-4169E1?style=flat-square&logo=postgresql&logoColor=white" alt="PostgreSQL" />
  <img src="https://img.shields.io/badge/SQLAlchemy-2.0+-D71F00?style=flat-square&logo=sqlalchemy&logoColor=white" alt="SQLAlchemy" />
  <img src="https://img.shields.io/badge/Pydantic-v2-E92063?style=flat-square&logo=pydantic&logoColor=white" alt="Pydantic" />
  <img src="https://img.shields.io/badge/License-Not_Specified-lightgrey?style=flat-square" alt="License" />
</p>

<br />

<div style="background: linear-gradient(135deg, #064e3b 0%, #022c22 100%); padding: 18px 24px; border-radius: 12px; margin: 12px 0; border: 1px solid #059669;">
  <span style="color: #6ee7b7; font-size: 13px; font-weight: 700; letter-spacing: 1px; text-transform: uppercase;">🌐 Production Service Status</span><br />
  <span style="color: #ffffff; font-size: 18px; font-weight: 600;">API Base Endpoint: </span>
  <a href="https://civicquest-backend.onrender.com" style="color: #a7f3d0; font-size: 18px; font-weight: 700; text-decoration: underline;">https://civicquest-backend.onrender.com</a>
</div>

<br />

<p align="center">
  <a href="#-overview">Overview</a> •
  <a href="#-architecture">Architecture</a> •
  <a href="#-technology-stack">Tech Stack</a> •
  <a href="#-project-structure">Structure</a> •
  <a href="#-api-documentation--endpoints">API Docs</a> •
  <a href="#-authentication--rbac">Authentication</a> •
  <a href="#-database--models">Database</a> •
  <a href="#-environment-variables">Environment</a> •
  <a href="#-csv-dataset-ingestion">CSV Import</a> •
  <a href="#-local-development">Local Setup</a> •
  <a href="#-deployment">Deployment</a>
</p>

</div>

---

## 🚀 Overview

The **CivicQuest Backend** is an enterprise-grade REST service written in **Python 3** using the **FastAPI** framework. It acts as the operational nerve center for the CivicQuest platform, managing data synchronization, verification integrity, and civic gamification across over 35,000 public development records.

### Key Capabilities
- **Authentication & RBAC:** Secure user registration, salted bcrypt password hashing, and stateless JWT authorization enforcing Citizen (`USER`), Community Auditor (`AUDITOR`), and Platform Administrator (`ADMIN`) roles.
- **MPLADS Works Management:** Paginated catalog filtering, full-text search across project descriptions, bounding-box proximity searches, and lightweight map data serialization.
- **Geospatial & Coordinate Resolution:** Priority-driven location resolution combining exact dataset coordinates, 543 Parliamentary Constituency Centroids, and cached OpenStreetMap Nominatim geocoding.
- **Evidence Verification Pipeline:** Multi-part file upload receiving citizen site photos, Pillow-based image validation, and server-side Haversine distance proximity verification.
- **Auditor Workflow Engine:** Review inbox for unmoderated claims, atomic approval transactions awarding $+150\text{ XP}$, level recalculation, and mandatory rejection feedback.
- **Vector PDF Certificate Engine:** On-demand cryptographic certificate generation compiled as vector PDFs using ReportLab for citizens reaching 5 approved audits.
- **Streaming Dataset Pipeline:** High-performance Pandas ingestion stream capable of importing tens of thousands of records without memory spikes.

---

## 🏛️ Architecture

The backend sits between the frontend client and data stores:

```
┌─────────────────────────────────────────────────────────────┐
│                    NEXT.JS FRONTEND                         │
│         [ https://civicquest-tau.vercel.app/ ]              │
└────────────────────────────┬────────────────────────────────┘
                             │  HTTPS / JSON / Multipart
                             ▼
┌─────────────────────────────────────────────────────────────┐
│                    FASTAPI REST BACKEND                     │
│         [ https://civicquest-backend.onrender.com ]         │
│                                                             │
│  ┌──────────────────┐   ┌───────────────────────────────┐   │
│  │ CORS Middleware  │   │  PyJWT Bearer Authentication  │   │
│  └────────┬─────────┘   └───────────────┬───────────────┘   │
│           │                             │                   │
│  ┌────────┴─────────────────────────────┴───────────────┐   │
│  │                    API ROUTERS                       │   │
│  │  /auth · /projects · /submissions · /audits          │   │
│  │  /certificates · /leaderboard · /notifications · /admin │
│  └──────────────────────┬───────────────────────────────┘   │
│                         │                                   │
│  ┌──────────────────────┴───────────────────────────────┐   │
│  │                  SERVICES CORE                       │   │
│  │  • geocoding.py (Haversine, Nominatim & Cache)       │   │
│  │  • csv_import.py (Pandas Batch Ingestion Stream)     │   │
│  │  • map_generator.py (Folium Clusters & Hubs)         │   │
│  │  • certificates.py (ReportLab PDF Generation)        │   │
│  └──────────────────────┬───────────────────────────────┘   │
│                         │                                   │
│  ┌──────────────────────┴───────────────────────────────┐   │
│  │             SQLAlchemy 2.0 ORM Engine                │   │
│  └──────────────────────┬───────────────────────────────┘   │
└─────────────────────────┼───────────────────────────────────┘
                          │
         ┌────────────────┴────────────────┐
         ▼                                 ▼
┌──────────────────┐             ┌──────────────────┐
│  🐘 POSTGRESQL   │             │   📁 /uploads    │
│   (Render DB)    │             │ (Pillow Verified │
│ Users, Projects, │             │  Citizen Photos) │
│ Submissions,     │             └──────────────────┘
│ Notifications,   │             ┌──────────────────┐
│ Certificates     │             │ 📊 Static Assets │
│ & Cache          │             │ Works Completed  │
└──────────────────┘             │ centroids.json   │
                                 └──────────────────┘
```

---

## 🛠️ Technology Stack

Every package in the backend is chosen for speed, reliability, and security:

<div align="center">

| Package | Version | Purpose |
|---|---|---|
| **[Python](https://www.python.org/)** | `>=3.10` (Tested on `3.14`) | Core runtime language |
| **[FastAPI](https://fastapi.tiangolo.com/)** | `>=0.115.0` | High-throughput asynchronous REST web framework |
| **[Uvicorn](https://www.uvicorn.org/)** | `>=0.30.0` | Production ASGI web server (`uvicorn[standard]`) |
| **[SQLAlchemy](https://www.sqlalchemy.org/)** | `>=2.0.30` | Modern declarative ORM and connection pooling |
| **[psycopg](https://www.psycopg.org/)** | `>=3.2.0` | Native binary PostgreSQL driver adapter (`psycopg[binary]`) |
| **[Pydantic](https://docs.pydantic.dev/)** | `>=2.7.0` | Strict schema validation, serialization, and typing |
| **[Pydantic-Settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/)** | `>=2.3.0` | Environment configuration loading from `.env` |
| **[bcrypt](https://github.com/pyca/bcrypt/)** | `>=4.2.0` | Salted cryptographic password hashing |
| **[PyJWT](https://pyjwt.readthedocs.io/)** | `>=2.9.0` | Stateless JSON Web Token encoding and verification |
| **[Pillow](https://python-pillow.org/)** | `>=10.4.0` | Server-side image decoding and header verification |
| **[Pandas](https://pandas.pydata.org/)** | `>=2.0.0` | High-performance streaming CSV parser and batcher |
| **[Geopy](https://geopy.readthedocs.io/)** | `>=2.4.1` | Nominatim geocoder with rate-limiting and cache |
| **[Folium](https://python-visualization.github.io/folium/)** | `>=0.17.0` | Standalone interactive HTML Leaflet map compiler |
| **[GeoPandas](https://geopandas.org/)** | `>=1.0.0` | Geospatial dataset manipulation |
| **[Shapely](https://shapely.readthedocs.io/)** | `>=2.0.0` | Geometric operations and spatial point calculations |
| **[ReportLab](https://www.reportlab.com/)** | `>=4.2.2` | Vector PDF generation for civic certificates |
| **[python-multipart](https://andrew-d.github.io/python-multipart/)** | `>=0.0.9` | Streaming multipart/form-data upload parsing |
| **[email-validator](https://github.com/JoshData/python-email-validator)** | `>=2.0.0` | Strict RFC-compliant email address validation |
| **[HTTPX](https://www.httpx.org/)** | `>=0.28.0` | Modern asynchronous HTTP client |

</div>

---

## 📁 Backend Project Structure

```text
Backend/
├── app/
│   ├── __init__.py             # Package initializer
│   ├── auth.py                 # bcrypt password hashing & PyJWT token utilities
│   ├── config.py               # Pydantic BaseSettings loading .env configuration
│   ├── database.py             # SQLAlchemy engine, session maker & declarative base
│   ├── dependencies.py         # HTTPBearer auth extraction & require_role() guards
│   ├── main.py                 # FastAPI application, CORS, static mounts & startup seed
│   ├── models.py               # SQLAlchemy ORM models (User, Project, Submission, etc.)
│   ├── schemas.py              # Pydantic request/response schemas (DTOs)
│   ├── routers/
│   │   ├── admin.py            # /api/admin — Platform stats, user roles, CSV import
│   │   ├── audits.py           # /api/audits — Review queue, approve/reject endpoints
│   │   ├── auth.py             # /api/auth — Signup, login, and current user profile
│   │   ├── certificates.py     # /api/certificates — Unlocked certs & PDF download
│   │   ├── leaderboard.py      # /api/leaderboard — Citizen XP ranking queries
│   │   ├── notifications.py    # /api/notifications — User notification inbox
│   │   ├── projects.py         # /api/projects — Catalog, filters, nearby & map data
│   │   └── submissions.py      # /api/submissions — Photo upload & GPS verification
│   └── services/
│       ├── certificates.py     # ReportLab PDF certificate canvas builder
│       ├── csv_import.py       # Pandas chunked CSV stream & priority-protected sync
│       ├── geocoding.py        # Haversine distance, Nominatim client & cache
│       └── map_generator.py    # Folium map builder (504 constituency hubs + clusters)
│
├── data/
│   ├── Works Completed.csv     # Full raw MPLADS dataset (11.2 MB, 35,293 records)
│   ├── constituency_centroids.json # 543 Parliamentary Constituency reference coordinates
│   ├── works_completed.csv     # Normalized dataset copy
│   └── works_map.html          # Precompiled Folium interactive map
│
├── scripts/
│   ├── generate_folium_map.py  # Standalone script to compile data/works_map.html
│   ├── import_csv.py           # CLI tool for streaming dataset import with flags
│   ├── seed_db.py              # Initializes database tables and default accounts
│   └── test_api.py             # Automated 12-step end-to-end integration test suite
│
├── uploads/                    # Storage directory for verified citizen evidence
├── .env.example                # Template configuration file for development
├── requirements.txt            # Pinned Python package dependencies
└── README.md                   # Backend documentation
```

---

## 📡 API Documentation & Endpoints

FastAPI automatically serves interactive, contract-compliant documentation:

<div align="center">

| Interface | Cloud URL | Description |
|---|---|---|
| **Swagger UI** | [`https://civicquest-backend.onrender.com/docs`](https://civicquest-backend.onrender.com/docs) | Interactive testing console with schema inspection |
| **ReDoc** | [`https://civicquest-backend.onrender.com/redoc`](https://civicquest-backend.onrender.com/redoc) | Responsive, clean technical reference |
| **Root Health** | [`https://civicquest-backend.onrender.com/`](https://civicquest-backend.onrender.com/) | Platform online status, version, and links |
| **National Map** | [`https://civicquest-backend.onrender.com/map`](https://civicquest-backend.onrender.com/map) | Folium HTML map rendering all 35k+ works |

</div>

<br />

### Endpoint Catalog

```
CivicQuest REST API
├── /api/auth
│   ├── POST   /register             Public: Registers a new citizen (strictly sets role=USER)
│   ├── POST   /login                Public: Verifies credentials via bcrypt; returns JWT
│   ├── GET    /me                   Authenticated: Returns active user profile
│   └── POST   /logout               Authenticated: Client session termination helper
│
├── /api/projects
│   ├── GET    /                     Public: Filterable catalog (state, constituency, category)
│   ├── GET    /summary-stats        Public: Dynamic database statistics (works, states, counts)
│   ├── GET    /states               Public: List of states with recorded project volumes
│   ├── GET    /nearby               Public: Haversine radius search (?lat=..&lng=..&radius_km=25)
│   ├── GET    /map-hubs             Public: Aggregated 504 constituency hubs (~45KB payload)
│   ├── GET    /map-works            Public: Lightweight coordinate array for map plotting
│   └── GET    /{id}                 Public: Complete metadata for a specific work
│
├── /api/submissions
│   ├── POST   /                     USER: Upload site photo & GPS data (Status: PENDING)
│   └── GET    /my                   USER: Get logged-in citizen's personal quests
│
├── /api/audits
│   ├── GET    /pending              AUDITOR/ADMIN: List unreviewed pending submissions
│   ├── GET    /history              AUDITOR/ADMIN: List past reviewed audits with decisions
│   ├── POST   /{id}/approve         AUDITOR/ADMIN: Approve quest (+150 XP, check certificate)
│   └── POST   /{id}/reject          AUDITOR/ADMIN: Reject quest (mandatory feedback >= 5 chars)
│
├── /api/certificates
│   ├── GET    /                     USER: Unlocked civic participation certificates
│   └── GET    /{id}/download        USER/AUDITOR/ADMIN: Streams generated ReportLab vector PDF
│
├── /api/leaderboard
│   └── GET    /                     Public: Citizens ranked by verified XP from database
│
├── /api/notifications
│   ├── GET    /                     Authenticated: User notification inbox
│   └── PATCH  /{id}/read            Authenticated: Mark notification as read
│
└── /api/admin
    ├── GET    /stats                ADMIN: Platform-wide analytics and audit volumes
    ├── GET    /users                ADMIN: User directory with role filtering
    ├── PATCH  /users/{id}           ADMIN: Promote/demote user permissions
    ├── GET    /submissions          ADMIN: Global submissions audit overview
    └── POST   /import-csv           ADMIN: Trigger batch CSV import (background or synchronous)
```

---

## 🔐 Authentication & RBAC

CivicQuest enforces a 3-tier Role-Based Access Control model:

```
[ Unauthenticated Request ]
            │
            ▼
    [ Bearer Token? ] ──(No)──► Allow only Public routes (Projects, Map, Leaderboard)
            │ (Yes)
            ▼
   [ Decode HS256 JWT ]
            │
            ├─► Role: USER      ──► Submissions, Personal Quests, Certificates
            ├─► Role: AUDITOR   ──► Review Queue, Approve/Reject Decisions (+ User Scope)
            └─► Role: ADMIN     ──► Platform Analytics, User Role Management, CSV Import
```

### Role Scope
1. **Citizen Explorer (`USER`):** Can search public works, submit field verifications with photos and GPS, track quest history, and download earned certificates. Cannot access moderation queues or admin tools.
2. **Community Auditor (`AUDITOR`):** Can review pending citizen submissions, inspect photos, evaluate GPS proximity, and record binding audit decisions with feedback.
3. **Platform Administrator (`ADMIN`):** Can inspect system-wide audit metrics, manage user roles (promote users to Auditor), oversee all submissions, and trigger dataset ingestion.

> [!IMPORTANT]
> **Credential Security Notice:**
> Passwords are salted with random 12-round salts and hashed using `bcrypt` before storage. Plaintext passwords are never saved. Real passwords and database credentials are **never** committed to version control. Set your own secure credentials upon initial setup.

---

## 🗄️ Database & Models

CivicQuest uses **SQLAlchemy 2.0** with 7 primary relational tables:

```
┌─────────────────┐       ┌─────────────────┐       ┌─────────────────┐
│     users       │       │    projects     │       │ location_cache  │
├─────────────────┤       ├─────────────────┤       ├─────────────────┤
│ id (PK)         │       │ id (PK)         │       │ id (PK)         │
│ name            │       │ work            │       │ query_key (UQ)  │
│ email (UQ)      │       │ work_category   │       │ latitude        │
│ password_hash   │       │ state           │       │ longitude       │
│ role (Enum)     │       │ constituency    │       │ location_source │
│ xp (Integer)    │       │ amount_disbursed│       │ geocoded_at     │
│ level (Integer) │       │ latitude        │       └─────────────────┘
└────────┬────────┘       │ longitude       │
         │ 1              │ location_source │
         │                └────────┬────────┘
         │                         │ 1
         │ N                       │ N
┌────────┴─────────────────────────┴────────┐
│               submissions                 │
├───────────────────────────────────────────┤
│ id (PK, sub-*)                            │
│ user_id (FK -> users.id)                  │
│ project_id (FK -> projects.id)            │
│ photo_url, observation, notes             │
│ check_in_type (gps / simulated)           │
│ gps_latitude, gps_longitude, gps_accuracy │
│ distance_from_project, gps_verification   │
│ status (PENDING / APPROVED / REJECTED)    │
│ reviewed_by (FK -> users.id)              │
│ review_feedback, submitted_at, reviewed_at│
└─────────────────────┬─────────────────────┘
                      │ 1
                      │ N
         ┌────────────┴────────────┐
         ▼                         ▼
┌─────────────────┐       ┌─────────────────┐
│  audit_records  │       │  notifications  │
├─────────────────┤       ├─────────────────┤
│ id (PK)         │       │ id (PK)         │
│ submission_id   │       │ user_id (FK)    │
│ auditor_id (FK) │       │ title, message  │
│ decision        │       │ type, is_read   │
│ feedback        │       │ created_at      │
│ created_at      │       └─────────────────┘
└─────────────────┘
```

---

## ⚙️ Environment Variables

The backend loads configuration from `.env` using Pydantic Settings (`app/config.py`):

```env
# Database Connection URI (psycopg 3 binary driver)
DATABASE_URL=postgresql+psycopg://USER:PASSWORD@HOST:PORT/DATABASE

# Cryptographic Token Secret (HS256)
JWT_SECRET=your_super_secret_high_entropy_random_string

# Token Parameters
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# Allowed CORS Origins (Comma-separated)
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000,https://civicquest-tau.vercel.app

# File Storage Paths
UPLOAD_DIR=uploads
DATA_CSV_PATH=data/works_completed.csv
```

### Variable Reference

| Variable | Type | Default | Description |
|---|:---:|---|---|
| `DATABASE_URL` | String | `postgresql+psycopg://...` | Connection URI. Supports PostgreSQL or SQLite fallback for testing. |
| `JWT_SECRET` | String | *Development placeholder* | Private key used to sign HS256 authentication tokens. |
| `JWT_ALGORITHM` | String | `HS256` | JWT signing algorithm. |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Integer | `1440` (24 hours) | Lifespan of issued bearer access tokens. |
| `CORS_ORIGINS` | String | `http://localhost:3000,...` | Comma-separated list of origins permitted to communicate via CORS. |
| `UPLOAD_DIR` | String | `uploads` | Directory where uploaded evidence photos are stored. |
| `DATA_CSV_PATH` | String | `data/works_completed.csv` | Relative or absolute path to the MPLADS dataset file. |
| `APPROVAL_XP` | Integer | `150` | XP awarded to a citizen per approved project inspection. |
| `LEVEL_XP` | Integer | `450` | XP threshold required to advance to the next explorer level. |
| `CERTIFICATE_THRESHOLD` | Integer | `5` | Approved verification count required to unlock a participation certificate. |
| `MAX_FILE_SIZE_BYTES` | Integer | `8388608` (8 MB) | Maximum permitted file upload size. |

---

## 📊 CSV Dataset Ingestion

The backend includes a streaming ingestion engine (`app/services/csv_import.py`) powered by **Pandas**:

```bash
# Ingest first 200 rows for rapid local testing:
python scripts/import_csv.py --limit 200

# Ingest with custom batch size:
python scripts/import_csv.py --batch-size 1000

# Ingest all 35,293 records:
python scripts/import_csv.py
```

### Ingestion Features
- **Streaming Chunks:** Reads CSV in chunks of 1,000 rows to ensure low memory consumption.
- **Priority Coordinate Protection:** If a project already has a verified location (e.g., `EXACT_DATASET`), incoming approximate data will **never** overwrite it.
- **Amount & String Normalization:** Cleans rupee symbols (₹), commas, and whitespace anomalies.
- **Background API Trigger:** Administrators can trigger imports directly from the web interface via `POST /api/admin/import-csv`.

---

## 🗺️ Location & Coordinate Resolution

CivicQuest applies a strict coordinate hierarchy to ensure transparent geographical representation:

```
┌────────────────────────────────────────────────────────┐
│             COORDINATE RESOLUTION HIERARCHY            │
├─────────┬─────────────────────────┬────────────────────┤
│ Priority│ Source                  │ Accuracy Tag       │
├─────────┼─────────────────────────┼────────────────────┤
│ 1 (Top) │ EXACT_DATASET           │ EXACT              │
│ 2       │ CONSTITUENCY_CENTROID   │ APPROXIMATE        │
│ 3       │ Cached Nominatim Geocode│ APPROXIMATE        │
│ 4       │ District / City Lookup  │ APPROXIMATE        │
│ 5 (Low) │ MISSING                 │ MISSING            │
└─────────┴─────────────────────────┴────────────────────┘
```

> [!IMPORTANT]
> **Approximate Location Disclosure:**
> Most records in the raw MPLADS dataset list the Parliamentary Constituency and Implementing Agency without physical GPS coordinates.
> CivicQuest maps these projects to the **Parliamentary Constituency Centroid** derived from authoritative OpenGIS datasets (`data/constituency_centroids.json`).
> 
> When citizens verify against these records, the GPS engine designates proximity as **`LIMITED`**. This transparently alerts auditors that the citizen is within the regional constituency, but sub-meter physical attendance at the exact gate cannot be mathematically confirmed.

---

## 📸 Evidence Uploads & Validation

Citizen evidence photos are handled through a dedicated pipeline:

1. **File Type Verification:** Enforces MIME types: `image/jpeg`, `image/png`, `image/webp`.
2. **File Size Check:** Enforces `MAX_FILE_SIZE_BYTES` limit (8 MB).
3. **Pillow Header Verification:**
   ```python
   with Image.open(image_stream) as img:
       img.verify()  # Validates image structure; catches corrupted or spoofed files
   ```
4. **Collision-Free Storage:** Writes files using a unique UUID (`uuid.uuid4().hex.jpg`) to prevent path traversal attacks.
5. **Static File Serving:** Mounted at `/uploads` via FastAPI's `StaticFiles`:
   ```python
   app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
   ```

---

## 💻 Local Development Setup

### Prerequisites
- **Python 3.10+** (Tested on Python 3.14)
- **PostgreSQL 15+** *(Optional: fallback to SQLite supported for local testing)*

---

### Step-by-Step Installation

```bash
# 1. Navigate to the Backend folder
cd Backend

# 2. Create and activate a Python virtual environment
python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Copy and configure environment variables
cp .env.example .env
# Edit .env to set your PostgreSQL connection string and secret key

# 5. Initialize database tables and seed initial accounts
python scripts/seed_db.py

# 6. Import MPLADS dataset (first 200 records for fast local testing)
python scripts/import_csv.py --limit 200

# 7. Start the development server with live reload
uvicorn app.main:app --port 8000 --reload
```

The server will be available at **[`http://127.0.0.1:8000`](http://127.0.0.1:8000)**.
Open **[`http://127.0.0.1:8000/docs`](http://127.0.0.1:8000/docs)** to test endpoints in Swagger UI.

---

## 🧪 Automated Testing

CivicQuest includes an automated test suite verifying all 12 core backend integration workflows:

```bash
python scripts/test_api.py
```

### Tested Scenarios
1. Health check verification (`GET /`)
2. Administrator login & JWT generation
3. Auditor login & JWT generation
4. Citizen registration (`role = "USER"` constraint)
5. RBAC security: verifies `403 Forbidden` on unauthorized route access
6. Project catalog queries and location metadata parsing
7. Multipart citizen evidence upload with Pillow validation
8. In-app notification creation
9. Auditor approval workflow and feedback logging
10. XP calculation (+150 XP atomic increment) and level recalculation
11. Real-time leaderboard indexing of verified citizens
12. Platform administrative metric aggregations

---

## 🚀 Cloud Deployment (Render)

The backend is configured for deployment on **[Render](https://render.com/)**:

### Render Web Service Settings
- **Environment:** `Python 3`
- **Root Directory:** `Backend`
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- **Environment Variables:**
  - `DATABASE_URL`: Connection string from your Render PostgreSQL instance.
  - `JWT_SECRET`: High-entropy random secret key.
  - `CORS_ORIGINS`: Allowed client domains (e.g., `https://civicquest-tau.vercel.app`).
  - `UPLOAD_DIR`: `uploads`
  - `DATA_CSV_PATH`: `data/works_completed.csv`

---

## 🔧 Troubleshooting

| Issue | Root Cause | Resolution |
|---|---|---|
| **`psycopg.OperationalError: connection failed`** | PostgreSQL is not running or credentials invalid | Verify PostgreSQL is running on port 5432 and `DATABASE_URL` matches credentials. |
| **CORS policy error on frontend** | Client domain not in `CORS_ORIGINS` | Add the frontend domain (e.g. `https://civicquest-tau.vercel.app`) to `CORS_ORIGINS` in `.env`. |
| **`FileNotFoundError: Works Completed.csv`** | CSV path incorrect | Ensure `DATA_CSV_PATH` points to `data/works_completed.csv` relative to Backend root. |
| **Render Web Service spinning down** | Free tier inactivity suspension | Initial requests after inactivity take ~30 seconds to spin up the container. |
| **`413 Request Entity Too Large`** | Photo exceeds 8 MB | The server limits uploads to 8 MB (`MAX_FILE_SIZE_BYTES`). Ensure client downscaling is active. |

---

## 🗺️ Future Roadmap

- [ ] **EXIF Metadata Parsing:** Extract hardware timestamps and sensor GPS directly from JPEG EXIF headers.
- [ ] **AI-Assisted Photo Moderation:** Automated pre-screening using lightweight computer vision models to flag off-topic images.
- [ ] **S3/Cloudflare R2 Object Storage:** Transition `/uploads` from local disk to S3-compatible cloud object storage.
- [ ] **Webhook Event Subscriptions:** Allow civic organizations to subscribe to approved verification events via webhooks.

---

## 📄 License & Attribution

This backend service is part of the CivicQuest civic transparency platform. License information has not yet been specified.
