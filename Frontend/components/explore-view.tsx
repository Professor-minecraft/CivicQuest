"use client";

import { useEffect, useMemo, useState } from "react";
import dynamic from "next/dynamic";
import Image from "next/image";
import { ArrowDown, ArrowRight, Building2, Check, Clock3, Compass, MapPin, Search, SlidersHorizontal, Sparkles, Trees, Zap } from "lucide-react";
import { PROJECTS, type Project, type Category, type ProjectStatus } from "@/lib/demo-data";
import { api, type BackendProject } from "@/lib/api";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Input } from "@/components/ui/input";
import { ToggleGroup, ToggleGroupItem } from "@/components/ui/toggle-group";
import { cn } from "@/lib/utils";

const ProjectMap = dynamic(() => import("./project-map"), { ssr: false, loading: () => <div className="map-loading"><Compass className="size-8" /><span>Unfolding your neighborhood…</span></div> });

export function ProjectStatusBadge({ status }: { status: string }) {
  return <Badge variant="secondary" data-status={status.toLowerCase()}>{status === "Completed" || status === "approved" || status === "APPROVED" ? <Check data-icon="inline-start" /> : <Clock3 data-icon="inline-start" />}{status}</Badge>;
}

export function ProjectCard({ project, selected, onSelect, onOpen }: { project: Project; selected?: boolean; onSelect?: () => void; onOpen: () => void }) {
  return <article className={cn("project-card", selected && "selected")}>
    <button className="project-photo" onClick={onSelect ?? onOpen} aria-label={`Locate ${project.name} on map`}>
      {project.image ? <Image src={project.image} alt={`Illustrative ${project.category.toLowerCase()} project image, not site evidence`} fill sizes="(max-width: 640px) 100vw, 350px" /> : <div className="project-icon-art"><Building2 /><span>{project.category}</span></div>}
      <span className="project-photo-status"><ProjectStatusBadge status={project.status} /></span>
      <span className="illustration-label">{project.location_source === "approximate" ? "Approx. Location" : "Site Record"}</span>
    </button>
    <div className="project-card-content"><div className="project-category">{project.category === "Parks" ? <Trees /> : <Building2 />}{project.category}</div><h3>{project.name}</h3><p className="project-locality"><MapPin />{project.locality}</p><div className="project-card-footer"><span className="xp-reward"><Zap />150 XP</span><button className="text-action" onClick={onOpen}>View quest<ArrowRight /></button></div></div>
  </article>;
}

export function AdventureHero({ onExplore, onHow }: { onExplore: () => void; onHow: () => void }) {
  return <section className="adventure-hero">
    <div className="hero-copy"><div className="eyebrow"><Sparkles />YOUR NEIGHBORHOOD. YOUR IMPACT.</div><h1>Small quests.<br />A better city.</h1><p>Explore public works. Share what you see.<br className="desktop-break" /> Turn everyday action into real-world impact.</p><div className="hero-actions"><Button size="lg" onClick={onExplore}><Compass data-icon="inline-start" />Find a quest<ArrowRight data-icon="inline-end" /></Button><button className="hero-how" onClick={onHow}>How it works<ArrowRight /></button></div></div>
    <div className="hero-art"><Image src="/images/quest-city.png" alt="Playful miniature neighborhood with community buildings, trees, and a quest location pin" fill priority sizes="(max-width: 640px) 250px, 450px" /></div>
    <div className="hero-reward"><span className="reward-icon"><Zap /></span><div><strong>+150 XP</strong><span>Every approved verification</span></div></div>
  </section>;
}

function mapBackendToProject(bp: BackendProject): Project {
  const budget = bp.amount_disbursed ? `₹ ${(bp.amount_disbursed / 100000).toFixed(1)} lakh` : "₹ 15 lakh";
  let cat: Category = "Infrastructure";
  const rawCat = (bp.work_category || "").toLowerCase();
  if (rawCat.includes("community") || rawCat.includes("hall")) cat = "Community";
  else if (rawCat.includes("park") || rawCat.includes("garden") || rawCat.includes("tree")) cat = "Parks";
  else if (rawCat.includes("school") || rawCat.includes("education") || rawCat.includes("college") || rawCat.includes("room")) cat = "Education";

  // Only use legitimate coordinates; never invent or fallback to arbitrary points
  const parsedLat = bp.latitude != null && !isNaN(Number(bp.latitude)) ? Number(bp.latitude) : NaN;
  const parsedLng = bp.longitude != null && !isNaN(Number(bp.longitude)) ? Number(bp.longitude) : NaN;

  return {
    id: bp.id,
    name: bp.work || "Public Development Work",
    locality: bp.constituency ? `${bp.constituency}, ${bp.state || ""}` : (bp.state || "India"),
    category: cat,
    status: (bp.status === "Ongoing" ? "Ongoing" : "Completed") as ProjectStatus,
    lat: parsedLat,
    lng: parsedLng,
    budget,
    description: bp.work_description || bp.work || "Government development work from public record.",
    image: bp.image && bp.image.startsWith("http") ? bp.image : undefined,
    mp_name: bp.mp_name || undefined,
    constituency: bp.constituency || undefined,
    state: bp.state || undefined,
    location_source: bp.location_source,
    location_accuracy: bp.location_accuracy || undefined,
    completion_date: bp.completion_date || undefined,
    amount_disbursed: bp.amount_disbursed || undefined,
  };
}

export function ExploreView({ onOpen }: { onOpen: (project: Project) => void }) {
  const [liveProjects, setLiveProjects] = useState<Project[]>([]);
  const [states, setStates] = useState<{ state: string; count: number }[]>([]);
  const [selectedState, setSelectedState] = useState<string>("All states");
  const [query, setQuery] = useState("");
  const [status, setStatus] = useState("All works");
  const [category, setCategory] = useState("All categories");
  const [filtersOpen, setFiltersOpen] = useState(false);
  const [selected, setSelected] = useState<Project | null>(null);
  const [showAll, setShowAll] = useState(false);
  const [resetKey, setResetKey] = useState(0);
  const [loading, setLoading] = useState(false);
  const [summaryStats, setSummaryStats] = useState<{
    total_works: number;
    total_states: number;
    total_constituencies: number;
    completed_works: number;
    ongoing_works: number;
  } | null>(null);

  // Load available states and summary stats on mount
  useEffect(() => {
    api.getStates()
      .then((data) => {
        if (data && data.length > 0) {
          setStates(data);
        }
      })
      .catch(() => {});

    api.getSummaryStats()
      .then(setSummaryStats)
      .catch(() => {});
  }, []);

  // Fetch works whenever selectedState or category changes
  useEffect(() => {
    setLoading(true);
    if (selectedState === "All states") {
      {/* Load nationwide works or state-filtered works */}
      api.getMapWorks({ limit: 36000 })
        .then((works) => {
          if (works && works.length > 0) {
            setLiveProjects(works.map(mapBackendToProject));
          }
        })
        .catch(() => {
          // Fallback to local demo projects if offline
        })
        .finally(() => setLoading(false));
    } else {
      // Load works specifically for the selected state
      api.getMapWorks({ state: selectedState, limit: 36000 })
        .then((works) => {
          if (works && works.length > 0) {
            setLiveProjects(works.map(mapBackendToProject));
          }
        })
        .catch(() => {})
        .finally(() => setLoading(false));
    }
  }, [selectedState]);

  const totalDatabaseCount = useMemo(() => {
    return summaryStats?.total_works ?? (states.length > 0 ? states.reduce((sum, s) => sum + s.count, 0) : liveProjects.length);
  }, [summaryStats, states, liveProjects]);

  const sourceProjects = liveProjects.length > 0 ? liveProjects : PROJECTS;

  const filtered = useMemo(() => sourceProjects.filter((p) => (status === "All works" || p.status === status) && (category === "All categories" || p.category === category) && `${p.name} ${p.locality} ${p.category} ${p.description} ${p.constituency || ""} ${p.state || ""}`.toLowerCase().includes(query.toLowerCase().trim())), [sourceProjects, query, status, category]);
  const cards = selected && filtered.some((p) => p.id === selected.id) ? [selected, ...filtered.filter((p) => p.id !== selected.id)] : filtered;

  function handleNearMe(lat: number, lng: number) {
    api.getNearbyProjects(lat, lng, 35)
      .then((nearby) => {
        if (nearby && nearby.length > 0) {
          const mapped = nearby.map(mapBackendToProject);
          setLiveProjects(mapped);
          setSelected(mapped[0]);
        }
      })
      .catch(() => {});
  }

  return <section id="explore" className="explore-section">
    {/* Map Statistics (Part 32: Dynamic from database) */}
    {summaryStats && (
      <div className="map-stats-header">
        <div className="stats-pill">
          <strong>{summaryStats.total_works.toLocaleString()}</strong> Works
        </div>
        <div className="stats-pill">
          <strong>{summaryStats.total_states}</strong> States & UTs
        </div>
        <div className="stats-pill">
          <strong>{summaryStats.total_constituencies}</strong> Constituencies
        </div>
        <div className="stats-pill stats-completed">
          <strong>{summaryStats.completed_works.toLocaleString()}</strong> Completed
        </div>
      </div>
    )}

    <div className="section-heading">
      <div>
        <div className="heading-line">
          <h2>Explore Government Development Works</h2>
          <span className="count-pill">{filtered.length.toLocaleString()} works</span>
        </div>
        <p>Interactive verification map of completed MPLADS development projects across India.</p>
      </div>
    </div>

    {/* Clean Map Toolbar with Search & Filters */}
    <div className="explore-toolbar">
      {/* Search Input (Part 29) */}
      <div style={{ position: "relative", flex: "1 1 240px", minWidth: "220px" }}>
        <Search style={{ position: "absolute", left: "10px", top: "10px", width: "16px", height: "16px", color: "var(--muted-foreground)" }} />
        <Input
          placeholder="Search works, places, constituencies..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          style={{ paddingLeft: "34px", height: "36px", fontSize: "14px", borderRadius: "8px" }}
        />
      </div>

      <ToggleGroup aria-label="Filter works by reported status" value={[status]} onValueChange={(value) => { if (value[0]) { setStatus(value[0]); setSelected(null); } }}>
        <ToggleGroupItem value="All works"><Compass />All</ToggleGroupItem>
        <ToggleGroupItem value="Ongoing"><span className="legend-dot ongoing" />Ongoing</ToggleGroupItem>
        <ToggleGroupItem value="Completed"><span className="legend-dot complete" />Completed</ToggleGroupItem>
      </ToggleGroup>
      
      {/* State Selector */}
      <select
        className="state-select"
        value={selectedState}
        onChange={(e) => {
          setSelectedState(e.target.value);
          setSelected(null);
          setResetKey((n) => n + 1);
        }}
        style={{
          padding: "6px 12px",
          borderRadius: "8px",
          border: "1px solid var(--border)",
          background: "var(--background)",
          color: "var(--foreground)",
          fontSize: "13px",
          fontWeight: "500",
          cursor: "pointer",
          height: "36px"
        }}
      >
        <option value="All states">
          All India {totalDatabaseCount > 0 ? `(${totalDatabaseCount.toLocaleString()} Works)` : ""}
        </option>
        {states.map((s) => (
          <option key={s.state} value={s.state}>
            {s.state} ({s.count.toLocaleString()} works)
          </option>
        ))}
      </select>

      <Button variant="outline" size="sm" onClick={() => setFiltersOpen(!filtersOpen)} aria-expanded={filtersOpen} style={{ height: "36px" }}>
        <SlidersHorizontal data-icon="inline-start" />Filters{category !== "All categories" ? " · active" : ""}
      </Button>
    </div>

    {filtersOpen && <div className="filter-panel">
      <label className="category-label">Category
        <select value={category} onChange={(e) => setCategory(e.target.value)}>
          <option>All categories</option>
          <option>Community</option>
          <option>Parks</option>
          <option>Education</option>
          <option>Infrastructure</option>
        </select>
      </label>
      <Button variant="ghost" size="sm" onClick={() => { setQuery(""); setCategory("All categories"); setStatus("All works"); setSelectedState("All states"); setSelected(null); setResetKey((n) => n + 1); }}>Reset filters</Button>
    </div>}

    <ProjectMap 
      projects={filtered} 
      selected={selected && filtered.some((p) => p.id === selected.id) ? selected : null} 
      onSelect={setSelected} 
      resetKey={resetKey}
      selectedState={selectedState}
      totalDatabaseCount={totalDatabaseCount}
      onOpenQuest={onOpen}
    />
    
    <div id="explore-cards" className="nearby-heading">
      <h3>Discover a little. Make a difference.</h3>
      <span>Public Works in {selectedState} ({cards.length.toLocaleString()})</span>
    </div>

    {cards.length ? (
      <div className="project-grid">
        {(showAll ? cards : cards.slice(0, 4)).map((p) => (
          <ProjectCard key={p.id} project={p} selected={selected?.id === p.id} onSelect={() => setSelected(p)} onOpen={() => onOpen(p)} />
        ))}
      </div>
    ) : (
      <div className="empty-state">
        <Search />
        <h3>No quests found</h3>
        <p>Try another state or reset your search filters.</p>
        <Button variant="outline" onClick={() => { setQuery(""); setStatus("All works"); setCategory("All categories"); setSelectedState("All states"); }}>Reset filters</Button>
      </div>
    )}

    {cards.length > 4 && (
      <Button variant="outline" className="w-full mt-4" onClick={() => setShowAll(!showAll)}>
        {showAll ? "Show fewer works" : `Explore all ${cards.length.toLocaleString()} works`}
        <ArrowDown data-icon="inline-end" />
      </Button>
    )}
    <p className="data-disclaimer">Official MPLADS public records from Works Completed.csv. Georeferenced via open parliamentary boundaries.</p>
  </section>;
}
