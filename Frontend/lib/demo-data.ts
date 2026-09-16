export type ProjectStatus = "Ongoing" | "Completed";
export type Category = "Community" | "Parks" | "Education" | "Infrastructure";
export type Project = {
  id: string; name: string; locality: string; category: Category;
  status: ProjectStatus; lat: number; lng: number; budget: string;
  description: string; image?: string;
  mp_name?: string; constituency?: string; state?: string;
  location_source?: string; location_accuracy?: string;
  completion_date?: string; amount_disbursed?: number;
};

export const CITY_CENTER: [number, number] = [22.5937, 78.9629]; // Center of India
export const PROJECTS: Project[] = [
  { id: "CQ-001", name: "Indiranagar Community Hall", locality: "Indiranagar", category: "Community", status: "Ongoing", lat: 12.9784, lng: 77.6392, budget: "₹ 25 lakh", description: "A shared space for neighborhood meetings, community events, and skill-building workshops. Check the entrance, accessibility ramp, and overall construction progress.", image: "/images/community-hall.png" },
  { id: "CQ-002", name: "Domlur Neighborhood Park", locality: "Domlur", category: "Parks", status: "Completed", lat: 12.9610, lng: 77.6369, budget: "₹ 18 lakh", description: "New walking paths, play equipment, and seating for a greener neighborhood. Check whether the paths and equipment are complete and usable.", image: "/images/neighborhood-park.png" },
  { id: "CQ-003", name: "Ulsoor Public Library", locality: "Ulsoor", category: "Education", status: "Ongoing", lat: 12.9850, lng: 77.6191, budget: "₹ 12 lakh", description: "A neighborhood reading room with accessible entry and study spaces. Document visible progress without entering restricted construction areas." },
  { id: "CQ-004", name: "Richmond Town Footpath", locality: "Richmond Town", category: "Infrastructure", status: "Completed", lat: 12.9601, lng: 77.6031, budget: "₹ 9 lakh", description: "A safer pedestrian route with curb ramps and upgraded paving. Review the surface, continuity, and accessibility of the footpath." },
  { id: "CQ-005", name: "Shivajinagar Drinking Water Point", locality: "Shivajinagar", category: "Infrastructure", status: "Ongoing", lat: 12.9894, lng: 77.6040, budget: "₹ 6 lakh", description: "A public drinking water point for the surrounding neighborhood. Photograph visible installation progress; do not make assumptions about water quality." },
  { id: "CQ-006", name: "Cubbon Reading Garden", locality: "Cubbon Park", category: "Parks", status: "Completed", lat: 12.9764, lng: 77.5924, budget: "₹ 14 lakh", description: "Outdoor seating and landscaped reading areas. Review the condition of seating, walkways, and public access.", image: "/images/neighborhood-park.png" },
  { id: "CQ-007", name: "Austin Town Learning Center", locality: "Austin Town", category: "Education", status: "Ongoing", lat: 12.9549, lng: 77.6190, budget: "₹ 20 lakh", description: "A new after-school learning space. Document external construction progress and accessibility from a safe public location.", image: "/images/community-hall.png" },
  { id: "CQ-008", name: "Vasanth Nagar Street Lighting", locality: "Vasanth Nagar", category: "Infrastructure", status: "Completed", lat: 12.9942, lng: 77.5918, budget: "₹ 8 lakh", description: "Replacement street lighting along neighborhood roads. Check visible installation and note whether lights are working if you visit after dark." },
];

export function distanceMeters(a: { lat: number; lng: number }, b: { lat: number; lng: number }) {
  const rad = (degrees: number) => degrees * Math.PI / 180;
  const dLat = rad(b.lat - a.lat);
  const dLng = rad(b.lng - a.lng);
  const h = Math.sin(dLat / 2) ** 2 + Math.cos(rad(a.lat)) * Math.cos(rad(b.lat)) * Math.sin(dLng / 2) ** 2;
  return 6371000 * 2 * Math.atan2(Math.sqrt(h), Math.sqrt(1 - h));
}
