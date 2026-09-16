import { useEffect, useState } from "react";
import { ArrowRight, Award, Camera, Check, Compass, Download, Flag, Leaf, LockKeyhole, Medal, ShieldCheck, Sparkles, Target, Trophy, Zap } from "lucide-react";
import { PROJECTS, type Project } from "@/lib/demo-data";
import { getProgress, LEVEL_XP, type DemoState } from "@/lib/demo-state";
import { api, type LeaderboardUser, type BackendSubmission, type CertificateItem } from "@/lib/api";
import { useAuth } from "@/lib/auth-context";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import { ProjectStatusBadge } from "./explore-view";
import { cn } from "@/lib/utils";

export const BADGES = [
  { name: "First steps", description: "Your first approved verification", threshold: 1, icon: Compass, color: "mint" },
  { name: "Local legend", description: "3 approved verifications", threshold: 3, icon: ShieldCheck, color: "peach" },
  { name: "Changemaker", description: "5 approved verifications & Citizen Certificate", threshold: 5, icon: Trophy, color: "lilac" },
];

export function ExplorerRail({ state, onQuests, onBadges, onLeaderboard }: { state: DemoState; onQuests: () => void; onBadges: () => void; onLeaderboard: () => void }) {
  const { user } = useAuth();
  const demoProg = getProgress(state);

  const xp = user ? user.xp : demoProg.xp;
  const level = user ? user.level : demoProg.level;
  const approved = user ? Math.floor(user.xp / 150) : demoProg.approved;
  const pending = demoProg.pending;
  const levelProgress = xp % LEVEL_XP;

  return <aside className="explorer-rail" aria-label="Your explorer progress"><section className="profile-panel"><div className="profile-top"><span>YOUR EXPLORER CARD</span><Sparkles /></div><div className="explorer-avatar"><Compass /><span>{level}</span></div><h3>{user ? user.name : "Explorer"}</h3><p>{user ? `${user.role} Member` : "Neighborhood Explorer"}</p><Badge variant="secondary">Level {level} · {level < 2 ? "Curious Citizen" : "Community Scout"}</Badge><div className="xp-label"><span><Zap />Total XP</span><strong>{xp.toLocaleString()} <small>XP</small></strong></div><Progress value={levelProgress / LEVEL_XP * 100} aria-label="Progress toward next explorer level" /><div className="next-level"><span>{LEVEL_XP - levelProgress} XP to Level {level + 1}</span><span>{levelProgress}/{LEVEL_XP}</span></div><div className="profile-stats"><div><strong>{approved}</strong><span><ShieldCheck />Verified</span></div><div><strong>{pending}</strong><span><Camera />In review</span></div><div><strong>{BADGES.filter((b) => approved >= b.threshold).length}</strong><span><Award />Badges</span></div></div></section>
    <section className="weekly-panel"><div className="rail-heading"><h3><Flag />Your next challenge</h3><span className="small-label">QUEST</span></div><h4>Neighborhood champion</h4><p>Get 3 local work reviews approved.<br />Good things start close to home.</p><div className="challenge-progress"><Progress value={Math.min(approved / 3, 1) * 100} aria-label="Neighborhood champion challenge" /><span>{Math.min(approved, 3)}/3</span></div><div className="challenge-footer"><span className="xp-reward"><Zap />450 XP total</span><button aria-label="View neighborhood champion quest" onClick={onQuests}><ArrowRight /></button></div></section>
    <section className="badge-panel"><div className="rail-heading"><h3>Your badge collection</h3><button className="text-action" onClick={onBadges}>View all<ArrowRight /></button></div><div className="mini-badges">{BADGES.map((b) => <button key={b.name} title={`${b.name}: ${b.description}`} onClick={onBadges}><span className={cn("badge-medallion", b.color, approved < b.threshold && "locked")}><b.icon />{approved < b.threshold && <LockKeyhole className="badge-lock" />}</span><span>{b.name}</span></button>)}</div></section>
    <section className="impact-panel"><span className="impact-illustration"><Leaf /><Sparkles /></span><h3>A little effort.<br />A lasting impact.</h3><p>Every honest review helps build a more accountable community.</p><button className="text-action" onClick={onLeaderboard}>Meet the changemakers<ArrowRight /></button></section>
  </aside>;
}

export function QuestsView({ state, onOpen, onExplore }: { state: DemoState; onOpen?: (p: Project) => void; onExplore: () => void }) {
  const { user } = useAuth();
  const [liveSubmissions, setLiveSubmissions] = useState<BackendSubmission[]>([]);

  useEffect(() => {
    if (user) {
      api.getMySubmissions().then(setLiveSubmissions).catch(() => {});
    }
  }, [user]);

  const hasLive = liveSubmissions.length > 0;
  const submissionsList = hasLive ? liveSubmissions : state.submissions;
  const approvedCount = hasLive ? liveSubmissions.filter((s) => s.status === "APPROVED").length : getProgress(state).approved;
  const totalXp = user ? user.xp : getProgress(state).xp;

  return <section className="page-section"><div className="page-intro"><span className="eyebrow"><Flag />YOUR ADVENTURE LOG</span><h1>Little missions. Meaningful progress.</h1><p>Your photo is the first step. Every auditor-approved verification earns 150 XP.</p></div><div className="summary-grid"><div><Camera /><span>Submitted</span><strong>{submissionsList.length}</strong></div><div><ShieldCheck /><span>Approved works</span><strong>{approvedCount}</strong></div><div><Zap /><span>XP earned</span><strong>{totalXp}</strong></div></div><div className="section-heading"><div><h2>Your verification quests</h2><p>{user ? "Your verified public works journal." : "Session activity log."}</p></div><Button variant="outline" onClick={onExplore}>Find a new quest<ArrowRight data-icon="inline-end" /></Button></div>{submissionsList.length ? <div className="quest-log">{submissionsList.map((s) => {
    const pId = "project_id" in s ? s.project_id : s.projectId;
    const workTitle = "project" in s && s.project?.work ? s.project.work : PROJECTS.find((p) => p.id === pId)?.name || pId;
    const checkKind = "check_in_type" in s ? s.check_in_type : s.checkIn?.kind;
    const isApproved = s.status === "approved" || s.status === "APPROVED";
    const feedbackText = "review_feedback" in s ? s.review_feedback : "feedback" in s ? s.feedback : null;
    const matchingProj = PROJECTS.find((p) => p.id === pId);

    return <article key={s.id}><div className={cn("quest-log-icon", isApproved && "is-approved")}>{isApproved ? <Check /> : <Camera />}</div><div className="quest-log-text"><h3>{workTitle}</h3><p>You observed: {s.observation} · {checkKind === "simulated" ? "Simulated visit" : "GPS visit"}</p>{feedbackText && <p className="audit-feedback">Auditor: {feedbackText}</p>}</div><div className="quest-log-status"><ProjectStatusBadge status={s.status} /><span>{isApproved ? "+150 XP earned" : "No XP awarded"}</span></div>{matchingProj && onOpen && <Button size="sm" variant="outline" onClick={() => onOpen(matchingProj)}>{s.status === "rejected" || s.status === "REJECTED" ? "Try again" : "Details"}</Button>}</article>;
  })}</div> : <div className="empty-state spacious"><Compass /><h3>Your first quest is waiting.</h3><p>Choose a public work from the map, check in, and submit a photo and your observations.</p><Button onClick={onExplore}>Start exploring<ArrowRight data-icon="inline-end" /></Button></div>}<div className="challenge-banner"><Target /><div><h3>Neighborhood champion</h3><p>Get 3 different project reviews approved to unlock the Local legend badge.</p></div><strong>{Math.min(approvedCount, 3)} / 3</strong></div></section>;
}

export function BadgesView({ state }: { state: DemoState }) {
  const { user } = useAuth();
  const [certs, setCerts] = useState<CertificateItem[]>([]);
  const demoProg = getProgress(state);
  const approved = user ? Math.floor(user.xp / 150) : demoProg.approved;

  useEffect(() => {
    if (user) {
      api.getCertificates().then(setCerts).catch(() => {});
    }
  }, [user]);

  return <section className="page-section"><div className="page-intro"><span className="eyebrow"><Medal />COLLECT MOMENTS THAT MATTER</span><h1>Wear your impact with pride.</h1><p>Badges are earned through approved reviews, never just uploads.</p></div>
    <div className="achievement-grid">{BADGES.map((b) => { const unlocked = approved >= b.threshold; return <article key={b.name} className={cn("achievement-card", unlocked && "unlocked")}><span className={cn("badge-medallion", b.color, !unlocked && "locked")}><b.icon />{!unlocked && <LockKeyhole className="badge-lock" />}</span><Badge variant={unlocked ? "secondary" : "outline"}>{unlocked ? "Unlocked" : "Locked"}</Badge><h2>{b.name}</h2><p>{b.description}</p><Progress value={Math.min(approved / b.threshold, 1) * 100} aria-label={`${b.name} badge progress`} /><span>{Math.min(approved, b.threshold)} / {b.threshold} approved reviews</span></article>; })}</div>

    {/* Certificate Banner when 5+ verifications approved or cert exists */}
    {(approved >= 5 || certs.length > 0) && (
      <div className="challenge-banner" style={{ background: "#fdf8ee", borderColor: "#f1dfb5", marginBottom: "20px" }}>
        <Trophy className="text-amber-600" />
        <div>
          <h3>CivicQuest Civic Participation Certificate Unlocked</h3>
          <p>You have demonstrated outstanding civic participation with {approved} approved field verifications.</p>
        </div>
        {certs.length > 0 ? (
          <a href={api.getCertificateDownloadUrl(certs[0].id)} target="_blank" rel="noreferrer" style={{ textDecoration: "none" }}>
            <Button size="sm"><Download data-icon="inline-start" />Download PDF</Button>
          </a>
        ) : (
          <Badge variant="secondary">Certificate Issued</Badge>
        )}
      </div>
    )}

    <div className="notice-box"><Zap /><p><strong>Your next level is an adventure away.</strong> Earn 150 XP for each approved project verification. Every 450 XP unlocks another explorer level. Badges do not add bonus XP.</p></div>
  </section>;
}

export function LeaderboardView({ state }: { state: DemoState }) {
  const { user } = useAuth();
  const [dbLeaders, setDbLeaders] = useState<LeaderboardUser[]>([]);

  useEffect(() => {
    api.getLeaderboard()
      .then((data) => {
        if (data && data.length > 0) setDbLeaders(data);
      })
      .catch(() => {});
  }, []);

  const hasLiveLeaders = dbLeaders.length > 0;
  const demoXp = getProgress(state).xp;

  return <section className="page-section"><div className="page-intro"><span className="eyebrow"><Trophy />LOCAL ACTION. COLLECTIVE IMPACT.</span><h1>Meet your neighborhood heroes.</h1><p>A little friendly competition. A whole lot of positive change.</p></div><div className="leaderboard-heading"><h2>Civic changemakers</h2><Badge variant="outline">{hasLiveLeaders ? "Live database leaderboard" : "Leaderboard"}</Badge></div><div className="leaderboard-list"><div className="leaderboard-labels"><span>RANK</span><span>EXPLORER</span><span>LEVEL</span><span>TOTAL XP</span></div>
    {hasLiveLeaders ? dbLeaders.map((person, i) => {
      const isYou = user?.id === person.id;
      const initials = person.name.split(" ").map((n) => n[0]).join("").toUpperCase().slice(0, 2);
      const color = i % 3 === 0 ? "mint" : i % 3 === 1 ? "peach" : "lilac";
      return <div key={person.id} className={cn("leaderboard-row", isYou && "your-ranking")}><span className="rank-number">{i === 0 ? <Trophy /> : String(i + 1).padStart(2, "0")}</span><div className="leader-person"><span className={cn("initial-avatar", color)}>{initials}</span><div><strong>{person.name}{isYou && <Badge variant="secondary">You</Badge>}</strong><small>{person.approved_count} verified works</small></div></div><span className="leader-level">Level {person.level}</span><strong className="leader-xp"><Zap />{person.xp.toLocaleString()}</strong></div>;
    }) : (
      <div style={{ textAlign: "center", padding: "40px 20px" }}>
        <Trophy className="mx-auto size-10" style={{ color: "var(--muted-foreground)" }} />
        <h3 style={{ marginTop: "12px", fontSize: "16px", fontWeight: "600" }}>No verified quests yet</h3>
        <p style={{ fontSize: "13px", color: "var(--muted-foreground)", marginTop: "4px" }}>
          Be the first citizen explorer to submit a verified public work review and earn 150 XP!
        </p>
      </div>
    )}</div>
    <p className="data-disclaimer">Scores update in real time when citizen verifications are audited and approved.</p>
  </section>;
}
