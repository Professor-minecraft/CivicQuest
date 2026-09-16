import { useCallback, useEffect, useState, type Dispatch } from "react";
import Image from "next/image";
import { CheckCircle2, ClipboardCheck, ShieldCheck, X } from "lucide-react";
import { toast } from "sonner";
import { PROJECTS } from "@/lib/demo-data";
import { type DemoAction, type DemoState, type Submission } from "@/lib/demo-state";
import { api, type BackendSubmission } from "@/lib/api";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle } from "@/components/ui/dialog";
import { Field, FieldGroup, FieldLabel } from "@/components/ui/field";
import { Textarea } from "@/components/ui/textarea";
import { ToggleGroup, ToggleGroupItem } from "@/components/ui/toggle-group";
import { CheckInDetails } from "./evidence-dialog";
import { ProjectStatusBadge } from "./explore-view";

function mapBackendToSubmission(bs: BackendSubmission): Submission {
  return {
    id: bs.id,
    projectId: bs.project_id,
    photo: bs.photo_url.startsWith("http") ? bs.photo_url : `http://localhost:8000${bs.photo_url}`,
    fileName: bs.file_name || "evidence.jpg",
    observation: bs.observation,
    notes: bs.notes,
    checkIn: bs.check_in_type === "gps" && bs.gps_latitude && bs.gps_longitude ? {
      kind: "gps",
      lat: bs.gps_latitude,
      lng: bs.gps_longitude,
      accuracy: bs.gps_accuracy || 20,
      distance: bs.distance_from_project || 50,
      timestamp: bs.submitted_at
    } : {
      kind: "simulated",
      timestamp: bs.submitted_at
    },
    submittedAt: bs.submitted_at,
    status: bs.status.toLowerCase() as "pending" | "approved" | "rejected",
    feedback: bs.review_feedback || undefined
  };
}

export function AuditorView({ state, dispatch, onExplore }: { state: DemoState; dispatch: Dispatch<DemoAction>; onExplore: () => void }) {
  const [filter, setFilter] = useState("pending");
  const [reviewId, setReviewId] = useState<string | null>(null);
  const [checked, setChecked] = useState(false);
  const [feedback, setFeedback] = useState("");
  const [backendItems, setBackendItems] = useState<Submission[]>([]);

  const loadSubmissions = useCallback(() => {
    if (filter === "pending") {
      api.getPendingAudits()
        .then((subs) => setBackendItems(subs.map(mapBackendToSubmission)))
        .catch(() => {});
    } else {
      api.getAuditHistory()
        .then((subs) => setBackendItems(subs.map(mapBackendToSubmission)))
        .catch(() => {});
    }
  }, [filter]);

  useEffect(() => {
    loadSubmissions();
  }, [loadSubmissions]);

  const sourceSubmissions = backendItems.length > 0 ? backendItems : state.submissions;
  const entries = sourceSubmissions.filter((s) => filter === "all" || s.status === filter);
  const review = sourceSubmissions.find((s) => s.id === reviewId);
  const project = PROJECTS.find((p) => p.id === review?.projectId);

  async function decide(decision: "approved" | "rejected") {
    if (!review || review.status !== "pending") return;
    if (!checked) { toast.error("Confirm that you reviewed the image and visit details first."); return; }
    if (decision === "rejected" && feedback.trim().length < 5) { toast.error("Add a rejection reason of at least 5 characters."); return; }

    try {
      if (decision === "approved") {
        await api.approveSubmission(review.id, feedback.trim());
      } else {
        await api.rejectSubmission(review.id, feedback.trim());
      }
      toast.success(decision === "approved" ? "Evidence approved · 150 XP awarded" : "Evidence rejected · no XP awarded", { description: "Audited record saved to PostgreSQL." });
      loadSubmissions();
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : "Audited locally.";
      toast.success(decision === "approved" ? "Evidence approved" : "Evidence rejected", { description: msg });
    }

    dispatch({ type: "review", id: review.id, decision, feedback });
    setReviewId(null);
  }

  const pendingCount = sourceSubmissions.filter((s) => s.status === "pending").length;

  return <section className="page-section"><div className="page-intro"><span className="eyebrow"><ShieldCheck />AUDITOR WORKSPACE</span><h1>A second look makes a difference.</h1><p>Review citizen evidence thoughtfully. Reward honest observations, not just completed work.</p></div><div className="review-toolbar"><h2>Evidence inbox <span className="count-pill">{pendingCount} pending</span></h2><ToggleGroup value={[filter]} onValueChange={(v) => v[0] && setFilter(v[0])} aria-label="Filter audit submissions"><ToggleGroupItem value="pending">Pending</ToggleGroupItem><ToggleGroupItem value="all">All reviews</ToggleGroupItem></ToggleGroup></div>
    {entries.length ? <div className="audit-list">{entries.map((s) => <article key={s.id} className="audit-row"><Image src={s.photo} alt="Citizen-submitted evidence thumbnail" width={88} height={76} unoptimized /><div className="audit-row-copy"><h3>{PROJECTS.find((p) => p.id === s.projectId)?.name || s.projectId}</h3><p>Citizen observation: {s.observation}</p><span>{s.checkIn.kind === "simulated" ? "Simulated visit" : "GPS check-in"} · {new Date(s.submittedAt).toLocaleDateString()}</span></div><ProjectStatusBadge status={s.status} /><Button variant="outline" size="sm" onClick={() => { setReviewId(s.id); setChecked(false); setFeedback(""); }}>{s.status === "pending" ? "Review evidence" : "View decision"}</Button></article>)}</div> : <div className="empty-state spacious"><ClipboardCheck /><h3>{filter === "pending" ? "All clear. No evidence waiting." : "Your review desk is ready."}</h3><p>Citizen verifications submitted on the map will appear here for review.</p><Button onClick={onExplore}>Explore works</Button></div>}
    <Dialog open={!!review} onOpenChange={(open) => { if (!open) setReviewId(null); }}><DialogContent className="sm:max-w-2xl max-h-[90dvh] overflow-y-auto p-6"><DialogHeader><DialogTitle>Review evidence</DialogTitle><DialogDescription>{project?.name || review?.projectId} · Citizen submission</DialogDescription></DialogHeader>{review && <><div className="audit-evidence-image"><Image src={review.photo} alt="Full citizen photo submitted for manual evidence review" width={800} height={500} unoptimized /></div><div className="audit-facts"><div><span>Reported project status</span><strong>{project?.status || "Government Work"}</strong></div><div><span>Citizen observation</span><strong>{review.observation}</strong></div><Badge variant="outline">{review.status}</Badge></div>
    {/* Honest GPS status limitation */}
    {review.checkIn.kind === "gps" && (
      <div style={{ background: "#fef3c7", border: "1px solid #fde68a", borderRadius: "6px", padding: "8px 12px", margin: "8px 0", fontSize: "11px", color: "#92400e" }}>
        <strong>Government location: APPROXIMATE · GPS verification: LIMITED</strong>
        <p style={{ margin: "2px 0 0" }}>Project coordinate is based on constituency geodata. GPS distance indicates regional proximity, not absolute proof of physical site attendance.</p>
      </div>
    )}
    <CheckInDetails checkIn={review.checkIn} /><div className="citizen-notes"><strong>Citizen notes</strong><p>{review.notes}</p><small>{review.fileName} · {new Date(review.submittedAt).toLocaleString()}</small></div>{review.status === "pending" ? <FieldGroup><p className="tiny-note">Inspect whether the image is relevant and consistent with the notes. GPS and visual review do not guarantee authenticity.</p><Field orientation="horizontal"><input id="review-confirm" type="checkbox" checked={checked} onChange={(e) => setChecked(e.target.checked)} /><FieldLabel htmlFor="review-confirm">I reviewed the image and visit details.</FieldLabel></Field><Field><FieldLabel htmlFor="audit-feedback">Feedback (required for rejection)</FieldLabel><Textarea id="audit-feedback" value={feedback} onChange={(e) => setFeedback(e.target.value)} maxLength={1000} placeholder="Explain what supports the evidence or what needs to be resubmitted." /></Field><div className="audit-decision-actions"><Button variant="destructive" onClick={() => decide("rejected")}><X data-icon="inline-start" />Reject evidence</Button><Button disabled={!checked} onClick={() => decide("approved")}><CheckCircle2 data-icon="inline-start" />Approve · award 150 XP</Button></div></FieldGroup> : <div className="notice-box"><CheckCircle2 /><p><strong>{review.status === "approved" ? "150 XP awarded once." : "No XP awarded."}</strong><br />{review.feedback || "No additional feedback provided."}</p></div>}</>}</DialogContent></Dialog>
  </section>;
}
