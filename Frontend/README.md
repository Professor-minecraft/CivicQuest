<div align="center">

# 🏛️ CivicQuest — Frontend Client
### *Citizen-Powered Verification for Public Development Works*

<p align="center">
  <b>The modern Next.js 16 web application powering the CivicQuest civic audit platform.</b><br />
  Enabling citizens to explore public works on interactive maps, upload ground-level evidence, and collaborate with community auditors.
</p>

<p align="center">
  <a href="https://civicquest-tau.vercel.app/"><img src="https://img.shields.io/badge/Live_Application-Vercel-000000?style=for-the-badge&logo=vercel&logoColor=white" alt="Live App on Vercel" /></a>
  <a href="https://civicquest-backend.onrender.com/docs"><img src="https://img.shields.io/badge/Backend_API-Render-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI Backend" /></a>
  <a href="https://civicquest-backend.onrender.com/map"><img src="https://img.shields.io/badge/National_Map-Folium-199900?style=for-the-badge&logo=leaflet&logoColor=white" alt="National Folium Map" /></a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Next.js-16.3.4-black?style=flat-square&logo=next.js&logoColor=white" alt="Next.js" />
  <img src="https://img.shields.io/badge/React-19.2.8-61DAFB?style=flat-square&logo=react&logoColor=black" alt="React" />
  <img src="https://img.shields.io/badge/TypeScript-5.x-3178C6?style=flat-square&logo=typescript&logoColor=white" alt="TypeScript" />
  <img src="https://img.shields.io/badge/Tailwind_CSS-v4-06B6D4?style=flat-square&logo=tailwindcss&logoColor=white" alt="Tailwind CSS" />
  <img src="https://img.shields.io/badge/Leaflet-1.9.4-199900?style=flat-square&logo=leaflet&logoColor=white" alt="Leaflet" />
  <img src="https://img.shields.io/badge/Package_Manager-pnpm_10-F69220?style=flat-square&logo=pnpm&logoColor=white" alt="pnpm" />
</p>

<br />

<div style="background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%); padding: 18px 24px; border-radius: 12px; margin: 12px 0; border: 1px solid #334155;">
  <span style="color: #38bdf8; font-size: 13px; font-weight: 700; letter-spacing: 1px; text-transform: uppercase;">🚀 Production Deployment</span><br />
  <span style="color: #ffffff; font-size: 18px; font-weight: 600;">Visit the live web app: </span>
  <a href="https://civicquest-tau.vercel.app/" style="color: #67e8f9; font-size: 18px; font-weight: 700; text-decoration: underline;">https://civicquest-tau.vercel.app/</a>
</div>

<br />

<p align="center">
  <a href="#-overview">Overview</a> •
  <a href="#-features">Features</a> •
  <a href="#-technology-stack">Tech Stack</a> •
  <a href="#-frontend-architecture">Architecture</a> •
  <a href="#-project-structure">Structure</a> •
  <a href="#-environment-variables">Environment</a> •
  <a href="#-local-development">Local Setup</a> •
  <a href="#-troubleshooting">Troubleshooting</a>
</p>

</div>

---

## 🚀 Overview

The **CivicQuest Frontend** is an intuitive, responsive web application designed to make public infrastructure tracking accessible and engaging. Built with **Next.js 16** and **React 19**, it transforms thousands of complex government records into an interactive geospatial experience where citizens actively participate in civic accountability.

### Core User Capabilities
- **Citizen Exploration:** Discover completed and ongoing public development works on an interactive map, search across parliamentary constituencies, and filter by work category.
- **Field Evidence Submission:** Capture real site photos, select observed operational status (*Completed*, *Ongoing*, or *Not done*), provide descriptive field notes, and check in via GPS telemetry.
- **Community Auditor Workspace:** Moderation desk where authorized community auditors inspect photo submissions, verify location authenticity, approve genuine verifications, or reject invalid claims with mandatory feedback.
- **Admin Governance:** Administrative dashboard providing platform-wide statistics, user role promotion/demotion, and dataset synchronization triggers.
- **Verified Progression:** An XP-driven engagement loop granting $+150\text{ XP}$ per approved verification, calculating explorer ranks, tracking milestone badges, and unlocking downloadable vector PDF certificates.

---

## ✨ Features

<div align="center">

| Feature Area | Description | Primary Component |
|---|---|---|
| **Interactive Map** | React-Leaflet map framed to Indian bounds with smooth fly-to navigation, layer controls, and HTML5 geolocation. | `components/project-map.tsx` |
| **Catalog & Filters** | Search works by keyword, filter by state/constituency, or query nearby projects within a 25 km radius. | `components/explore-view.tsx` |
| **Evidence Submission** | Photo capture modal with client-side canvas compression (1600px edge, JPEG 0.86) and GPS proximity validation. | `components/evidence-dialog.tsx` |
| **Auditor Review Desk** | Queue of pending citizen submissions with full-resolution photo inspection, field notes, and decision tools. | `components/auditor-view.tsx` |
| **Admin Panel** | Live platform metrics (total works, pending audits, users), role management, and CSV ingestion trigger. | `components/admin-view.tsx` |
| **Explorer Progression** | Level calculation (`Level = XP // 450 + 1`), weekly quests, milestone badges, and live citizen leaderboard. | `components/progression.tsx` |
| **PDF Certificates** | Automatic unlocking and streaming download of verified participation certificates upon reaching 5 approved audits. | `lib/api.ts` $\rightarrow$ ReportLab |
| **Notification Center** | In-app notification feed tracking submission approvals, rejections, and certificate milestones. | `components/civic-quest.tsx` |

</div>

---

## 🛠️ Technology Stack

The frontend stack is selected for performance, accessibility, and modern developer ergonomics:

- **Framework:** [Next.js 16.3.4](https://nextjs.org/) (App Router with Turbopack readiness)
- **Library:** [React 19.2.8](https://react.dev/) & React-DOM `19.2.8`
- **Language:** [TypeScript 5](https://www.typescriptlang.org/) for complete static type safety
- **Styling:** [Tailwind CSS v4](https://tailwindcss.com/) with `@tailwindcss/postcss` and `tw-animate-css`
- **Typography:** Next.js Google Fonts (`Geist` for body, `Plus Jakarta Sans` for headings)
- **Mapping:** [Leaflet 1.9.4](https://leafletjs.com/) and [React-Leaflet 5.0.0](https://react-leaflet.js.org/)
- **Map Tiles:** Open-source [CARTO Voyager](https://carto.com/basemaps/) and [OpenStreetMap](https://www.openstreetmap.org/)
- **Icons:** [Lucide React 1.45.0](https://lucide.dev/)
- **UI Primitives:** [@base-ui/react](https://base-ui.com/) and Shadcn-inspired accessible components
- **Feedback & Alerts:** [Sonner 2.0.8](https://sonner.emilkowal.ski/) toast notifications
- **Package Management:** [pnpm 10.34.3](https://pnpm.io/) (configured via `packageManager` field; npm compatible)

---

## 🏛️ Frontend Architecture

The client communicates with the deployed FastAPI backend via a centralized, typed HTTP service layer:

```
┌─────────────────────────────────────────────────────────────┐
│                    NEXT.JS 16 WEB CLIENT                    │
│                                                             │
│   ┌───────────────────┐               ┌─────────────────┐   │
│   │   app/page.tsx    │ ────────────► │ civic-quest.tsx │   │
│   └───────────────────┘               └────────┬────────┘   │
│                                                │            │
│         ┌──────────────────┬───────────────────┼────────────┴────────┐
│         ▼                  ▼                   ▼                     ▼
│  explore-view.tsx   evidence-dialog    auditor-view.tsx      admin-view.tsx
│  project-map.tsx    (Canvas Resize)    (Moderation Desk)     (Analytics/RBAC)
│         │                  │                   │                     │
│         └──────────────────┼───────────────────┴─────────────────────┘
│                            ▼
│                   lib/auth-context.tsx
│             (User State & Persistent Token)
│                            ▼
│                       lib/api.ts
│            (Typed Fetch API Client Layer)
└────────────────────────────┬────────────────────────────────┘
                             │  HTTP / Bearer Token / Multipart
                             ▼
         [ https://civicquest-backend.onrender.com ]
```

### Architectural Highlights

1. **Centralized API Client (`lib/api.ts`):**
   - Encapsulates all REST requests (`auth`, `projects`, `submissions`, `audits`, `leaderboard`, `notifications`, `certificates`, `admin`).
   - Automatically injects the stored JWT bearer token from `localStorage` into request headers via `getAuthHeader()`.
   - Defaults to the production Render backend when `NEXT_PUBLIC_API_URL` is omitted.

2. **Authentication State Provider (`lib/auth-context.tsx`):**
   - React Context managing the current `user` profile, active `token`, and loading states.
   - On page load, verifies the saved token against `GET /api/auth/me` to rehydrate the session.
   - Cleans up state and storage upon logout.

3. **Client-Side Image Optimization (`components/evidence-dialog.tsx`):**
   - Rather than uploading multi-megabyte raw photos directly from mobile cameras, an in-browser HTML5 `<canvas>` downsizes the image to a maximum edge of 1600px at 0.86 JPEG quality.
   - Saves client bandwidth and ensures fast uploads to the server.

4. **Dynamic Map Loading (`components/explore-view.tsx`):**
   - Leaflet requires browser window primitives and cannot execute during server-side rendering (SSR).
   - The map component is loaded dynamically with `{ ssr: false }` to prevent hydration mismatches while maintaining fast first-contentful paint.

---

## 📁 Project Structure

```text
Frontend/
├── app/
│   ├── favicon.ico             # Application icon
│   ├── globals.css             # Design tokens, variables, custom styles & animations
│   ├── layout.tsx              # Root HTML layout with Geist & Plus Jakarta Sans fonts
│   └── page.tsx                # Main entry point rendering <CivicQuest />
│
├── components/
│   ├── ui/                     # Accessible UI components (Shadcn / Base-UI)
│   │   ├── badge.tsx           # Status and category badges
│   │   ├── button.tsx          # Button variants and sizing
│   │   ├── dialog.tsx          # Accessible modal overlays
│   │   ├── field.tsx           # Form field layout helpers
│   │   ├── input.tsx           # Text input components
│   │   ├── label.tsx           # Form label elements
│   │   ├── progress.tsx        # Linear XP & quest progress bars
│   │   ├── separator.tsx       # Visual divider rules
│   │   ├── sonner.tsx          # Toast notification viewport wrapper
│   │   ├── textarea.tsx        # Multi-line textareas for field notes
│   │   ├── toggle.tsx          # Toggle button primitive
│   │   └── toggle-group.tsx    # Filter toggle button groups
│   ├── admin-view.tsx          # Admin metrics, user role promotion, dataset info
│   ├── auditor-view.tsx        # Auditor review inbox, photo inspection & decision modal
│   ├── civic-quest.tsx         # Primary application shell, tab routing & auth dialogs
│   ├── evidence-dialog.tsx     # Citizen photo upload, canvas compression & GPS check-in
│   ├── explore-view.tsx        # Project card catalog, state/category filters & search
│   ├── progression.tsx         # Explorer rail, XP bar, badges, quests & leaderboard
│   └── project-map.tsx         # React-Leaflet map with India boundary constraints
│
├── lib/
│   ├── api.ts                  # Typed Fetch client communicating with FastAPI
│   ├── auth-context.tsx        # React Context for global auth & session rehydration
│   ├── demo-data.ts            # Fallback demonstration project stubs
│   ├── demo-state.ts           # Client state reducer for local simulation
│   └── utils.ts                # Class name merging utility (cn)
│
├── public/
│   ├── images/
│   │   ├── community-hall.png  # Project visual asset
│   │   ├── neighborhood-park.png # Project visual asset
│   │   └── quest-city.png      # CivicQuest hero artwork
│   ├── file.svg / globe.svg    # Static SVG assets
│   └── works_map.html          # Static mirror of the Folium map
│
├── .env.local                  # Environment variables for local development
├── components.json             # Shadcn component configuration
├── eslint.config.mjs           # ESLint configuration
├── next.config.ts              # Next.js security headers and build options
├── package.json                # Pinned dependencies & scripts (pnpm@10.34.3)
├── pnpm-lock.yaml              # Lockfile for pnpm
├── postcss.config.mjs          # PostCSS configuration for Tailwind CSS v4
└── tsconfig.json               # Strict TypeScript compiler options
```

---

## ⚙️ Environment Variables

Configure frontend behavior using `.env.local`:

```env
# URL pointing to the running backend service:
# For local development:
NEXT_PUBLIC_API_URL=http://localhost:8000

# For production (Vercel deployment):
# NEXT_PUBLIC_API_URL=https://civicquest-backend.onrender.com
```

| Variable | Required | Default in Code | Description |
|---|:---:|---|---|
| `NEXT_PUBLIC_API_URL` | No | `https://civicquest-backend.onrender.com` | Base URL of the backend REST API. Must not end with a trailing slash. |

> [!NOTE]
> Variables prefixed with `NEXT_PUBLIC_` are embedded into the client-side JavaScript bundle during the build step. Whenever this variable is updated in production (e.g., on Vercel), a **new deployment / rebuild** must be triggered for changes to take effect.

---

## 💻 Local Development Setup

### Prerequisites
- **Node.js 20+**
- **pnpm** (Recommended, configured via `packageManager: pnpm@10.34.3`) or **npm**
- Running CivicQuest Backend (typically at `http://localhost:8000`)

---

### 1. Install Dependencies

Using `pnpm`:
```bash
pnpm install
```

Or using `npm`:
```bash
npm install
```

---

### 2. Configure Environment

Create `.env.local` in the `Frontend/` folder:

```bash
echo NEXT_PUBLIC_API_URL=http://localhost:8000 > .env.local
```

*(If testing against the cloud backend directly, you can use `https://civicquest-backend.onrender.com`)*

---

### 3. Start the Development Server

Using `pnpm`:
```bash
pnpm dev
```

Or using `npm`:
```bash
npm run dev
```

Open **[`http://localhost:3000`](http://localhost:3000)** in your browser. The application supports Hot Module Replacement (HMR).

---

## 📦 Production Build & Validation

To test the production compilation locally:

```bash
# 1. Type-check and compile the Next.js production bundle
pnpm build
# (or: npm run build)

# 2. Run the production server locally
pnpm start
# (or: npm run start)
```

The production server starts on port `3000` with optimized assets and zero development overhead.

---

## 🚀 Vercel Deployment

The frontend is optimized for deployment on the **[Vercel Platform](https://vercel.com/)**:

1. **Connect Repository:** Import your repository into the Vercel dashboard.
2. **Set Root Directory:** Set the Root Directory to **`Frontend`**.
3. **Framework Preset:** Select **Next.js** (automatically detected).
4. **Environment Variables:** Add:
   ```text
   NEXT_PUBLIC_API_URL = https://civicquest-backend.onrender.com
   ```
5. **Deploy:** Click Deploy. Vercel automatically runs `next build` and deploys the app to the global edge network.

---

## 📸 Screenshots & UI Previews

<div align="center">

<table>
  <tr>
    <td width="50%" align="center">
      <img src="public/images/quest-city.png" width="100%" alt="CivicQuest Hero" style="border-radius: 8px;" />
      <br />
      <b>Citizen Exploration & Hero</b>
    </td>
    <td width="50%" align="center">
      <img src="public/images/community-hall.png" width="100%" alt="Project Card Example" style="border-radius: 8px;" />
      <br />
      <b>Public Development Work Preview</b>
    </td>
  </tr>
</table>

*(Additional high-resolution interface captures of the Map, Evidence Dialog, and Auditor Desk can be linked here)*

</div>

---

## 🔧 Troubleshooting

| Issue | Likely Cause | Solution |
|---|---|---|
| **"Network Error" / Cannot log in** | Backend is sleeping or unreachable | The free Render backend spins down after inactivity. Open [`https://civicquest-backend.onrender.com`](https://civicquest-backend.onrender.com) once in your browser to wake it up (takes ~30s). |
| **CORS blocked by browser** | Frontend domain not whitelisted | Add your frontend origin (e.g. `https://civicquest-tau.vercel.app`) to the backend's `CORS_ORIGINS` environment variable in Render. |
| **Map fails to render / Blank container** | Leaflet container sizing before DOM ready | Ensure Leaflet CSS is imported and the component is loaded with `{ ssr: false }`. `project-map.tsx` automatically calls `map.invalidateSize()`. |
| **Old backend URL called after env change** | Stale Next.js build cache | `NEXT_PUBLIC_` variables are baked in at build time. Redeploy or rebuild the project (`pnpm build`). |
| **GPS location denied** | Browser permission blocked | Enable location access in your browser's site settings, or select the **Simulated Visit** option in the evidence dialog. |

---

## 📄 License & Attribution

This project is part of the CivicQuest civic transparency platform. License information has not yet been specified.
