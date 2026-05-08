import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { api, type SymptomSummary } from "../api/client";
import "./SymptomList.css";

export function SymptomList() {
  const [symptoms, setSymptoms] = useState<SymptomSummary[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    api
      .getSymptoms()
      .then(setSymptoms)
      .catch((e: Error) => setError(e.message))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <p className="state-msg">Loading symptoms…</p>;
  if (error) return <p className="state-msg error">Error: {error}</p>;

  return (
    <div>
      <h1 className="page-title">Browse by Symptom</h1>
      <p className="page-subtitle">
        Select a symptom to see which supplements have research findings for it.
      </p>
      {symptoms.length === 0 ? (
        <p className="state-msg">No symptoms with findings yet.</p>
      ) : (
        <div className="symptom-tags-list">
          {symptoms.map((s) => (
            <Link key={s.id} to={`/symptoms/${s.slug}`} className="symptom-card">
              {s.name}
            </Link>
          ))}
        </div>
      )}
    </div>
  );
}
