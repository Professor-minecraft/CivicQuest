import assert from "node:assert/strict";
import { test } from "node:test";
import { demoReducer, getProgress, initialState, type Submission } from "./demo-state";
import { PROJECTS, distanceMeters } from "./demo-data";

function submission(projectId = "CQ-001", id = "review-1"): Submission {
  return { id, projectId, photo: "data:image/png;base64,example", fileName: "photo.png", observation: "Ongoing", notes: "The entrance is still under construction.", checkIn: { kind: "simulated", timestamp: "2026-09-11T12:00:00Z" }, submittedAt: "2026-09-11T12:00:00Z", status: "pending" };
}

test("uploads award no XP; approval awards exactly 150 once", () => {
  const pending = demoReducer(initialState, { type: "submit", submission: submission() });
  assert.equal(getProgress(pending).xp, 0);
  assert.equal(getProgress(pending).pending, 1);
  const approved = demoReducer(pending, { type: "review", id: "review-1", decision: "approved", feedback: "Evidence is consistent." });
  assert.equal(getProgress(approved).xp, 150);
  assert.equal(getProgress(approved).approved, 1);
  const duplicate = demoReducer(approved, { type: "review", id: "review-1", decision: "approved", feedback: "Again" });
  assert.equal(getProgress(duplicate).xp, 150);
  assert.equal(PROJECTS[0].status, "Ongoing");
  assert.equal(duplicate.submissions[0].observation, "Ongoing");
});

test("duplicate pending and approved project submissions are blocked", () => {
  const pending = demoReducer(initialState, { type: "submit", submission: submission() });
  assert.equal(demoReducer(pending, { type: "submit", submission: submission("CQ-001", "review-2") }).submissions.length, 1);
  const approved = demoReducer(pending, { type: "review", id: "review-1", decision: "approved", feedback: "" });
  assert.equal(demoReducer(approved, { type: "submit", submission: submission("CQ-001", "review-2") }).submissions.length, 1);
});

test("rejection requires feedback, awards zero, and allows a new attempt", () => {
  const pending = demoReducer(initialState, { type: "submit", submission: submission() });
  assert.equal(demoReducer(pending, { type: "review", id: "review-1", decision: "rejected", feedback: "  " }).submissions[0].status, "pending");
  const rejected = demoReducer(pending, { type: "review", id: "review-1", decision: "rejected", feedback: "Photo does not show the entrance." });
  assert.equal(getProgress(rejected).xp, 0);
  const attemptedFlip = demoReducer(rejected, { type: "review", id: "review-1", decision: "approved", feedback: "" });
  assert.equal(getProgress(attemptedFlip).xp, 0);
  const retry = demoReducer(rejected, { type: "submit", submission: submission("CQ-001", "review-2") });
  assert.equal(retry.submissions.length, 2);
  const approvedRetry = demoReducer(retry, { type: "review", id: "review-2", decision: "approved", feedback: "" });
  assert.equal(getProgress(approvedRetry).xp, 150);
});

test("three approved projects unlock level two at 450 XP", () => {
  let state = initialState;
  for (const project of PROJECTS.slice(0, 3)) {
    state = demoReducer(state, { type: "submit", submission: submission(project.id, project.id) });
    state = demoReducer(state, { type: "review", id: project.id, decision: "approved", feedback: "" });
  }
  assert.deepEqual(getProgress(state), { approved: 3, xp: 450, level: 2, levelProgress: 0, pending: 0 });
});

test("unknown projects and missing evidence are rejected", () => {
  assert.equal(demoReducer(initialState, { type: "submit", submission: submission("unknown") }).submissions.length, 0);
  assert.equal(demoReducer(initialState, { type: "submit", submission: { ...submission(), photo: "" } }).submissions.length, 0);
});

test("GPS distance is zero at the sample location and detects distant visits", () => {
  assert.equal(distanceMeters(PROJECTS[0], PROJECTS[0]), 0);
  assert.ok(distanceMeters(PROJECTS[0], { lat: 28.6139, lng: 77.209 }) > 1_000_000);
});
