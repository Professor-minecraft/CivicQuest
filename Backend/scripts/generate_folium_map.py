"""
Command-line script to generate the interactive Folium map from Works Completed.csv.
Saves to Frontend/public/works_map.html and Backend/data/works_map.html.
"""

import sys
from pathlib import Path

# Add Backend to sys.path
backend_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(backend_dir))

from app.services.map_generator import generate_interactive_map

def main():
    root_dir = backend_dir.parent
    csv_path = root_dir / "Works Completed.csv"
    if not csv_path.exists():
        csv_path = backend_dir / "data" / "Works Completed.csv"

    centroids_path = backend_dir / "data" / "constituency_centroids.json"
    frontend_out = root_dir / "Frontend" / "public" / "works_map.html"
    backend_out = backend_dir / "data" / "works_map.html"

    print("==================================================")
    print("Generating CivicQuest Interactive Folium Map")
    print(f"CSV Path:       {csv_path}")
    print(f"Centroids:      {centroids_path}")
    print("==================================================")

    m = generate_interactive_map(
        csv_path=csv_path,
        centroids_path=centroids_path,
        output_html_path=frontend_out
    )

    # Also copy or save to backend data
    backend_out.parent.mkdir(parents=True, exist_ok=True)
    m.save(str(backend_out))
    print(f"Also saved copy to: {backend_out}")
    print("Map generation successfully completed!")

if __name__ == "__main__":
    main()
