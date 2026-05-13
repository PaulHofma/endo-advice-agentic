import { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import { api, type SupplementDetail as SupplementDetailType, type Finding } from "../api/client";
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

  const totalCitations = supplement.symptomSections
    .flatMap((s) => s.findings)
    .reduce((acc, f) => acc + f.citations.length, 0);
  const totalFindings = supplement.symptomSections.reduce((acc, s) => acc + s.findings.length, 0);

  return (
    <div className="detail-page">
      <Link to="/supplements" className="back-link">← Back to supplements</Link>

      <h1 className="detail-title">{supplement.name}</h1>

      {/* AI-generated supplement overview summary */}
      {supplement.supplementSummary ? (
        <section className="detail-section summary-section">
          <p className="supplement-summary">{supplement.supplementSummary}</p>
        </section>
      ) : (
        <section className="detail-section">
          <p className="detail-summary">{supplement.summary}</p>
        </section>
      )}

      {/* Evidence snapshot */}
      {totalFindings > 0 && (
        <section className="detail-section">
          <p className="evidence-snapshot">
            {totalFindings} finding{totalFindings !== 1 ? "s" : ""} backed by{" "}
            {totalCitations} PubMed citation{totalCitations !== 1 ? "s" : ""}
          </p>
        </section>
      )}

      {/* Symptom sections */}
      {supplement.symptomSections.length === 0 ? (
        <section className="detail-section">
          <p className="state-msg">No findings yet.</p>
        </section>
      ) : (
        supplement.symptomSections.map((section) => (
          <section key={section.symptom.id} className="detail-section symptom-section">
            <h2 className="symptom-section-heading">
              <Link to={`/symptoms/${section.symptom.slug}`} className="symptom-section-link">
                {section.symptom.name}
              </Link>
              {section.evidenceStrength && (
                <span className={`evidence-badge evidence-badge--${section.evidenceStrength}`}>
                  {section.evidenceStrength}
                </span>
              )}
            </h2>

            {section.pairSummary && (
              <p className="pair-summary">{section.pairSummary}</p>
            )}

            <ul className="findings-list">
              {section.findings.map((finding) => (
                <FindingCard key={finding.id} finding={finding} />
              ))}
            </ul>
          </section>
        ))
      )}
    </div>
  );
}

function FindingCard({ finding }: { finding: Finding }) {
  return (
    <li className="finding-item">
      <p className="finding-summary">{finding.plainLanguageSummary}</p>

      {(finding.studyType || finding.sampleSize != null) && (
        <p className="finding-credibility">
          {[
            finding.studyType?.toUpperCase().replace("_", " "),
            finding.sampleSize != null ? `n=${finding.sampleSize}` : null,
          ]
            .filter(Boolean)
            .join(" · ")}
        </p>
      )}

      {(finding.dosage || finding.duration) && (
        <p className="finding-clinical">
          {[
            finding.dosage ? `Dose: ${finding.dosage}` : null,
            finding.duration ? `Duration: ${finding.duration}` : null,
          ]
            .filter(Boolean)
            .join(" · ")}
        </p>
      )}

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

      {finding.safetyNotes && (
        <div className="finding-safety">
          <span className="finding-safety-label">Safety note:</span>{" "}
          {finding.safetyNotes}
        </div>
      )}
    </li>
  );
}
