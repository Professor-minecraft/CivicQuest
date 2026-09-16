"use client";

import { useEffect, useState, useMemo } from "react";
import { MapContainer, TileLayer, CircleMarker, Tooltip, useMap, useMapEvents } from "react-leaflet";
import L from "leaflet";
import { LocateFixed, Minus, Navigation, Plus, ShieldCheck, X } from "lucide-react";
import { type Project } from "@/lib/demo-data";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { toast } from "sonner";
import "leaflet/dist/leaflet.css";

// India geographic boundary framing (includes all states and union territories)
export const INDIA_BOUNDS: [[number, number], [number, number]] = [
  [6.5, 68.0],
  [36.0, 97.5]
];
export const INDIA_CENTER: [number, number] = [22.0, 78.9629];

function ZoomTracker({ onZoomChange }: { onZoomChange: (z: number) => void }) {
  useMapEvents({
    zoomend(e) {
      onZoomChange(e.target.getZoom());
    }
  });
  return null;
}

function MapControls({
  selected,
  resetKey,
  projects,
  selectedState,
  onNearMe
}: {
  selected: Project | null;
  resetKey: number;
  projects: Project[];
  selectedState?: string;
  onNearMe?: (lat: number, lng: number) => void;
}) {
  const map = useMap();
  const [locating, setLocating] = useState(false);

  // Invalidate size on mount to ensure Leaflet computes exact container dimensions
  useEffect(() => {
    const timer = setTimeout(() => {
      map.invalidateSize();
      map.fitBounds(INDIA_BOUNDS, { padding: [16, 16] });
    }, 100);
    return () => clearTimeout(timer);
  }, [map]);

  // Selected single project fly-to
  useEffect(() => {
    if (selected && typeof selected.lat === "number" && typeof selected.lng === "number" && !isNaN(selected.lat)) {
      map.flyTo([selected.lat, selected.lng], Math.max(map.getZoom(), 12), { duration: 0.6 });
    }
  }, [selected, map]);

  // Viewport bounds on state change or reset
  useEffect(() => {
    if (selectedState && selectedState !== "All states") {
      const valid = projects.filter((p) => typeof p.lat === "number" && typeof p.lng === "number" && !isNaN(p.lat));
      if (valid.length > 1) {
        const bounds = L.latLngBounds(valid.map((p) => [p.lat, p.lng]));
        if (bounds.isValid()) {
          map.fitBounds(bounds, { padding: [40, 40], maxZoom: 10 });
          return;
        }
      }
    }
    // Default initial and reset: frame the entire country of India
    map.fitBounds(INDIA_BOUNDS, { padding: [16, 16] });
  }, [resetKey, selectedState, map]);

  function handleLocate() {
    if (!navigator.geolocation) {
      toast.error("Geolocation is not supported by this browser.");
      return;
    }
    setLocating(true);
    navigator.geolocation.getCurrentPosition(
      (pos) => {
        setLocating(false);
        const { latitude, longitude } = pos.coords;
        map.flyTo([latitude, longitude], 12, { duration: 1.0 });
        if (onNearMe) onNearMe(latitude, longitude);
        toast.success("Centered on your location", {
          description: "Displaying nearby public works."
        });
      },
      () => {
        setLocating(false);
        toast.error("Could not access your location", {
          description: "Location permission was denied or unavailable."
        });
      },
      { timeout: 10000, enableHighAccuracy: true }
    );
  }

  return (
    <div className="map-controls">
      <Button variant="outline" size="icon" aria-label="Zoom in" onClick={() => map.zoomIn()}><Plus /></Button>
      <Button variant="outline" size="icon" aria-label="Zoom out" onClick={() => map.zoomOut()}><Minus /></Button>
      <Button
        variant="outline"
        size="icon"
        aria-label="Frame all of India"
        title="Frame India"
        onClick={() => {
          map.fitBounds(INDIA_BOUNDS, { padding: [16, 16] });
        }}
      >
        <LocateFixed />
      </Button>
      <Button
        variant="outline"
        size="icon"
        aria-label="Works near me"
        title="Works near me (GPS)"
        disabled={locating}
        onClick={handleLocate}
      >
        <Navigation className="size-4" style={{ transform: "rotate(45deg)" }} />
      </Button>
    </div>
  );
}

export default function ProjectMap({
  projects,
  selected,
  onSelect,
  resetKey,
  selectedState = "All states",
  totalDatabaseCount,
  onOpenQuest
}: {
  projects: Project[];
  selected: Project | null;
  onSelect: (project: Project | null) => void;
  resetKey: number;
  selectedState?: string;
  totalDatabaseCount?: number;
  onOpenQuest?: (project: Project) => void;
}) {
  const [tileError, setTileError] = useState(false);
  const [zoomLevel, setZoomLevel] = useState(5);

  // Never plot projects with missing or non-numeric coordinates
  const validProjects = useMemo(() => {
    return projects.filter(
      (p) => typeof p.lat === "number" && typeof p.lng === "number" && !isNaN(p.lat) && !isNaN(p.lng)
    );
  }, [projects]);

  // Small, clean CivicQuest green dots (unobtrusive dot density)
  const baseRadius = zoomLevel < 6 ? 2.5 : zoomLevel < 8 ? 3.5 : 5;

  return (
    <div className="map-frame" aria-label="Interactive map of public works">
      <MapContainer
        bounds={INDIA_BOUNDS}
        boundsOptions={{ padding: [16, 16] }}
        zoomControl={false}
        scrollWheelZoom={true}
        preferCanvas={true}
        className="project-map"
      >
        {/* Standard OpenStreetMap TileLayer without API keys */}
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          eventHandlers={{
            tileerror: () => setTileError(true),
            load: () => setTileError(false),
          }}
        />

        <ZoomTracker onZoomChange={setZoomLevel} />

        {/* Individual clean green / orange dots for each government work */}
        {validProjects.map((p) => {
          const isSelected = selected?.id === p.id;
          const isCompleted = p.status === "Completed";
          const isApprox = (p.location_source || "").toUpperCase() === "APPROXIMATE";

          // CivicQuest color language:
          // Completed -> Clean Green (#22c55e / #16a34a)
          // Ongoing -> Clean Orange (#f97316 / #ea580c)
          const dotFill = isCompleted ? "#22c55e" : "#f97316";
          const dotStroke = isSelected ? "#0f172a" : isCompleted ? "#15803d" : "#c2410c";

          return (
            <CircleMarker
              key={p.id}
              center={[p.lat, p.lng]}
              radius={isSelected ? baseRadius + 3 : baseRadius}
              pathOptions={{
                color: dotStroke,
                fillColor: dotFill,
                fillOpacity: isSelected ? 1 : 0.85,
                weight: isSelected ? 2.5 : 1,
              }}
              eventHandlers={{
                click: () => onSelect(p),
              }}
            >
              {/* Compact, clean hover tooltip */}
              <Tooltip
                direction="top"
                offset={[0, -4]}
                opacity={0.98}
                className="civic-clean-tooltip"
              >
                <div className="tooltip-card">
                  <div className="tooltip-line">
                    <span className="tooltip-key">Place:</span> {p.locality || p.constituency || "India"}{p.state ? `, ${p.state}` : ""}
                  </div>
                  <div className="tooltip-line">
                    <span className="tooltip-key">Project:</span> {p.name}
                  </div>
                  {p.constituency && (
                    <div className="tooltip-line">
                      <span className="tooltip-key">Constituency:</span> {p.constituency}
                    </div>
                  )}
                  {p.mp_name && (
                    <div className="tooltip-line">
                      <span className="tooltip-key">MP:</span> {p.mp_name}
                    </div>
                  )}
                  {isApprox && (
                    <div className="tooltip-approx">
                      <span>⚠️</span> Approximate location
                    </div>
                  )}
                </div>
              </Tooltip>
            </CircleMarker>
          );
        })}

        <MapControls
          selected={selected}
          resetKey={resetKey}
          projects={validProjects}
          selectedState={selectedState}
        />
      </MapContainer>

      {/* Floating Work Detail Side Panel (Part 28) */}
      {selected && (
        <div className="map-detail-card" aria-label="Selected work details">
          <div className="detail-card-header">
            <div style={{ minWidth: 0, flex: 1 }}>
              <h4>{selected.name}</h4>
              <p>{selected.constituency ? `${selected.constituency}, ` : ""}{selected.state || "India"}</p>
            </div>
            <button className="detail-card-close" onClick={() => onSelect(null)} aria-label="Close details">
              <X className="size-4" />
            </button>
          </div>

          <div className="detail-card-metrics">
            <div className="metric-row">
              <span className="metric-label">Status</span>
              <Badge variant="secondary" data-status={selected.status.toLowerCase()}>
                {selected.status}
              </Badge>
            </div>
            {selected.budget && (
              <div className="metric-row">
                <span className="metric-label">Amount</span>
                <strong>{selected.budget}</strong>
              </div>
            )}
            {selected.completion_date && (
              <div className="metric-row">
                <span className="metric-label">Completed</span>
                <span>{selected.completion_date}</span>
              </div>
            )}
            {selected.constituency && (
              <div className="metric-row">
                <span className="metric-label">Constituency</span>
                <span>{selected.constituency}</span>
              </div>
            )}
            {selected.mp_name && (
              <div className="metric-row">
                <span className="metric-label">MP</span>
                <span>{selected.mp_name}</span>
              </div>
            )}
          </div>

          <div className="detail-card-verification">
            <span className="verification-title">Citizen verification</span>
            {(selected.location_source || "").toUpperCase() === "APPROXIMATE" ? (
              <Badge variant="secondary" className="badge-approx">
                ⚠️ Approximate location ({selected.location_accuracy || "Constituency Centroid"})
              </Badge>
            ) : (
              <Badge variant="secondary" className="badge-verified">
                ✓ Verified site record
              </Badge>
            )}
          </div>

          <div className="detail-card-actions">
            <Button
              size="sm"
              variant="outline"
              onClick={() => {
                document.getElementById("explore-cards")?.scrollIntoView({ behavior: "smooth" });
              }}
            >
              View details
            </Button>
            <Button
              size="sm"
              onClick={() => {
                if (onOpenQuest) onOpenQuest(selected);
              }}
            >
              <ShieldCheck className="size-4 mr-1" />
              Verify this work
            </Button>
          </div>
        </div>
      )}

      {/* Dynamic Data Counter - never hardcodes figures */}
      <div className="map-location">
        <span className="live-dot" />
        {selectedState && selectedState !== "All states" ? (
          `${selectedState} · ${validProjects.length.toLocaleString()} works on map`
        ) : (
          `MPLADS Works Map · ${totalDatabaseCount ? totalDatabaseCount.toLocaleString() : validProjects.length.toLocaleString()} works recorded`
        )}
      </div>

      {/* Minimal clean unobtrusive legend */}
      <div className="map-legend">
        <span><i className="legend-dot complete" />Completed</span>
        <span><i className="legend-dot ongoing" />Ongoing</span>
        <span><span style={{ color: "#d97706", fontWeight: "700", marginRight: "3px" }}>⚠️</span>Approximate</span>
      </div>

      {tileError && (
        <p className="map-error" role="status">
          Map tiles are currently loading or offline. Government works remain fully interactive below.
        </p>
      )}
    </div>
  );
}
