import { useEffect, useState } from "react";
import { api, type SupplementSummary } from "../api/client";
import { SupplementCard } from "../components/SupplementCard";
import "./SupplementList.css";

export function SupplementList() {
  const [supplements, setSupplements] = useState<SupplementSummary[]>([]);
  const [query, setQuery] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    api
      .getSupplements()
      .then(setSupplements)
      .catch((e: Error) => setError(e.message))
      .finally(() => setLoading(false));
  }, []);

  const filtered = supplements.filter((s) =>
    s.name.toLowerCase().includes(query.toLowerCase())
  );

  if (loading) return <p className="state-msg">Loading supplements…</p>;
  if (error) return <p className="state-msg error">Error: {error}</p>;

  return (
    <div>
      <h1 className="page-title">Supplements</h1>
      <input
        type="search"
        className="search-input"
        placeholder="Search by name…"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        aria-label="Search supplements by name"
      />
      {filtered.length === 0 ? (
        <p className="state-msg">
          {supplements.length === 0
            ? "No supplements have been loaded yet."
            : "No supplements match your search."}
        </p>
      ) : (
        <div className="supplement-grid">
          {filtered.map((s) => (
            <SupplementCard key={s.id} supplement={s} />
          ))}
        </div>
      )}
    </div>
  );
}
