export const API_BASE =
  process.env.NEXT_PUBLIC_API_URL || "https://civicquest-backend.onrender.com";

export type UserRole = "USER" | "AUDITOR" | "ADMIN";

export interface UserProfile {
  id: number;
  name: string;
  email: string;
  role: UserRole;
  xp: number;
  level: number;
  created_at?: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
  user: UserProfile;
}

export interface BackendProject {
  id: string;
  sr_no?: number | null;
  work_category?: string | null;
  work?: string | null;
  state?: string | null;
  ida?: string | null;
  work_description?: string | null;
  mp_name?: string | null;
  constituency?: string | null;
  image?: string | null;
  completion_date?: string | null;
  amount_disbursed?: number | null;
  latitude?: number | null;
  longitude?: number | null;
  location_source?: string;
  location_accuracy?: string | null;
  status?: string;
}

export interface BackendSubmission {
  id: string;
  user_id: number;
  project_id: string;
  photo_url: string;
  file_name?: string;
  observation: "Completed" | "Ongoing" | "Not done";
  notes: string;
  check_in_type: "gps" | "simulated";
  gps_latitude?: number | null;
  gps_longitude?: number | null;
  gps_accuracy?: number | null;
  distance_from_project?: number | null;
  gps_verification_status?: string | null;
  status: "PENDING" | "APPROVED" | "REJECTED";
  submitted_at: string;
  reviewed_at?: string | null;
  reviewed_by?: number | null;
  review_feedback?: string | null;
  project?: BackendProject;
}

export interface LeaderboardUser {
  id: number;
  name: string;
  xp: number;
  level: number;
  role: string;
  approved_count: number;
}

export interface NotificationItem {
  id: number;
  title: string;
  message: string;
  type: string;
  is_read: boolean;
  created_at: string;
}

export interface CertificateItem {
  id: string;
  citizen_name: string;
  achievement: string;
  approved_verifications_count: number;
  issue_date: string;
  certificate_code: string;
}

export interface AdminStats {
  total_projects: number;
  total_users: number;
  total_auditors: number;
  pending_reviews: number;
  approved_reviews: number;
  rejected_reviews: number;
  total_xp_awarded: number;
}

function getAuthHeader(): HeadersInit {
  if (typeof window === "undefined") return {};
  const token = localStorage.getItem("civicquest_token");
  return token ? { Authorization: `Bearer ${token}` } : {};
}

export interface MapHub {
  constituency: string;
  state: string;
  mp_name?: string | null;
  work_count: number;
  latitude?: number | null;
  longitude?: number | null;
}

export const api = {
  // --- Auth ---
  async login(email: string, password: string): Promise<AuthResponse> {
    const res = await fetch(`${API_BASE}/api/auth/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password }),
    });

    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: "Login failed" }));
      throw new Error(err.detail || "Invalid credentials");
    }

    return res.json();
  },

  async register(name: string, email: string, password: string): Promise<AuthResponse> {
    const res = await fetch(`${API_BASE}/api/auth/register`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name, email, password }),
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: "Registration failed" }));
      throw new Error(err.detail || "Registration failed");
    }
    return res.json();
  },

  async getMe(): Promise<UserProfile> {
    const res = await fetch(`${API_BASE}/api/auth/me`, {
      headers: { ...getAuthHeader() },
    });
    if (!res.ok) throw new Error("Unauthorized");
    return res.json();
  },

  async logout(): Promise<void> {
    try {
      await fetch(`${API_BASE}/api/auth/logout`, { method: "POST" });
    } catch { }
    if (typeof window !== "undefined") {
      localStorage.removeItem("civicquest_token");
    }
  },

  // --- Projects ---
  async getProjects(params?: {
    search?: string;
    category?: string;
    status?: string;
    state?: string;
    constituency?: string;
    has_coords?: boolean;
    limit?: number;
  }): Promise<{ total: number; projects: BackendProject[] }> {
    const query = new URLSearchParams();
    if (params?.search) query.append("search", params.search);
    if (params?.category && params.category !== "All categories") query.append("category", params.category);
    if (params?.status && params.status !== "All works") query.append("status", params.status);
    if (params?.state) query.append("state", params.state);
    if (params?.constituency) query.append("constituency", params.constituency);
    if (params?.has_coords !== undefined) query.append("has_coords", String(params.has_coords));
    query.append("limit", String(params?.limit || 100));

    const res = await fetch(`${API_BASE}/api/projects?${query.toString()}`);
    if (!res.ok) throw new Error("Failed to load projects");
    return res.json();
  },

  async getStates(): Promise<{ state: string; count: number }[]> {
    const res = await fetch(`${API_BASE}/api/projects/states`);
    if (!res.ok) return [];
    return res.json();
  },

  async getMapHubs(): Promise<MapHub[]> {
    const res = await fetch(`${API_BASE}/api/projects/map-hubs`);
    if (!res.ok) return [];
    return res.json();
  },

  async getMapWorks(params?: {
    state?: string;
    constituency?: string;
    category?: string;
    search?: string;
    limit?: number;
  }): Promise<BackendProject[]> {
    const query = new URLSearchParams();
    if (params?.state && params.state !== "All states") query.append("state", params.state);
    if (params?.constituency && params.constituency !== "All") query.append("constituency", params.constituency);
    if (params?.category && params.category !== "All categories") query.append("category", params.category);
    if (params?.search) query.append("search", params.search);
    query.append("limit", String(params?.limit || 1000));

    const res = await fetch(`${API_BASE}/api/projects/map-works?${query.toString()}`);
    if (!res.ok) return [];
    return res.json();
  },

  async getSummaryStats(): Promise<{
    total_works: number;
    total_states: number;
    total_constituencies: number;
    completed_works: number;
    ongoing_works: number;
  }> {
    const res = await fetch(`${API_BASE}/api/projects/summary-stats`);
    if (!res.ok) {
      return { total_works: 35293, total_states: 35, total_constituencies: 504, completed_works: 34800, ongoing_works: 493 };
    }
    return res.json();
  },

  async getNearbyProjects(lat: number, lng: number, radiusKm = 25): Promise<BackendProject[]> {
    const res = await fetch(`${API_BASE}/api/projects/nearby?lat=${lat}&lng=${lng}&radius_km=${radiusKm}`);
    if (!res.ok) return [];
    return res.json();
  },

  async getProject(id: string): Promise<BackendProject> {
    const res = await fetch(`${API_BASE}/api/projects/${id}`);
    if (!res.ok) throw new Error("Project not found");
    return res.json();
  },

  // --- Submissions ---
  async submitVerification(formData: FormData): Promise<BackendSubmission> {
    const res = await fetch(`${API_BASE}/api/submissions`, {
      method: "POST",
      headers: { ...getAuthHeader() },
      body: formData,
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: "Submission failed" }));
      throw new Error(err.detail || "Submission failed");
    }
    return res.json();
  },

  async getMySubmissions(): Promise<BackendSubmission[]> {
    const res = await fetch(`${API_BASE}/api/submissions/my`, {
      headers: { ...getAuthHeader() },
    });
    if (!res.ok) throw new Error("Failed to fetch your quests");
    return res.json();
  },

  // --- Audits ---
  async getPendingAudits(): Promise<BackendSubmission[]> {
    const res = await fetch(`${API_BASE}/api/audits/pending`, {
      headers: { ...getAuthHeader() },
    });
    if (!res.ok) throw new Error("Failed to fetch pending audits");
    return res.json();
  },

  async getAuditHistory(): Promise<BackendSubmission[]> {
    const res = await fetch(`${API_BASE}/api/audits/history`, {
      headers: { ...getAuthHeader() },
    });
    if (!res.ok) throw new Error("Failed to fetch audit history");
    return res.json();
  },

  async approveSubmission(id: string, feedback?: string): Promise<BackendSubmission> {
    const res = await fetch(`${API_BASE}/api/audits/${id}/approve`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        ...getAuthHeader(),
      },
      body: JSON.stringify({ decision: "approved", feedback: feedback || "" }),
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: "Approval failed" }));
      throw new Error(err.detail || "Approval failed");
    }
    return res.json();
  },

  async rejectSubmission(id: string, feedback: string): Promise<BackendSubmission> {
    const res = await fetch(`${API_BASE}/api/audits/${id}/reject`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        ...getAuthHeader(),
      },
      body: JSON.stringify({ decision: "rejected", feedback }),
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: "Rejection failed" }));
      throw new Error(err.detail || "Rejection failed");
    }
    return res.json();
  },

  // --- Leaderboard ---
  async getLeaderboard(): Promise<LeaderboardUser[]> {
    const res = await fetch(`${API_BASE}/api/leaderboard`);
    if (!res.ok) throw new Error("Failed to load leaderboard");
    const data = await res.json();
    return data.leaders;
  },

  // --- Notifications ---
  async getNotifications(): Promise<NotificationItem[]> {
    const res = await fetch(`${API_BASE}/api/notifications`, {
      headers: { ...getAuthHeader() },
    });
    if (!res.ok) return [];
    return res.json();
  },

  async markNotificationRead(id: number): Promise<void> {
    await fetch(`${API_BASE}/api/notifications/${id}/read`, {
      method: "PATCH",
      headers: { ...getAuthHeader() },
    });
  },

  // --- Certificates ---
  async getCertificates(): Promise<CertificateItem[]> {
    const res = await fetch(`${API_BASE}/api/certificates`, {
      headers: { ...getAuthHeader() },
    });
    if (!res.ok) return [];
    return res.json();
  },

  getCertificateDownloadUrl(id: string): string {
    return `${API_BASE}/api/certificates/${id}/download`;
  },

  // --- Admin ---
  async getAdminStats(): Promise<AdminStats> {
    const res = await fetch(`${API_BASE}/api/admin/stats`, {
      headers: { ...getAuthHeader() },
    });
    if (!res.ok) throw new Error("Failed to fetch admin statistics");
    return res.json();
  },

  async getAdminUsers(role?: string): Promise<UserProfile[]> {
    const q = role ? `?role=${role}` : "";
    const res = await fetch(`${API_BASE}/api/admin/users${q}`, {
      headers: { ...getAuthHeader() },
    });
    if (!res.ok) throw new Error("Failed to fetch users");
    return res.json();
  },

  async updateUserRole(userId: number, role: UserRole): Promise<UserProfile> {
    const res = await fetch(`${API_BASE}/api/admin/users/${userId}`, {
      method: "PATCH",
      headers: {
        "Content-Type": "application/json",
        ...getAuthHeader(),
      },
      body: JSON.stringify({ role }),
    });
    if (!res.ok) throw new Error("Failed to update user role");
    return res.json();
  },
};
