import { Link } from "react-router-dom";
import type { SupplementSummary } from "../api/client";
import "./SupplementCard.css";

interface Props {
  supplement: SupplementSummary;
}

export function SupplementCard({ supplement }: Props) {
  return (
    <Link to={`/supplements/${supplement.id}`} className="supplement-card">
      <h3 className="supplement-card-name">{supplement.name}</h3>
      <p className="supplement-card-summary">{supplement.summary}</p>
    </Link>
  );
}
