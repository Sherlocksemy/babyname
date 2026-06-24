import type { ProfileForm } from "./validation";

export const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL || "http://127.0.0.1:8000";

type ApiError = {
  error?: {
    code: string;
    message: string;
    field?: string | null;
    details?: Record<string, unknown>;
  };
};

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE}${path}`, {
    ...init,
    headers: {
      "Content-Type": "application/json",
      ...(init?.headers || {})
    },
    cache: "no-store"
  });
  const text = await response.text();
  const data = text ? JSON.parse(text) : {};
  if (!response.ok) {
    const error = data as ApiError;
    throw new Error(error.error?.message || `HTTP ${response.status}`);
  }
  return data as T;
}

export function generateNames(profile: ProfileForm) {
  return request<{ request_id: string; status: string; created_at: string }>("/api/v1/names/generate", {
    method: "POST",
    body: JSON.stringify(profile)
  });
}

export function getResult(requestId: string) {
  return request<any>(`/api/v1/names/${requestId}`);
}

export function getCandidateDetail(requestId: string, candidateId: string) {
  return request<any>(`/api/v1/names/${requestId}/candidates/${candidateId}`);
}

export function regenerate(requestId: string) {
  return request<{ request_id: string; status: string; created_at: string }>(`/api/v1/names/${requestId}/regenerate`, {
    method: "POST",
    body: JSON.stringify({})
  });
}

export function createFavorite(requestId: string, candidateId: string) {
  return request<any>("/api/v1/favorites", {
    method: "POST",
    body: JSON.stringify({ request_id: requestId, candidate_id: candidateId })
  });
}

export function listFavorites(requestId: string) {
  return request<any>(`/api/v1/favorites?request_id=${encodeURIComponent(requestId)}`);
}
