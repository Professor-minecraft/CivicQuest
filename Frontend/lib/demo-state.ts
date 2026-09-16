import { PROJECTS } from "./demo-data";

export const APPROVAL_XP = 150;
export const LEVEL_XP = 450;
export type CheckIn = { kind: "simulated"; timestamp: string } | { kind: "gps"; lat: number; lng: number; accuracy: number; distance: number; timestamp: string };
export type Submission = {
  id: string; projectId: string; photo: string; fileName: string;
  observation: "Completed" | "Ongoing" | "Not done";
  notes: string; checkIn: CheckIn; submittedAt: string;
  status: "pending" | "approved" | "rejected"; feedback?: string;
};
export type DemoState = { submissions: Submission[] };
export type DemoAction =
  | { type: "submit"; submission: Submission }
  | { type: "review"; id: string; decision: "approved" | "rejected"; feedback: string }
  | { type: "reset" };
export const initialState: DemoState = { submissions: [] };

export function demoReducer(state: DemoState, action: DemoAction): DemoState {
  if (action.type === "reset") {
    return { submissions: [] };
  }
  if (action.type === "submit") {
    const entry = action.submission;
    if (!PROJECTS.some((p) => p.id === entry.projectId) || state.submissions.some((s) => s.projectId === entry.projectId && s.status !== "rejected")) return state;
    if (!entry.photo || !entry.notes.trim() || !entry.checkIn) return state;
    return { submissions: [{ ...entry, status: "pending", feedback: undefined }, ...state.submissions] };
  }
  if (action.type !== "review") return state;
  if (action.decision === "rejected" && !action.feedback.trim()) return state;
  return { submissions: state.submissions.map((s) => s.id === action.id && s.status === "pending" ? { ...s, status: action.decision, feedback: action.feedback.trim() } : s) };
}

export function getProgress(state: DemoState) {
  const approved = new Set(state.submissions.filter((s) => s.status === "approved").map((s) => s.projectId)).size;
  const xp = approved * APPROVAL_XP;
  return { approved, xp, level: Math.floor(xp / LEVEL_XP) + 1, levelProgress: xp % LEVEL_XP, pending: state.submissions.filter((s) => s.status === "pending").length };
}
