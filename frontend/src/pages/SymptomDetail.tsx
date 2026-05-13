import { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import { api, type SymptomDetailResponse, type Finding } from "../api/client";
import "./SymptomDetail.css";

export function SymptomDetail() {
  const { slug } = useParams<{ slug: string }>();
  const [detail, setDetail] = useState<SymptomDetailResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!slug) return;
    api
      .getSupplementsBySymptom(slug)
      .then(setDetail)
      .catch((e: Error) => setError(e.message))
      .finally(() => setLoading(false));
  }, [slug]);

  if (loading) return <p className="state-msg">Loading…</p>;
  if (error) return <p className="state-msg error">Error: {error}</p>;
  if (!detail) return <p className="state-msg">Symptom not found.</p>;

  const symptomName = slug
    ? slug.replace(/-/g, " ").replace(/\b\w/g, (c) => c.toUpperCase())
    : "";

  return (
    <div className="symptom-detail-page">
      <Link to="/symptoms" className="back-link">← Back to symptoms</Link>

      <h1 className="page-title">{symptomName}</h1>

      {detail.symptomSummary && (
        <section className="symptom-overview-section">
          <p className="symptom-overview-text">{detail.symptomSummary}</p>
        </section>
      )}

      {detail.supplements.length === 0 ? (
        <p className="state-msg">No supplements found for this symptom.</p>
      ) : (
        detail.supplements.map((section) => (
          <section key={section.supplement.id} className="supplement-section">
            <h2 className="supplement-section-heading">
              <Link
                to={`/supplements/${section.supplement.id}`}
                className="supplement-section-link"
              >
                {section.supplement.name}
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

            {section.findings.length > 0 && (
              <ul className="findings-list">
                {section.findings.map((finding) => (
                  <FindingCard key={finding.id} finding={finding} />
                ))}
              </ul>
            )}
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
