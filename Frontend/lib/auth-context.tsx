"use client";

import React, { createContext, useContext, useEffect, useState } from "react";
import { api, type UserProfile } from "./api";

interface AuthContextType {
  user: UserProfile | null;
  token: string | null;
  loading: boolean;
  login: (email: string, pass: string) => Promise<UserProfile>;
  register: (name: string, email: string, pass: string) => Promise<UserProfile>;
  logout: () => Promise<void>;
  refreshUser: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [token, setToken] = useState<string | null>(() => {
    if (typeof window !== "undefined") {
      return localStorage.getItem("civicquest_token");
    }
    return null;
  });
  const [user, setUser] = useState<UserProfile | null>(null);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    if (!token) {
      setLoading(false);
      return;
    }

    api.getMe()
      .then((profile) => setUser(profile))
      .catch(() => {
        if (typeof window !== "undefined") {
          localStorage.removeItem("civicquest_token");
        }
        setToken(null);
        setUser(null);
      })
      .finally(() => {
        setLoading(false);
      });
  }, [token]);

  async function login(email: string, pass: string) {
    setLoading(true);
    try {
      const data = await api.login(email, pass);
      localStorage.setItem("civicquest_token", data.access_token);
      setToken(data.access_token);
      setUser(data.user);
      return data.user;
    } finally {
      setLoading(false);
    }
  }

  async function register(name: string, email: string, pass: string) {
    setLoading(true);
    try {
      const data = await api.register(name, email, pass);
      localStorage.setItem("civicquest_token", data.access_token);
      setToken(data.access_token);
      setUser(data.user);
      return data.user;
    } finally {
      setLoading(false);
    }
  }

  async function logout() {
    try {
      await api.logout();
    } catch {}
    if (typeof window !== "undefined") {
      localStorage.removeItem("civicquest_token");
    }
    setToken(null);
    setUser(null);
  }

  async function refreshUser() {
    try {
      const profile = await api.getMe();
      setUser(profile);
    } catch {
      setUser(null);
      setToken(null);
    }
  }

  return (
    <AuthContext.Provider value={{ user, token, loading, login, register, logout, refreshUser }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
}
