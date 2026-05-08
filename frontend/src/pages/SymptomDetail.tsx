import { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import { api, type SupplementDetail } from "../api/client";
import { SupplementCard } from "../components/SupplementCard";
import "./SymptomDetail.css";

export function SymptomDetail() {
  const { slug } = useParams<{ slug: string }>();
  const [supplements, setSupplements] = useState<SupplementDetail[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!slug) return;
    api
      .getSupplementsBySymptom(slug)
      .then(setSupplements)
      .catch((e: Error) => setError(e.message))
      .finally(() => setLoading(false));
  }, [slug]);

  if (loading) return <p className="state-msg">Loading…</p>;
  if (error) return <p className="state-msg error">Error: {error}</p>;

  const symptomName = supplements[0]?.findings
    .flatMap((f) => f.symptoms)
    .find((s) => s.slug === slug)?.name ?? slug;

  return (
    <div>
      <Link to="/symptoms" className="back-link">← Back to symptoms</Link>
      <h1 className="page-title">{symptomName}</h1>
      <p className="page-subtitle">Supplements with research findings for this symptom</p>
      {supplements.length === 0 ? (
        <p className="state-msg">No supplements found for this symptom.</p>
      ) : (
        <div className="supplement-grid">
          {supplements.map((s) => (
            <SupplementCard key={s.id} supplement={s} />
          ))}
        </div>
      )}
    </div>
  );
}
