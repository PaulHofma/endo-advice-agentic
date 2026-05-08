import { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import { api, type SupplementDetail as SupplementDetailType } from "../api/client";
import "./SupplementDetail.css";

export function SupplementDetail() {
  const { id } = useParams<{ id: string }>();
  const [supplement, setSupplement] = useState<SupplementDetailType | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!id) return;
    api
      .getSupplementById(Number(id))
      .then(setSupplement)
      .catch((e: Error) => setError(e.message))
      .finally(() => setLoading(false));
  }, [id]);

  if (loading) return <p className="state-msg">Loading…</p>;
  if (error) return <p className="state-msg error">Error: {error}</p>;
  if (!supplement) return <p className="state-msg">Supplement not found.</p>;

  return (
    <div className="detail-page">
      <Link to="/supplements" className="back-link">← Back to supplements</Link>

      <h1 className="detail-title">{supplement.name}</h1>

      {/* Plain-language summary */}
      <section className="detail-section">
        <h2 className="section-heading">Summary</h2>
        <p className="detail-summary">{supplement.summary}</p>
      </section>

      {/* Evidence snapshot */}
      {supplement.findings.length > 0 && (
        <section className="detail-section">
          <h2 className="section-heading">Evidence Snapshot</h2>
          <p className="evidence-snapshot">
            {supplement.findings.length} finding{supplement.findings.length !== 1 ? "s" : ""} backed by{" "}
            {supplement.findings.reduce((acc, f) => acc + f.citations.length, 0)} PubMed citation
            {supplement.findings.reduce((acc, f) => acc + f.citations.length, 0) !== 1 ? "s" : ""}
          </p>
        </section>
      )}

      {/* Findings list */}
      <section className="detail-section">
        <h2 className="section-heading">Findings</h2>
        {supplement.findings.length === 0 ? (
          <p className="state-msg">No findings yet.</p>
        ) : (
          <ul className="findings-list">
            {supplement.findings.map((finding) => (
              <li key={finding.id} className="finding-item">
                <p className="finding-summary">{finding.plainLanguageSummary}</p>
                <p className="finding-evidence">{finding.evidenceSnapshot}</p>
                {finding.citations.map((citation) => (
                  <blockquote key={citation.id} className="citation-block">
                    <p className="citation-excerpt">"{citation.abstractExcerpt}"</p>
                    <footer className="citation-footer">
                      <span className="citation-meta">
                        {citation.authors} ({citation.year}). {citation.title}.
                      </span>{" "}
                      <a
                        href={citation.pubmedUrl}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="citation-link"
                      >
                        View on PubMed ↗
                      </a>
                    </footer>
                  </blockquote>
                ))}
                {finding.symptoms.length > 0 && (
                  <div className="finding-symptoms">
                    {finding.symptoms.map((s) => (
                      <Link
                        key={s.id}
                        to={`/symptoms/${s.slug}`}
                        className="symptom-tag"
                      >
                        {s.name}
                      </Link>
                    ))}
                  </div>
                )}
              </li>
            ))}
          </ul>
        )}
      </section>
    </div>
  );
}
