import { useEffect, useState } from "react";
import { ArrowRight, ClipboardList, Compass, FolderOpen, LayoutDashboard, RefreshCw, Settings, ShieldCheck, Users } from "lucide-react";
import { PROJECTS } from "@/lib/demo-data";
import { api, type AdminStats, type UserProfile, type BackendProject } from "@/lib/api";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";

export function AdminView({ onExplore }: { onExplore: () => void }) {
  const [stats, setStats] = useState<AdminStats | null>(null);
  const [users, setUsers] = useState<UserProfile[]>([]);
  const [projects, setProjects] = useState<BackendProject[]>([]);

  function loadData() {
    Promise.all([
      api.getAdminStats().then(setStats).catch(() => {}),
      api.getAdminUsers().then(setUsers).catch(() => {}),
      api.getProjects({ limit: 10 }).then((d) => setProjects(d.projects)).catch(() => {})
    ]);
  }

  useEffect(() => {
    Promise.all([
      api.getAdminStats().then(setStats).catch(() => {}),
      api.getAdminUsers().then(setUsers).catch(() => {}),
      api.getProjects({ limit: 10 }).then((d) => setProjects(d.projects)).catch(() => {})
    ]);
  }, []);

  return (
    <section className="page-section">
      <div className="page-intro">
        <span className="eyebrow"><LayoutDashboard />ADMIN PANEL</span>
        <h1>Platform management.</h1>
        <p>Manage projects, review submissions, and oversee platform activity in real-time.</p>
      </div>

      {/* Stats overview */}
      <div className="summary-grid" style={{ marginBottom: "32px" }}>
        <div><FolderOpen /><span>Total works</span><strong>{stats ? stats.total_projects : PROJECTS.length}</strong></div>
        <div><ShieldCheck /><span>Pending reviews</span><strong>{stats ? stats.pending_reviews : 0}</strong></div>
        <div><Users /><span>Registered users</span><strong>{stats ? stats.total_users : users.length}</strong></div>
      </div>

      {/* Admin sections */}
      <div className="admin-grid">

        {/* Project management */}
        <div className="admin-card">
          <div className="admin-card-header">
            <span className="admin-card-icon"><FolderOpen /></span>
            <div>
              <h2>Government works dataset</h2>
              <p>{stats ? `${stats.total_projects} MPLADS works imported in PostgreSQL` : "Public works database"}</p>
            </div>
          </div>
          <div className="admin-project-list">
            {projects.length > 0 ? (
              projects.slice(0, 4).map((p) => (
                <div key={p.id} className="admin-project-row">
                  <div>
                    <strong>{p.work || "MPLADS Work"}</strong>
                    <span>{p.constituency || p.state} · {p.work_category || "Infrastructure"}</span>
                  </div>
                  <Badge variant="secondary">{p.status || "Completed"}</Badge>
                </div>
              ))
            ) : (
              PROJECTS.slice(0, 4).map((p) => (
                <div key={p.id} className="admin-project-row">
                  <div>
                    <strong>{p.name}</strong>
                    <span>{p.locality} · {p.category}</span>
                  </div>
                  <Badge variant="secondary">{p.status}</Badge>
                </div>
              ))
            )}
            {(stats?.total_projects || PROJECTS.length) > 4 && (
              <p className="admin-more-label">+{(stats?.total_projects || PROJECTS.length) - 4} more records</p>
            )}
          </div>
          <div className="admin-card-footer">
            <button className="text-action" onClick={onExplore}>View all on map<ArrowRight /></button>
          </div>
        </div>

        {/* Review oversight */}
        <div className="admin-card">
          <div className="admin-card-header">
            <span className="admin-card-icon"><ClipboardList /></span>
            <div>
              <h2>Review oversight</h2>
              <p>Auditor decisions and verification flow.</p>
            </div>
          </div>
          <div className="admin-settings-list" style={{ margin: "16px 0" }}>
            <div className="admin-setting-row"><span>Pending reviews</span><strong>{stats?.pending_reviews ?? 0}</strong></div>
            <div className="admin-setting-row"><span>Approved reviews</span><strong>{stats?.approved_reviews ?? 0}</strong></div>
            <div className="admin-setting-row"><span>Rejected reviews</span><strong>{stats?.rejected_reviews ?? 0}</strong></div>
            <div className="admin-setting-row"><span>Total XP rewarded</span><strong>{stats?.total_xp_awarded ?? 0} XP</strong></div>
          </div>
          <div className="admin-card-footer">
            <Badge variant="secondary">Live PostgreSQL Audits</Badge>
          </div>
        </div>

        {/* User management */}
        <div className="admin-card">
          <div className="admin-card-header">
            <span className="admin-card-icon"><Users /></span>
            <div>
              <h2>User management</h2>
              <p>Roles and community permissions.</p>
            </div>
          </div>
          <div className="admin-project-list">
            {users.slice(0, 4).map((u) => (
              <div key={u.id} className="admin-project-row">
                <div>
                  <strong>{u.name}</strong>
                  <span>{u.email}</span>
                </div>
                <Badge variant={u.role === "ADMIN" ? "default" : u.role === "AUDITOR" ? "secondary" : "outline"}>{u.role}</Badge>
              </div>
            ))}
            {users.length > 4 && (
              <p className="admin-more-label">+{users.length - 4} more users</p>
            )}
          </div>
          <div className="admin-card-footer">
            <Badge variant="outline">{stats?.total_auditors ?? 1} Authorized Auditors</Badge>
          </div>
        </div>

        {/* Platform settings */}
        <div className="admin-card">
          <div className="admin-card-header">
            <span className="admin-card-icon"><Settings /></span>
            <div>
              <h2>Platform rules & parameters</h2>
              <p>Verified civic verification settings.</p>
            </div>
          </div>
          <div className="admin-settings-list">
            <div className="admin-setting-row"><span>XP per approved review</span><strong>150 XP</strong></div>
            <div className="admin-setting-row"><span>XP per explorer level</span><strong>450 XP</strong></div>
            <div className="admin-setting-row"><span>Certificate threshold</span><strong>5 approved verifications</strong></div>
            <div className="admin-setting-row"><span>Dataset source</span><strong>MPLADS Completed Works</strong></div>
          </div>
          <div className="admin-card-footer">
            <Button variant="outline" size="sm" onClick={loadData}>
              <RefreshCw data-icon="inline-start" />Refresh metrics
            </Button>
          </div>
        </div>

      </div>

      <div className="notice-box" style={{ marginTop: "32px" }}>
        <Compass />
        <p><strong>Connected to CivicQuest FastAPI Backend.</strong> All project records, users, audits, and statistics are stored persistently in PostgreSQL.</p>
      </div>
    </section>
  );
}
