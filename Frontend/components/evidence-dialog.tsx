"use client";

import { useRef, useState, type ChangeEvent, type Dispatch, type FormEvent } from "react";
import Image from "next/image";
import { CheckCircle2, Clock3, LocateFixed, Navigation, ShieldCheck } from "lucide-react";
import { toast } from "sonner";
import { distanceMeters, type Project } from "@/lib/demo-data";
import { type CheckIn, type DemoAction, type Submission } from "@/lib/demo-state";
import { api } from "@/lib/api";
import { Button } from "@/components/ui/button";
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle } from "@/components/ui/dialog";
import { Field, FieldGroup, FieldLabel } from "@/components/ui/field";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";

export function CheckInDetails({ checkIn }: { checkIn: CheckIn }) {
  return <div className="check-in-details"><Navigation className="size-4" /><div>{checkIn.kind === "simulated" ? <><strong>Simulated visit</strong><p>No real location evidence was collected.</p></> : <><strong>GPS: {Math.round(checkIn.distance)} m from sample location</strong><p>Accuracy ±{Math.round(checkIn.accuracy)} m · {checkIn.lat.toFixed(5)}, {checkIn.lng.toFixed(5)}</p></>}<small>{new Date(checkIn.timestamp).toLocaleString()}</small></div></div>;
}

export function EvidenceDialog({ project, submission, dispatch, onClose, onQuests }: { project: Project; submission?: Submission; dispatch: Dispatch<DemoAction>; onClose: () => void; onQuests: () => void }) {
  const [photo, setPhoto] = useState<string | null>(null);
  const [rawFile, setRawFile] = useState<File | null>(null);
  const [fileName, setFileName] = useState("");
  const [observation, setObservation] = useState<"Completed" | "Ongoing" | "Not done">("Completed");
  const [notes, setNotes] = useState("");
  const [checkIn, setCheckIn] = useState<CheckIn | null>(null);
  const [gpsBusy, setGpsBusy] = useState(false);
  const [gpsMessage, setGpsMessage] = useState<string | null>(null);
  const [photoBusy, setPhotoBusy] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const gpsRequest = useRef(0);
  const locked = !!submission;

  function handlePhoto(e: ChangeEvent<HTMLInputElement>) {
    const file = e.target.files?.[0];
    if (!file) return;
    if (!file.type.startsWith("image/")) { setError("Please upload an image file (JPEG, PNG, or WebP)."); return; }
    if (file.size > 8 * 1024 * 1024) { setError("Please select an image smaller than 8MB."); return; }
    setRawFile(file);
    setPhotoBusy(true);
    setError(null);
    const reader = new FileReader();
    reader.onload = () => {
      const img = new window.Image();
      img.onload = () => {
        const max = 1600;
        const ratio = Math.min(1, max / Math.max(img.width, img.height));
        const canvas = document.createElement("canvas");
        canvas.width = Math.round(img.width * ratio);
        canvas.height = Math.round(img.height * ratio);
        const ctx = canvas.getContext("2d");
        if (!ctx) { setPhoto(reader.result as string); setFileName(file.name); setPhotoBusy(false); return; }
        ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
        setPhoto(canvas.toDataURL("image/jpeg", 0.86));
        setFileName(file.name);
        setPhotoBusy(false);
      };
      img.onerror = () => { setPhoto(reader.result as string); setFileName(file.name); setPhotoBusy(false); };
      img.src = reader.result as string;
    };
    reader.onerror = () => { setError("Could not read this file. Please try another photo."); setPhotoBusy(false); };
    reader.readAsDataURL(file);
  }

  function getLocation() {
    if (!navigator.geolocation) { setGpsMessage("This browser does not support GPS. Use a simulated visit to proceed."); return; }
    const id = ++gpsRequest.current;
    setGpsBusy(true);
    setGpsMessage("Requesting GPS location…");
    navigator.geolocation.getCurrentPosition(
      (pos) => {
        if (id !== gpsRequest.current) return;
        const { latitude: lat, longitude: lng, accuracy } = pos.coords;
        const distance = distanceMeters({ lat, lng }, project);
        setCheckIn({ kind: "gps", lat, lng, accuracy, distance, timestamp: new Date().toISOString() });
        setGpsBusy(false);
        setGpsMessage(accuracy > 100 ? "Location accuracy is too low. Retry outdoors, or use a simulated visit." : distance > 200 ? "You are outside the 200 m check-in area. Visit the location, or use a simulated visit." : "You are within the 200 m check-in area. GPS proximity is not proof of photo authenticity.");
      },
      (failure) => {
        if (id !== gpsRequest.current) return;
        setGpsBusy(false);
        setGpsMessage(failure.code === 1 ? "Location permission was denied. You can use a simulated visit." : failure.code === 3 ? "Location request timed out. Retry or use a simulated visit." : "Location is unavailable. Retry or use a simulated visit.");
      },
      { enableHighAccuracy: true, timeout: 10000, maximumAge: 0 }
    );
  }

  async function submit(e: FormEvent) {
    e.preventDefault();
    if (!photo || !rawFile) { setError("Please attach a photo of the public work."); return; }
    if (!checkIn) { setError("Check in with GPS or select a simulated visit."); return; }
    if (checkIn.kind === "gps" && (checkIn.distance > 200 || checkIn.accuracy > 100)) { setError("GPS check-in must be within 200 m with accuracy of 100 m or better. A simulated visit is available."); return; }
    if (notes.trim().length < 10) { setError("Please provide at least 10 characters of descriptive notes."); return; }
    setError(null);
    setIsSubmitting(true);

    try {
      const formData = new FormData();
      formData.append("project_id", project.id);
      formData.append("observation", observation);
      formData.append("notes", notes.trim());
      formData.append("check_in_type", checkIn.kind);
      if (checkIn.kind === "gps") {
        formData.append("gps_latitude", String(checkIn.lat));
        formData.append("gps_longitude", String(checkIn.lng));
        formData.append("gps_accuracy", String(checkIn.accuracy));
      }
      formData.append("photo", rawFile);

      const res = await api.submitVerification(formData);
      dispatch({
        type: "submit",
        submission: {
          id: res.id,
          projectId: project.id,
          photo: res.photo_url ? (res.photo_url.startsWith("http") ? res.photo_url : `${api.login.name ? "http://localhost:8000" : ""}${res.photo_url}`) : photo,
          fileName: res.file_name || fileName || "evidence.jpg",
          observation,
          notes: notes.trim(),
          checkIn,
          submittedAt: res.submitted_at || new Date().toISOString(),
          status: "pending"
        }
      });
      toast.success("Quest submitted for review", { description: "150 XP will be awarded upon auditor approval." });
      onClose();
      onQuests();
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : "Submission failed";
      if (msg.includes("log in")) {
        setError("Please log in or sign up first before submitting citizen evidence.");
        toast.error("Authentication required", { description: "Please log in using the sidebar user card." });
      } else {
        // Still dispatch locally so offline experience works
        dispatch({ type: "submit", submission: { id: `sub-${Date.now()}`, projectId: project.id, photo, fileName: fileName || "evidence.jpg", observation, notes: notes.trim(), checkIn, submittedAt: new Date().toISOString(), status: "pending" } });
        toast.success("Quest recorded", { description: msg || "150 XP will be awarded upon auditor approval." });
        onClose();
        onQuests();
      }
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <Dialog open onOpenChange={(open) => { if (!open) onClose(); }}>
      <DialogContent className="sm:max-w-2xl max-h-[90dvh] overflow-y-auto p-6">
        <DialogHeader><DialogTitle>{project.name}</DialogTitle><DialogDescription>{project.locality} · {project.category}</DialogDescription></DialogHeader>
        {locked ? <div className="submitted-panel"><span className="large-state-icon">{submission.status === "approved" ? <CheckCircle2 /> : <Clock3 />}</span><h3>{submission.status === "approved" ? "Quest approved. +150 XP earned!" : "Your evidence is awaiting review"}</h3><p>{submission.status === "approved" ? "Your evidence was approved. Reported construction status remains unchanged." : "No XP has been awarded yet. An auditor will review your submission shortly."}</p><p><strong>Your observation:</strong> {submission.observation}</p>{submission.feedback && <p><strong>Auditor feedback:</strong> {submission.feedback}</p>}<Button variant="outline" onClick={() => { onClose(); onQuests(); }}>View my quests</Button></div> : <form onSubmit={submit}><FieldGroup>
          <Field><FieldLabel>1. Check in at the work</FieldLabel><div className="check-in-actions"><Button type="button" variant="outline" onClick={getLocation} disabled={gpsBusy}><LocateFixed data-icon="inline-start" />{gpsBusy ? "Finding your location…" : "Use my GPS location"}</Button><Button type="button" variant="secondary" onClick={() => { ++gpsRequest.current; setGpsBusy(false); setCheckIn({ kind: "simulated", timestamp: new Date().toISOString() }); setGpsMessage("This visit is simulated and will be labeled for the auditor."); }}>Simulate visit</Button></div>{checkIn && <CheckInDetails checkIn={checkIn} />}{gpsMessage && <p className="tiny-note" role="status">{gpsMessage}</p>}</Field>
          <Field><FieldLabel htmlFor="evidence-file">2. Attach a photo</FieldLabel><Input id="evidence-file" type="file" accept="image/*" onChange={handlePhoto} /><p className="tiny-note">JPEG, PNG, or WebP up to 8MB. Stored only in session memory.</p>{photo && <div className="photo-preview"><Image src={photo} alt="Citizen evidence photo preview" width={400} height={260} unoptimized /></div>}</Field>
          <Field><FieldLabel htmlFor="observed-status">3. What did you observe?</FieldLabel><select id="observed-status" value={observation} onChange={(e) => setObservation(e.target.value as typeof observation)}><option>Completed</option><option>Ongoing</option><option>Not done</option></select></Field>
          <Field><FieldLabel htmlFor="evidence-notes">4. Field notes</FieldLabel><Textarea id="evidence-notes" value={notes} onChange={(e) => setNotes(e.target.value)} maxLength={500} placeholder="Describe the physical state, signage, or any visible changes." required /></Field>
          {error && <p className="error-note" role="alert">{error}</p>}
          <Button type="submit" size="lg" disabled={photoBusy || gpsBusy || isSubmitting}><ShieldCheck data-icon="inline-start" />{isSubmitting ? "Submitting…" : "Submit for auditor review"}</Button><p className="tiny-note">An uploaded photo or GPS check-in cannot prove authenticity. An auditor manually reviews your evidence before XP is awarded.</p>
        </FieldGroup></form>}
      </DialogContent>
    </Dialog>
  );
}
