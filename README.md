<div align="center">

# 🏛️ CivicQuest
### *Verify. Participate. Make Development Accountable.*

<p align="center">
  <b>An open-source citizen verification & community audit platform for public development works in India.</b><br />
  Connecting citizens, regional development datasets, independent community auditors, and verifiable civic rewards.
</p>

<p align="center">
  <a href="https://civicquest-backend.onrender.com/docs"><img src="https://img.shields.io/badge/API_Swagger-Docs-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="API Docs" /></a>
  <a href="https://civicquest-backend.onrender.com/map"><img src="https://img.shields.io/badge/Interactive-Folium_Map-199900?style=for-the-badge&logo=leaflet&logoColor=white" alt="National Map" /></a>
  <a href="https://civicquest-backend.onrender.com"><img src="https://img.shields.io/badge/Backend-Render-46E3B7?style=for-the-badge&logo=render&logoColor=white" alt="Backend on Render" /></a>
  <a href="https://vercel.com/"><img src="https://img.shields.io/badge/Frontend-Vercel-000000?style=for-the-badge&logo=vercel&logoColor=white" alt="Frontend on Vercel" /></a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Next.js-16.3-black?style=flat-square&logo=next.js&logoColor=white" alt="Next.js" />
  <img src="https://img.shields.io/badge/React-19.2-61DAFB?style=flat-square&logo=react&logoColor=black" alt="React" />
  <img src="https://img.shields.io/badge/TypeScript-5.0-3178C6?style=flat-square&logo=typescript&logoColor=white" alt="TypeScript" />
  <img src="https://img.shields.io/badge/Tailwind_CSS-v4-06B6D4?style=flat-square&logo=tailwindcss&logoColor=white" alt="Tailwind CSS" />
  <img src="https://img.shields.io/badge/FastAPI-0.115+-009688?style=flat-square&logo=fastapi&logoColor=white" alt="FastAPI" />
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/PostgreSQL-15+-4169E1?style=flat-square&logo=postgresql&logoColor=white" alt="PostgreSQL" />
  <img src="https://img.shields.io/badge/License-Not_Specified-lightgrey?style=flat-square" alt="License" />
</p>

<br />

<a href="#-overview">
  <img src="Frontend/public/images/quest-city.png" alt="CivicQuest Hero Illustration" width="820" style="border-radius: 14px; box-shadow: 0 12px 36px rgba(0,0,0,0.12);" />
</a>

<br /><br />

<!-- QUICK STATS BANNER -->
| 🏛️ **35,293** | 📍 **504** | 🇮🇳 **35** | ⚡ **+150 XP** | 📜 **PDF Awards** |
|:---:|:---:|:---:|:---:|:---:|
| **Imported Works** | **Constituency Hubs** | **States & UTs Covered** | **Per Approved Quest** | **Verifiable Certificates** |

<br />

<p align="center">
  <a href="#-overview">Overview</a> •
  <a href="#-key-features">Features</a> •
  <a href="#-system-architecture">Architecture</a> •
  <a href="#-interactive-mplads-map">Interactive Map</a> •
  <a href="#-auditor-review-workflow">Auditor Flow</a> •
  <a href="#-current-dataset--statistics">Dataset</a> •
  <a href="#-local-development-setup">Local Setup</a> •
  <a href="#-api-documentation">API Reference</a>
</p>

</div>

---

## 🚀 Overview

**CivicQuest** is a civic-tech verification platform built to democratize transparency and ground-level accountability around **MPLADS** (*Members of Parliament Local Area Development Scheme*) development works.

While public expenditure dashboards publish thousands of completed works, citizens historically lacked an intuitive, map-centric interface to locate these assets, inspect their ground reality, and report on their operational condition.

CivicQuest creates a closed-loop civic audit ecosystem:
1. **Explore:** Citizens discover local development works on an interactive map filtered by state, constituency, and category.
2. **Inspect & Submit:** Citizens visit the site, record GPS proximity, photograph the asset, and submit observations (*Completed*, *Ongoing*, or *Not done*).
3. **Moderate & Audit:** Authorized Community Auditors review photo evidence and location telemetry in a dedicated queue, approving genuine work or rejecting with mandatory feedback.
4. **Reward:** Approved inspections award experience points (XP), advance explorer levels, and unlock cryptographically coded PDF participation certificates.

---

## ✨ Project Types in Focus

CivicQuest covers diverse public infrastructure categories funded through parliamentary development grants:

<table>
  <tr>
    <td width="33%" align="center" valign="top">
      <img src="Frontend/public/images/community-hall.png" width="100%" alt="Community Halls" style="border-radius: 10px;" />
      <br /><br />
      <b>🏛️ Community & Learning Centers</b>
      <p><sub>Community halls, skill centers, public libraries, and school buildings designed for collective neighborhood use.</sub></p>
    </td>
    <td width="33%" align="center" valign="top">
      <img src="Frontend/public/images/neighborhood-park.png" width="100%" alt="Public Parks" style="border-radius: 10px;" />
      <br /><br />
      <b>🌳 Parks & Green Spaces</b>
      <p><sub>Neighborhood parks, walking paths, children's playgrounds, and open gyms promoting urban wellness.</sub></p>
    </td>
    <td width="33%" align="center" valign="top">
      <img src="Frontend/public/images/quest-city.png" width="100%" alt="Civic Infrastructure" style="border-radius: 10px;" />
      <br /><br />
      <b>🚧 Essential Civil Utilities</b>
      <p><sub>Drinking water points, street lighting installations, paved footpaths, drainage networks, and bus shelters.</sub></p>
    </td>
  </tr>
</table>

---

## 💡 Why CivicQuest?

```
TRADITIONAL PROCESS                          CIVICQUEST MODEL
┌──────────────────────────────┐             ┌──────────────────────────────┐
│  Opaque Public Data Tables   │             │  🗺️ Interactive Visual Map   │
│  Infrequent Official Audits  │    VS       │  📸 Citizen Field Evidence   │
│  Unverified Public Feedback  │             │  🔎 Structured Auditor Desk  │
│  Zero Citizen Recognition    │             │  🏆 Gamified XP & Certs      │
└──────────────────────────────┘             └──────────────────────────────┘
```

- **Bridging the Information Gap:** Transforms raw, tabular spreadsheets into an interactive spatial map accessible to any constituent with a smartphone or browser.
- **Independent Ground-Truthing:** Encourages on-site citizen observations to verify if public funds translated into functional assets.
- **Auditor Moderation Queue:** Eliminates spam, arbitrary claims, and non-site uploads through a structured review workflow requiring explicit approval or reasoned rejection.
- **Sustaining Civic Motivation:** Replaces dry bureaucratic portals with an engaging civic quest loop featuring levels, badges, a national leaderboard, and downloadable certificates.

---

## 🌐 Current Live Deployment

CivicQuest is deployed in a decoupled cloud architecture:

| Component | Platform | Direct Endpoint / Status | Purpose |
|---|---|---|---|
| **Backend REST API** | [Render](https://render.com) | [`https://civicquest-backend.onrender.com`](https://civicquest-backend.onrender.com) | Production FastAPI application server |
| **Interactive OpenAPI Docs** | Render (Swagger) | [`https://civicquest-backend.onrender.com/docs`](https://civicquest-backend.onrender.com/docs) | Interactive Swagger UI API playground |
| **Alternative Docs** | Render (ReDoc) | [`https://civicquest-backend.onrender.com/redoc`](https://civicquest-backend.onrender.com/redoc) | Clean developer reference documentation |
| **National Folium Map** | Render (Static HTML) | [`https://civicquest-backend.onrender.com/map`](https://civicquest-backend.onrender.com/map) | Full 504-constituency clustered map |
| **Database** | Render PostgreSQL | Managed PostgreSQL 15+ instance | Primary relational data store |
| **Frontend Web App** | [Vercel](https://vercel.com) | *Deployed on Vercel* | Next.js 16 App Router interface |

> [!NOTE]
> The backend root endpoint (`GET /`) provides a health check returning the platform status, online state, documentation paths, and active version (`1.0.0`).

---

## 🏗️ System Architecture

CivicQuest separates client presentation, business logic, geospatial resolution, and data persistence:

```mermaid
flowchart TD
    classDef client fill:#e0f2fe,stroke:#0284c7,stroke-width:2px,color:#0369a1;
    classDef api fill:#ecfdf5,stroke:#059669,stroke-width:2px,color:#047857;
    classDef svc fill:#fef3c7,stroke:#d97706,stroke-width:2px,color:#b45309;
    classDef storage fill:#ede9fe,stroke:#7c3aed,stroke-width:2px,color:#6d28d9;

    subgraph ClientLayer["🖥️ Frontend Clients (Next.js 16 / React 19 / Vercel)"]
        CitizenView["👤 Citizen Explorer\n• Map Discovery\n• Evidence Dialog\n• Quest Journal"]:::client
        AuditorView["🔎 Auditor Desk\n• Review Inbox\n• Photo Inspector\n• Decision Modal"]:::client
        AdminView["🛡️ Admin Panel\n• Metrics Overview\n• User Role Manager\n• Batch Ingestion"]:::client
    end

    subgraph APILayer["⚡ REST Gateway & Security (FastAPI / Render)"]
        Gateway["FastAPI Application (app.main)\n• CORS Middleware\n• Bearer JWT Auth (PyJWT)\n• RBAC Dependency Guards"]:::api
        Endpoints["Routers:\n/api/auth · /api/projects · /api/submissions\n/api/audits · /api/certificates · /api/leaderboard\n/api/notifications · /api/admin"]:::api
    end

    subgraph ServiceLayer["⚙️ Core Services & Geospatial Processing"]
        GeoService["Geocoding & GPS Engine\n• Haversine Calculation\n• Nominatim Geocoding\n• Persistent Cache"]:::svc
        CertService["Certificate Engine\n• ReportLab PDF Stamping\n• Cryptographic Code Hash"]:::svc
        CSVEngine["Pandas Ingestion Stream\n• Chunked Reader (1k rows)\n• Priority Coordinate Guard"]:::svc
        MapEngine["Folium Map Builder\n• 504 Constituency Centroids\n• FastMarkerCluster Layer"]:::svc
    end

    subgraph StorageLayer["💾 Persistence & File Storage"]
        DB[("🐘 PostgreSQL 15+\nUsers · Projects · Submissions\nAudit Records · Notifications\nCertificates · Location Cache")]:::storage
        Uploads["📁 /uploads Disk Storage\n(Sanitized Evidence Images)"]:::storage
        Dataset["📊 Geospatial Assets\nWorks Completed.csv\nconstituency_centroids.json"]:::storage
    end

    CitizenView -->|HTTP Requests / Multipart| Gateway
    AuditorView -->|HTTP Requests| Gateway
    AdminView -->|HTTP Requests| Gateway

    Gateway --> Endpoints
    Endpoints --> GeoService
    Endpoints --> CertService
    Endpoints --> CSVEngine
    Endpoints --> MapEngine

    Endpoints -->|SQLAlchemy 2.0 ORM| DB
    Endpoints -->|Pillow Verified Write| Uploads
    CSVEngine -->|Reads| Dataset
    MapEngine -->|Reads| Dataset
```

---

## 🔄 End-to-End Application Workflow

The step-by-step lifecycle of an MPLADS project verification:

```mermaid
sequenceDiagram
    autonumber
    actor Citizen as 👤 Citizen Explorer
    participant UI as 💻 Next.js Client
    participant API as ⚡ FastAPI Server
    participant DB as 🐘 PostgreSQL
    actor Auditor as 🔎 Community Auditor

    Note over API,DB: Background: 35k+ works imported, 504 constituency hubs mapped.
    
    Citizen->>UI: Discovers work on map and opens Quest modal
    UI->>API: GET /api/projects/{id}
    API-->>UI: Project record & reference location
    
    Citizen->>UI: Captures photo, records GPS check-in & observation notes
    UI->>UI: Canvas compresses photo & evaluates proximity
    Citizen->>UI: Submits verification
    UI->>API: POST /api/submissions (Multipart FormData)
    
    rect rgb(240, 249, 255)
        Note over API,DB: Server-side Security & Ingestion
        API->>API: Pillow validates image binary format & dimensions
        API->>API: Haversine verifies distance & sets GPS status
        API->>DB: Saves submission with status PENDING
        API->>DB: Emits SUBMISSION_RECEIVED notification
    end
    API-->>UI: Returns confirmation (Status: PENDING)
    
    Auditor->>UI: Opens Auditor Workspace
    UI->>API: GET /api/audits/pending (Restricted to AUDITOR / ADMIN)
    API-->>UI: Pending evidence queue
    
    Auditor->>UI: Examines photo, field notes, and GPS proximity status
    
    alt Approved by Auditor
        Auditor->>UI: Confirms inspection & clicks Approve
        UI->>API: POST /api/audits/{id}/approve
        rect rgb(240, 253, 244)
            Note over API,DB: Atomic Approval Transaction
            API->>DB: Mark APPROVED & log AuditRecord
            API->>DB: Award +150 XP to citizen (deduplicated per project)
            API->>DB: Recalculate level: (XP // 450) + 1
            API->>DB: Milestone check: if approved >= 5, issue Certificate
            API->>DB: Emit SUBMISSION_APPROVED notification
        end
        API-->>UI: Approval recorded
    else Rejected by Auditor
        Auditor->>UI: Enters mandatory rejection reason (>= 5 chars)
        UI->>API: POST /api/audits/{id}/reject
        rect rgb(254, 242, 242)
            API->>DB: Mark REJECTED, log reason, award 0 XP
            API->>DB: Emit SUBMISSION_REJECTED notification
        end
        API-->>UI: Rejection recorded
    end
    
    Citizen->>UI: Opens Adventure Log & Notifications
    UI->>API: GET /api/notifications & GET /api/certificates
    API-->>UI: Updated XP, next quest level & PDF certificate download link
```

---

## 👥 User Roles & Access Control

CivicQuest implements strict **Role-Based Access Control (RBAC)** enforced at the database and dependency levels:

<div align="center">

| Role | Badge | Permissions & Platform Scope |
|:---:|:---:|---|
| **Citizen** | `USER` | • Search & explore public works on map & catalog<br />• Submit site evidence (photo, GPS check-in, notes)<br />• Track personal adventure log & notification feed<br />• Compete on public leaderboard & download earned certificates |
| **Community Auditor** | `AUDITOR` | • Inherits all Citizen capabilities<br />• Access protected `/api/audits/pending` review queue<br />• Inspect submitted photos & location authenticity<br />• Approve submissions (+150 XP) or reject with mandatory feedback |
| **Administrator** | `ADMIN` | • Inherits all Auditor & Citizen capabilities<br />• Monitor platform-wide metrics & review volumes via `/api/admin/stats`<br />• User management: promote/demote user roles via `/api/admin/users`<br />• Trigger batch CSV dataset ingestion jobs |

</div>

### Access Control Highlights
- **Public Signup Safety:** Public registration (`POST /api/auth/register`) strictly sets `role = "USER"`. It is architecturally impossible to self-register as an Auditor or Admin.
- **Server-Side Enforcement:** Route protection relies on FastAPI's `require_role(*allowed_roles)` dependency which verifies decoded JWT claims. Unauthorized requests receive `403 Forbidden`.

---

## 🗺️ Interactive MPLADS Map

Mapping over 35,000 works across India requires a balance of visual clarity, responsiveness, and geographical honesty. CivicQuest uses a dual-engine approach:

<table>
  <tr>
    <td width="50%" valign="top">
      <h4>📱 1. Client-Side Explorer Map</h4>
      <ul>
        <li><b>Library:</b> React-Leaflet 5 + Leaflet 1.9.4</li>
        <li><b>Tile Layer:</b> CARTO Voyager & OpenStreetMap</li>
        <li><b>Bounds:</b> Framed to Indian territory (<code>[6.5, 68.0]</code> to <code>[36.0, 97.5]</code>)</li>
        <li><b>Navigation:</b> Smooth fly-to animations on work selection and state filter changes</li>
        <li><b>Proximity:</b> Browser HTML5 Geolocation with "Near Me" search</li>
      </ul>
    </td>
    <td width="50%" valign="top">
      <h4>🌐 2. National Overview Folium Map</h4>
      <ul>
        <li><b>Library:</b> Folium 0.17.0 (Python)</li>
        <li><b>Hub Aggregation:</b> 504 Parliamentary Constituency Centroids</li>
        <li><b>Hub Popups:</b> Card view showing MP name, completed works count, and disbursed funds</li>
        <li><b>Clustering:</b> FastMarkerCluster layer capable of rendering 35,292 individual work markers simultaneously</li>
        <li><b>Direct URL:</b> <a href="https://civicquest-backend.onrender.com/map"><code>/map</code></a></li>
      </ul>
    </td>
  </tr>
</table>

---

> [!IMPORTANT]
> ### ⚠️ Coordinate Resolution & Geolocation Transparency
> 
> The official raw MPLADS government records identify works by State, Parliamentary Constituency, and Implementing Agency, but do **not** provide exact sub-meter GPS survey coordinates for individual physical work gates.
> 
> CivicQuest implements a transparent coordinate resolution hierarchy:
> 
> ```
> [Exact Coordinates in Data] ──► Priority 1: EXACT_DATASET (Exact)
>             │ (if missing)
>             ▼
> [Constituency Centroids]   ──► Priority 2: APPROXIMATE / CONSTITUENCY_CENTROID
>             │ (if missing)
>             ▼
> [District/City Centroids]  ──► Priority 3: APPROXIMATE / DISTRICT_CENTROID
>             │ (if missing)
>             ▼
> [Unresolved]               ──► Priority 4: MISSING (Never fabricated)
> ```
> 
> **Impact on GPS Verification:**
> Because most works currently reference the **Parliamentary Constituency Centroid**, the GPS verification engine tags checks against these records as **`LIMITED`**. The platform explicitly discloses to both citizen and auditor that proximity to a constituency centroid confirms regional presence, but cannot definitively prove physical attendance at the sub-constituency physical job site.

---

## 📸 Citizen Verification & Evidence System

The evidence submission modal (`evidence-dialog.tsx`) applies multi-stage anti-fraud validation:

```
[Camera / File Input] ──► [Canvas Downsampling] ──► [GPS Haversine Check] ──► [Server Pillow Verify] ──► [PENDING Queue]
```

1. **Client-Side Image Optimization:** Accepts JPG, PNG, and WebP files up to 8 MB. Automatically downscales large images on an HTML5 canvas (maximum 1600px dimension, 0.86 quality JPEG) to save mobile data.
2. **Server-Side File Sanitization:** Raw bytes are verified using Python **Pillow** (`Image.open().verify()`) to confirm structural integrity and prevent malicious payload execution. Files are written to disk using collision-free UUIDs (`/uploads/<uuid>.jpg`).
3. **Observation Categorization:** Citizens classify physical progress as `Completed`, `Ongoing`, or `Not done`, accompanied by mandatory field notes ($\ge 10$ characters).
4. **Haversine Proximity Engine:** Evaluates distance between citizen coordinates and the recorded project location using the spherical earth radius ($R = 6,371,000\text{ m}$):
   - **`VERIFIED`:** Within 200 meters of an exact site coordinate.
   - **`LIMITED`:** Project coordinates are constituency-level centroids.
   - **`UNVERIFIED`:** Citizen is outside 200 meters of an exact site coordinate.
   - **`SIMULATED`:** Designated simulated visit for demonstration and testing.

---

## 🔍 Auditor Review Workflow

The Auditor workspace (`auditor-view.tsx`) provides an interface for evidence moderation:

<div align="center">

```
┌────────────────────────────────────────────────────────────────────────┐
│                        AUDITOR WORKSPACE                               │
├────────────────────────────────────────────────────────────────────────┤
│  [Review Queue: 12 Pending]                  [Toggle: Pending / All]   │
│                                                                        │
│  ┌────────────┐   Indiranagar Community Hall                           │
│  │   PHOTO    │   Observation: Completed                               │
│  │ EVIDENCE   │   GPS: Limited (Constituency Centroid) · ±15 m         │
│  └────────────┘   Notes: Building complete, accessibility ramp open.   │
│                                                                        │
│  [✓] I have verified the image and check-in details.                   │
│                                                                        │
│  [  ✅ APPROVE (+150 XP)  ]     [  ❌ REJECT (Requires Feedback)  ]     │
└────────────────────────────────────────────────────────────────────────┘
```

</div>

- **Mandatory Review Gate:** The auditor must confirm inspection via a dedicated checkbox before decision buttons are enabled.
- **Accountable Rejections:** Rejection requires an explanatory reason of at least 5 characters sent directly to the citizen's notification inbox.
- **One-Reward Guarantee:** Citizens can only receive XP once per unique project, preventing repetitive reward farming.

---

## 🏆 Gamification: XP, Levels & Certificates

CivicQuest balances civic duty with an encouraging, transparent progression system:

### 1. Predictable XP Scaling
- **+150 XP** awarded for every approved verification.
- Rejected or unreviewed submissions grant **0 XP**.

### 2. Explorer Levels
Progress calculates automatically from total verified XP:
$$\text{Level} = \left\lfloor\frac{\text{XP}}{450}\right\rfloor + 1$$
Every 3 approved verifications advance the citizen to the next rank.

### 3. Achievement Badges

<div align="center">

| Badge | Icon | Milestone | Rank Name | Description |
|---|:---:|:---:|:---:|---|
| **First Steps** | 🧭 | 1 Approved | *Curious Citizen* | Completed your first verified field inspection. |
| **Local Legend** | 🛡️ | 3 Approved | *Community Scout* | Demonstrated repeated neighborhood engagement. |
| **Changemaker** | 🏆 | 5 Approved | *Civic Auditor* | Unlocks official Participation Certificate. |

</div>

### 4. Official Participation Certificate (PDF)
Upon reaching **5 approved verifications** (`CERTIFICATE_THRESHOLD = 5`), the backend issues an official vector PDF certificate:
- **Engine:** Programmatically generated on-the-fly using **ReportLab**.
- **Security:** Features an individual certificate verification code (`CIVICQUEST-{user_id:04d}-{uuid}`).
- **Format:** Landscape presentation with formal seal, issue date, approved count, and civic disclaimer.
- **Download:** Available via `GET /api/certificates/{id}/download`.

---

## 📊 Current Dataset & Statistics

CivicQuest includes an imported MPLADS dataset containing real development works across India:

```
┌─────────────────────────────────────────────────────────────────┐
│                 CURRENT INGESTION STATISTICS                    │
├────────────────────────────────┬────────────────────────────────┤
│ Metric                         │ Value                          │
├────────────────────────────────┼────────────────────────────────┤
│ Total Processed Rows           │ 35,293                         │
│ New Records Inserted           │ 35,283                         │
│ Existing Records Updated       │ 10                             │
│ Parliamentary Constituencies   │ 504                            │
│ States & Union Territories     │ 35                             │
│ Primary Work Categories        │ Infrastructure, Education,     │
│                                │ Community, Parks, Health       │
│ Source File                    │ Works Completed.csv (11.2 MB)  │
└────────────────────────────────┴────────────────────────────────┘
```

> [!NOTE]
> These figures represent records successfully imported and verified within the CivicQuest local database instance, rather than the exhaustive sum of all historical works nationwide.

---

## 🛠️ Technology Stack

<div align="center">

| Category | Technology | Version | Purpose |
|---|---|---|---|
| **Frontend Framework** | [Next.js](https://nextjs.org/) | `16.3.4` | App Router architecture, SSR, font optimization |
| **Frontend Library** | [React](https://react.dev/) | `19.2.8` | Component state and user interface rendering |
| **Language** | [TypeScript](https://www.typescriptlang.org/) | `5.x` | Strict type safety across client interfaces |
| **Styling** | [Tailwind CSS](https://tailwindcss.com/) | `v4` | Modern utility styling and responsive token system |
| **UI Primitives** | [Base-UI](https://base-ui.com/) / Radix | `^1.8.0` | Accessible dialogs, toggles, badges, and progress bars |
| **Icons** | [Lucide React](https://lucide.dev/) | `^1.45.0` | Clean, modern iconography |
| **Notifications** | [Sonner](https://sonner.emilkowal.ski/) | `^2.0.8` | Non-blocking toast notifications |
| **Client Mapping** | [Leaflet](https://leafletjs.com/) + [React-Leaflet](https://react-leaflet.js.org/) | `1.9.4` / `5.0` | Dynamic client-side interactive map visualization |
| **Map Tiles** | CARTO Voyager + OpenStreetMap | Open | Open-source, zero-cost map tile layers |
| **Backend Framework** | [FastAPI](https://fastapi.tiangolo.com/) | `>=0.115.0` | High-throughput asynchronous REST API |
| **ASGI Server** | [Uvicorn](https://www.uvicorn.org/) | `>=0.30.0` | High-performance ASGI production server |
| **Database** | [PostgreSQL](https://www.postgresql.org/) | `15+` | Relational database engine |
| **Database Driver** | [psycopg](https://www.psycopg.org/) (Binary) | `>=3.2.0` | Native, thread-safe PostgreSQL driver |
| **ORM** | [SQLAlchemy](https://www.sqlalchemy.org/) | `>=2.0.30` | Declarative object-relational mapping |
| **Data Validation** | [Pydantic](https://docs.pydantic.dev/) | `>=2.7.0` | Strict schema validation and settings management |
| **Authentication** | [PyJWT](https://pyjwt.readthedocs.io/) + [bcrypt](https://github.com/pyca/bcrypt/) | `2.9` / `4.2` | Signed HS256 JWT tokens and salted password hashes |
| **Image Verification** | [Pillow](https://python-pillow.org/) | `>=10.4.0` | Server-side image decoding and header sanitization |
| **Geospatial Engine** | [Geopy](https://geopy.readthedocs.io/) | `>=2.4.1` | Nominatim geocoding client with rate-limiting and cache |
| **Static Mapping** | [Folium](https://python-visualization.github.io/folium/) | `>=0.17.0` | Marker cluster and constituency hub HTML generator |
| **Data Ingestion** | [Pandas](https://pandas.pydata.org/) | `>=2.0.0` | High-performance chunked CSV stream processing |
| **PDF Generation** | [ReportLab](https://www.reportlab.com/) | `>=4.2.2` | Programmatic vector PDF certificate compilation |

</div>

---

## 📁 Project Directory Structure

```text
CivicQuest/
├── Backend/
│   ├── app/
│   │   ├── auth.py                   # bcrypt hashing & PyJWT token utilities
│   │   ├── config.py                 # Pydantic BaseSettings & environment loader
│   │   ├── database.py               # SQLAlchemy engine, session maker & base
│   │   ├── dependencies.py           # HTTPBearer authentication & require_role()
│   │   ├── main.py                   # FastAPI app declaration, CORS & startup seed
│   │   ├── models.py                 # SQLAlchemy relational ORM models (7 entities)
│   │   ├── schemas.py                # Pydantic validation schemas (In/Out/DTOs)
│   │   ├── routers/
│   │   │   ├── admin.py              # Platform metrics, user roles & CSV trigger
│   │   │   ├── audits.py             # Auditor review queue, approval & rejection
│   │   │   ├── auth.py               # Signup, login & profile endpoints
│   │   │   ├── certificates.py       # Certificate listings & PDF download stream
│   │   │   ├── leaderboard.py        # Citizen XP rankings from real database
│   │   │   ├── notifications.py      # User in-app notification feed & read status
│   │   │   ├── projects.py           # Projects search, filters, nearby & map endpoints
│   │   │   └── submissions.py        # Photo upload, GPS validation & quest creation
│   │   └── services/
│   │       ├── certificates.py       # ReportLab PDF certificate canvas builder
│   │       ├── csv_import.py         # Streaming Pandas CSV batch synchronizer
│   │       ├── geocoding.py          # Haversine distance, GPS check & Nominatim
│   │       └── map_generator.py      # Folium standalone map builder with clusters
│   ├── data/
│   │   ├── Works Completed.csv       # Full MPLADS dataset (11.2 MB)
│   │   ├── constituency_centroids.json # 543 Constituency reference coordinates
│   │   └── works_map.html            # Precompiled Folium interactive map
│   ├── scripts/
│   │   ├── generate_folium_map.py    # Standalone script to compile Folium map
│   │   ├── import_csv.py             # CLI utility for chunked dataset imports
│   │   ├── seed_db.py                # Script to seed default Admin & Auditor accounts
│   │   └── test_api.py               # 12-step automated integration test suite
│   ├── uploads/                      # Storage directory for verified citizen evidence
│   ├── requirements.txt              # Pinned Python package dependencies
│   └── README.md                     # Backend-specific notes
│
├── Frontend/
│   ├── app/
│   │   ├── globals.css               # Design system tokens, variables & animations
│   │   ├── layout.tsx                # Root layout with Geist & Plus Jakarta Sans
│   │   └── page.tsx                  # Home entry point mounting CivicQuest shell
│   ├── components/
│   │   ├── ui/                       # Base-UI / Shadcn accessible UI primitives
│   │   ├── admin-view.tsx            # Admin dashboard, stats cards & user table
│   │   ├── auditor-view.tsx          # Auditor workspace & evidence moderation modal
│   │   ├── civic-quest.tsx           # Primary application container & tab router
│   │   ├── evidence-dialog.tsx       # Photo upload, camera compression & GPS check-in
│   │   ├── explore-view.tsx          # Project catalog, state filters & search bar
│   │   ├── progression.tsx           # XP bar, weekly quest, badges & leaderboard
│   │   └── project-map.tsx           # React-Leaflet interactive map with India bounds
│   ├── lib/
│   │   ├── api.ts                    # Complete client-side fetch client for FastAPI
│   │   ├── auth-context.tsx          # Global authentication state provider
│   │   └── demo-data.ts              # Fallback demonstration project stubs
│   ├── public/
│   │   ├── images/
│   │   │   ├── community-hall.png    # Illustrative asset for community projects
│   │   │   ├── neighborhood-park.png # Illustrative asset for park projects
│   │   │   └── quest-city.png        # Playful civic neighborhood hero graphic
│   │   └── works_map.html            # Static mirror of the Folium map
│   ├── package.json                  # Pinned npm/pnpm dependencies (pnpm@10.34.3)
│   ├── pnpm-lock.yaml                # pnpm lockfile
│   └── tsconfig.json                 # Strict TypeScript configuration
│
├── scripts/
│   └── test_auth_map.py              # End-to-end HTTP verification script
├── Works Completed.csv               # Root MPLADS source dataset
├── run.bat                           # Windows batch launcher (starts Backend & Frontend)
├── run.ps1                           # PowerShell launcher (starts both servers)
├── stop.bat                          # Batch shutdown script for local dev ports
├── stop.ps1                          # PowerShell script to terminate dev servers
└── README.md                         # Root repository documentation
```

---

## ⚙️ Environment Variables

### Backend Configuration (`Backend/.env`)
Create `Backend/.env` (or copy from `Backend/.env.example`):

```env
DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5432/civicquest
JWT_SECRET=your_super_secret_high_entropy_random_key_here
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
UPLOAD_DIR=uploads
DATA_CSV_PATH=data/works_completed.csv
```

### Frontend Configuration (`Frontend/.env.local`)
Create `Frontend/.env.local`:

```env
# Point to local FastAPI server during development:
NEXT_PUBLIC_API_URL=http://localhost:8000

# Or point to deployed production backend:
# NEXT_PUBLIC_API_URL=https://civicquest-backend.onrender.com
```

---

## 💻 Local Development Setup

### Prerequisites
- **Python 3.10+** (Tested on Python 3.14)
- **Node.js 20+**
- **pnpm** (Configured via `pnpm@10.34.3`) or **npm**
- **PostgreSQL 15+** *(Optional: fallback to SQLite supported for local evaluation)*

---

### Option 1: One-Click Quickstart (Windows)

Launch both the backend and frontend development servers in separate windows:

```powershell
# Using PowerShell:
.\run.ps1

# Or using Command Prompt:
run.bat
```

To stop all running development servers:
```powershell
.\stop.ps1
# or:
stop.bat
```

---

### Option 2: Step-by-Step Manual Setup

#### 1. Backend Service
```bash
# Navigate to the backend directory
cd Backend

# Create and activate a Python virtual environment
python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Initialize database tables and seed default accounts
python scripts/seed_db.py

# Import MPLADS works dataset (use --limit 200 for fast testing, or omit for all 35,293)
python scripts/import_csv.py --limit 200

# Launch FastAPI development server
uvicorn app.main:app --port 8000 --reload
```

#### Default Development Accounts
The seeder (`scripts/seed_db.py`) creates two pre-configured accounts:

| Role | Email | Password | Scope |
|---|---|---|---|
| **Administrator** | `admin@gg` | `admin` | Admin dashboard, user promotions, platform metrics |
| **Community Auditor** | `auditor@gg` | `auditor` | Audit queue, evidence approval/rejection |

*(Citizens can register new accounts freely via the frontend interface)*

#### 2. Frontend Web Client
Open a second terminal window:

```bash
# Navigate to the frontend directory
cd Frontend

# Install packages (pnpm is the primary configured package manager)
pnpm install
# (or with npm: npm install)

# Start Next.js development server
pnpm dev
# (or with npm: npm run dev)
```

Open [`http://localhost:3000`](http://localhost:3000) in your browser.

---

## 📡 API Documentation

FastAPI automatically generates interactive OpenAPI documentation:

<div align="center">

👉 **[Open Interactive Swagger UI (Live)](https://civicquest-backend.onrender.com/docs)** 👈

</div>

<br />

```
CivicQuest REST API
├── /api/auth
│   ├── POST   /register             Citizen signup (enforces role=USER)
│   ├── POST   /login                Authenticates user & returns signed JWT
│   └── GET    /me                   Returns current authenticated profile
│
├── /api/projects
│   ├── GET    /                     Filterable public works catalog
│   ├── GET    /summary-stats        Platform aggregate metrics
│   ├── GET    /states               Available states with project counts
│   ├── GET    /nearby               Haversine proximity radius search
│   ├── GET    /map-hubs             Aggregated constituency hubs for map
│   ├── GET    /map-works            Lightweight coordinate list for map
│   └── GET    /{id}                 Detailed work metadata
│
├── /api/submissions
│   ├── POST   /                     Submit site evidence (photo + observation)
│   └── GET    /my                   Logged-in citizen's personal quests
│
├── /api/audits
│   ├── GET    /pending              Review queue of unmoderated verifications
│   ├── GET    /history              Log of past auditor decisions
│   ├── POST   /{id}/approve         Approves evidence, awards +150 XP, checks cert
│   └── POST   /{id}/reject          Rejects evidence with mandatory feedback
│
├── /api/certificates
│   ├── GET    /                     Citizen's unlocked participation certificates
│   └── GET    /{id}/download        Streams generated ReportLab PDF certificate
│
├── /api/leaderboard
│   └── GET    /                     Ranked citizen leaderboard by XP
│
├── /api/notifications
│   ├── GET    /                     User notification inbox
│   └── PATCH  /{id}/read            Marks specific notification as read
│
└── /api/admin
    ├── GET    /stats                Comprehensive platform analytics
    ├── GET    /users                User directory with role filtering
    ├── PATCH  /users/{id}           Promote/demote user permissions
    ├── GET    /submissions          Global submissions oversight
    └── POST   /import-csv           Triggers chunked dataset ingestion
```

---

## 🧪 Testing & Quality Assurance

CivicQuest includes an automated test suite verifying core API behaviors and security boundaries.

### Run Backend Integration Tests
```bash
python Backend/scripts/test_api.py
```

The integration suite tests **12 core assertions** end-to-end:
1. `GET /` platform health check
2. Administrator login & JWT generation
3. Auditor login & JWT generation
4. Citizen registration (`role = "USER"` constraint)
5. RBAC security: verifies `403 Forbidden` when Citizens attempt to access auditor/admin routes
6. Project catalog queries and location metadata parsing
7. Multi-part citizen evidence upload with binary JPEG simulation
8. In-app notification creation for the citizen
9. Auditor approval workflow and feedback logging
10. XP calculation (+150 XP atomic increment) and level recalculation
11. Real-time leaderboard indexing of verified citizens
12. Platform administrative metric aggregations

### Run Live HTTP Endpoint Verification
```bash
python scripts/test_auth_map.py
```

---

## 🛡️ Security Architecture

- **Password Protection:** Plaintext passwords are never saved. Passwords are salted and hashed using **bcrypt** before database writes.
- **Stateless JWT Authorization:** API routes inspect signed JSON Web Tokens using HS256. Expired or forged tokens receive immediate HTTP 401 Unauthorized responses.
- **Strict Origin Isolation (CORS):** The backend restricts `Access-Control-Allow-Origin` strictly to authorized hostnames configured in `CORS_ORIGINS`.
- **Binary Image Verification:** Uploaded files undergo MIME-type checks and deep binary header verification using Pillow (`Image.open().verify()`) to prevent arbitrary file execution.
- **Disk Write Sanitization:** Filenames are replaced with cryptographic UUIDs (`uuid.uuid4().hex`) and constrained to allowed extensions (`.jpg`, `.jpeg`, `.png`, `.webp`), eliminating path traversal vulnerabilities.
- **HTTP Security Headers:** Next.js enforces defense-in-depth headers:
  - `X-Content-Type-Options: nosniff`
  - `Referrer-Policy: strict-origin-when-cross-origin`
  - `Strict-Transport-Security: max-age=63072000`
  - `Permissions-Policy: camera=(self), geolocation=(self)`

---

## 🗺️ Future Roadmap

- [ ] **Project-Level Georeferencing:** Transition beyond constituency centroids by partnering with local ward offices and open mapping communities to capture sub-meter site boundaries.
- [ ] **AI-Assisted Photo Pre-Moderation:** Integrate lightweight computer vision models to flag non-site photos (e.g., self-portraits, memes, blank shots) before they reach human auditors.
- [ ] **Progressive Web App (PWA) / Offline Mode:** Enable field inspectors to cache project details locally, record photos and GPS coordinates offline, and sync automatically once connectivity is restored.
- [ ] **Public Regional Dashboards:** Dedicated constituency analytics showing completion rates, fund utilization, and citizen inspection coverage per Member of Parliament.
- [ ] **Multi-Language Localization:** Provide local language interfaces across Hindi, Kannada, Tamil, Bengali, Marathi, and other regional languages.
- [ ] **Tamper-Resistant Photo Metadata:** Extract and cross-verify EXIF timestamp and sensor metadata directly from field camera hardware.

---

## 🤝 Contributing

Contributions to CivicQuest are welcome!

1. **Fork the repository** on GitHub.
2. **Create a feature branch:**
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Commit your changes:**
   ```bash
   git commit -m "feat: Add constituency geographic boundary filters"
   ```
4. **Push to your branch:**
   ```bash
   git push origin feature/your-feature-name
   ```
5. **Open a Pull Request** describing your changes and testing steps.

---

## 📄 License

License information has not yet been specified.

---

<div align="center">
  <sub>Built with ❤️ for civic transparency, active citizen participation, and accountable public development.</sub>
</div>
