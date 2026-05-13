const API_BASE = import.meta.env.VITE_API_BASE ?? "http://localhost:8080";

async function apiFetch<T>(path: string): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`);
  if (!res.ok) {
    throw new Error(`API error ${res.status}: ${res.statusText}`);
  }
  return res.json() as Promise<T>;
}

export interface SupplementSummary {
  id: number;
  name: string;
  summary: string;
}

export interface Citation {
  id: number;
  pmid: string;
  title: string;
  authors: string;
  year: number;
  abstractExcerpt: string;
  pubmedUrl: string;
}

export interface SymptomSummary {
  id: number;
  name: string;
  slug: string;
}

export interface Finding {
  id: number;
  plainLanguageSummary: string;
  evidenceSnapshot: string;
  citations: Citation[];
  symptoms: SymptomSummary[];
  dosage: string | null;
  duration: string | null;
  studyType: string | null;
  sampleSize: number | null;
  placeboControlled: boolean | null;
  safetyNotes: string | null;
}

export interface SupplementSymptomSection {
  symptom: SymptomSummary;
  pairSummary: string | null;
  evidenceStrength: string | null;
  findings: Finding[];
}

export interface SupplementDetail extends SupplementSummary {
  supplementSummary: string | null;
  symptomSections: SupplementSymptomSection[];
}

export interface SymptomSupplementSection {
  supplement: SupplementSummary;
  pairSummary: string | null;
  evidenceStrength: string | null;
  findings: Finding[];
}

export interface SymptomDetailResponse {
  symptomSummary: string | null;
  supplements: SymptomSupplementSection[];
}

export const api = {
  getSupplements: () => apiFetch<SupplementSummary[]>("/api/supplements"),
  getSupplementById: (id: number) => apiFetch<SupplementDetail>(`/api/supplements/${id}`),
  getSymptoms: () => apiFetch<SymptomSummary[]>("/api/symptoms"),
  getSupplementsBySymptom: (slug: string) =>
    apiFetch<SymptomDetailResponse>(`/api/symptoms/${slug}/supplements`),
};
