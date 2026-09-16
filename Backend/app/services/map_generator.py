"""
CivicQuest Map Generator using Folium and Pandas
Generates high-performance interactive maps for all MPLADS works from Works Completed.csv.
Uses open-source OpenStreetMap and CARTO tiles - ZERO paid APIs or API keys.
"""

import json
import logging
import re
from pathlib import Path
from typing import Optional, Dict, Any, Tuple
import pandas as pd
import folium
from folium.plugins import FastMarkerCluster, MarkerCluster, Fullscreen, MiniMap, Search

logger = logging.getLogger("civicquest.map_generator")

INDIA_CENTER = [22.5937, 78.9629]
DEFAULT_ZOOM = 5

def clean_rupees(val: Any) -> float:
    if pd.isna(val):
        return 0.0
    s = str(val).replace(",", "").replace("₹", "").replace("?", "").strip()
    try:
        return float(s)
    except (ValueError, TypeError):
        return 0.0

def generate_interactive_map(
    csv_path: Optional[Path] = None,
    centroids_path: Optional[Path] = None,
    output_html_path: Optional[Path] = None,
    include_individual_clusters: bool = True
) -> folium.Map:
    """
    Builds a complete Folium map taking data from Works Completed.csv,
    assigning coordinates via Parliamentary Constituency centroids, and
    rendering both Constituency Hubs and FastMarkerCluster of all works.
    """
    base_dir = Path(__file__).resolve().parent.parent.parent
    if csv_path is None:
        csv_path = base_dir / "Works Completed.csv"
        if not csv_path.exists():
            csv_path = base_dir / "Backend" / "data" / "Works Completed.csv"

    if centroids_path is None:
        centroids_path = base_dir / "Backend" / "data" / "constituency_centroids.json"

    # Load Centroids
    with open(centroids_path, "r", encoding="utf-8") as f:
        centroids: Dict[str, Dict[str, float]] = json.load(f)

    # Read CSV
    print(f"Reading {csv_path}...")
    df = pd.read_csv(csv_path, encoding="utf-8-sig")
    print(f"Total rows in CSV: {len(df)}")

    # Clean amount column
    amt_col = [c for c in df.columns if "Amount" in c]
    amt_name = amt_col[0] if amt_col else "Amount Disbursed ( ₹ )"
    df["clean_amount"] = df[amt_name].apply(clean_rupees)
    
    mp_col = [c for c in df.columns if "Parliament" in c or "MP" in c or "Member" in c]
    mp_name = mp_col[0] if mp_col else "Hon'ble Members of Parliament"

    # Match coordinates
    def get_coords(constituency: Any) -> Tuple[Optional[float], Optional[float]]:
        if pd.isna(constituency):
            return None, None
        norm = str(constituency).strip().upper()
        if norm in centroids:
            return centroids[norm]["lat"], centroids[norm]["lng"]
        clean_norm = re.sub(r'\s*\((?:SC|ST)\)\s*', '', norm).strip()
        if clean_norm in centroids:
            return centroids[clean_norm]["lat"], centroids[clean_norm]["lng"]
        return None, None

    coords = df["Constituency"].apply(get_coords)
    df["lat"] = [c[0] for c in coords]
    df["lng"] = [c[1] for c in coords]

    valid_df = df[df["lat"].notnull() & df["lng"].notnull()].copy()
    print(f"Works mapped to geographical locations: {len(valid_df)} / {len(df)}")

    # Initialize Folium Map with OpenStreetMap / CARTO Voyager
    m = folium.Map(
        location=INDIA_CENTER,
        zoom_start=DEFAULT_ZOOM,
        tiles=None,
        control_scale=True,
        prefer_canvas=True
    )

    # Add open tile layers
    folium.TileLayer(
        tiles="https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png",
        attr='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> &copy; <a href="https://carto.com/attributions">CARTO</a>',
        name="CARTO Voyager (Clean)",
        control=True
    ).add_to(m)

    folium.TileLayer(
        tiles="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
        attr='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
        name="OpenStreetMap Standard",
        control=True
    ).add_to(m)

    # FeatureGroup 1: Constituency Hubs (aggregated view of all 504 constituencies)
    hubs_group = folium.FeatureGroup(name="🏛️ Parliamentary Constituency Hubs (All Works)", show=True)

    # Aggregate by constituency
    grouped = valid_df.groupby("Constituency").agg(
        work_count=("Work", "count"),
        total_amount=("clean_amount", "sum"),
        state=("State", "first"),
        mp_name=(mp_name, "first"),
        lat=("lat", "first"),
        lng=("lng", "first")
    ).reset_index()

    for _, row in grouped.iterrows():
        c_name = row["Constituency"]
        c_works = row["work_count"]
        c_amt = row["total_amount"]
        c_state = row["state"]
        c_mp = row["mp_name"]
        lat = row["lat"]
        lng = row["lng"]

        amt_str = f"₹ {(c_amt / 10000000):.2f} Cr" if c_amt >= 10000000 else f"₹ {(c_amt / 100000):.1f} Lakh"

        # Responsive card popup
        popup_html = f"""
        <div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; min-width: 240px; max-width: 320px;">
            <div style="background: #1e293b; color: #fff; padding: 10px 14px; border-radius: 8px 8px 0 0;">
                <span style="font-size: 11px; text-transform: uppercase; letter-spacing: 0.5px; opacity: 0.8;">{c_state}</span>
                <h4 style="margin: 2px 0 0 0; font-size: 16px; font-weight: 700;">{c_name}</h4>
            </div>
            <div style="padding: 12px 14px; background: #ffffff; border: 1px solid #e2e8f0; border-top: none; border-radius: 0 0 8px 8px; font-size: 13px;">
                <p style="margin: 0 0 6px 0;"><strong>MP:</strong> {c_mp if pd.notna(c_mp) else 'N/A'}</p>
                <p style="margin: 0 0 6px 0;"><strong>Completed Works:</strong> <span style="color: #059669; font-weight: 700;">{c_works}</span></p>
                <p style="margin: 0 0 8px 0;"><strong>Total Disbursed:</strong> <span style="font-weight: 600;">{amt_str}</span></p>
                <div style="background: #f8fafc; border-left: 3px solid #3b82f6; padding: 6px 8px; font-size: 11px; color: #64748b;">
                    ⚠️ Approximate location (Constituency Centroid via OpenGIS)
                </div>
            </div>
        </div>
        """

        # Choose marker color based on count
        color = "green" if c_works > 50 else "blue" if c_works > 20 else "orange"

        folium.CircleMarker(
            location=[lat, lng],
            radius=max(6, min(22, int(c_works ** 0.45 * 3))),
            popup=folium.Popup(popup_html, max_width=350),
            tooltip=f"{c_name} ({c_state}): {c_works} works completed",
            color="#1e293b",
            weight=1.5,
            fill=True,
            fill_color=color,
            fill_opacity=0.75
        ).add_to(hubs_group)

    hubs_group.add_to(m)

    # FeatureGroup 2: FastMarkerCluster of all 35,292 individual works
    if include_individual_clusters:
        cluster_group = folium.FeatureGroup(name="📍 All Individual Works (35,292 Points Clustered)", show=False)
        
        # Prepare list of coordinates for FastMarkerCluster
        cluster_points = []
        cluster_popups = []
        
        for _, row in valid_df.iterrows():
            cluster_points.append([row["lat"], row["lng"]])
            work_title = str(row["Work"]).replace('"', '&quot;').replace("'", "&#39;")[:80]
            cluster_popups.append(f"{work_title} | {row['Constituency']}")

        FastMarkerCluster(
            data=cluster_points,
            popups=cluster_popups,
            name="Clustered Works"
        ).add_to(cluster_group)

        cluster_group.add_to(m)

    # Add interactive plugins
    Fullscreen(position="topleft").add_to(m)
    folium.LayerControl(position="topright", collapsed=False).add_to(m)

    # Title header overlay
    header_html = """
    <div style="position: fixed; 
                top: 15px; left: 60px; width: auto; 
                background: rgba(255, 255, 255, 0.95);
                backdrop-filter: blur(8px);
                border: 1px solid #cbd5e1;
                border-radius: 12px;
                padding: 10px 18px;
                box-shadow: 0 4px 14px rgba(0, 0, 0, 0.12);
                z-index: 1000;
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
        <div style="display: flex; align-items: center; gap: 8px;">
            <div style="width: 10px; height: 10px; border-radius: 50%; background: #10b981; animation: pulse 2s infinite;"></div>
            <h3 style="margin: 0; font-size: 15px; font-weight: 700; color: #0f172a;">CivicQuest National MPLADS Map</h3>
        </div>
        <div style="font-size: 11px; color: #64748b; margin-top: 3px;">
            Data Source: <strong>Works Completed.csv</strong> · 35,292 Works across 504 Constituencies
        </div>
    </div>
    """
    m.get_root().html.add_child(folium.Element(header_html))

    if output_html_path:
        output_html_path.parent.mkdir(parents=True, exist_ok=True)
        m.save(str(output_html_path))
        print(f"Interactive Folium map saved to: {output_html_path}")

    return m

if __name__ == "__main__":
    generate_interactive_map()
