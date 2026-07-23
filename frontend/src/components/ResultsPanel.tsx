import ReactMarkdown from "react-markdown";
import { AlertTriangle, CheckCircle, Leaf } from "lucide-react";
import type { Detection } from "../types";

interface Props {
  detections: Detection[];
  recommendations: string;
}

const ResultsPanel = ({ detections, recommendations }: Props) => {
  const healthy = detections.length === 0;

  return (
    <div className="results-panel">
      <div className="results-panel__header">
        {healthy ? (
          <CheckCircle size={20} className="icon--success" />
        ) : (
          <AlertTriangle size={20} className="icon--danger" />
        )}
        <h2 className="results-panel__title">
          {healthy
            ? "No diseases detected"
            : `${detections.length} disease${detections.length > 1 ? "s" : ""} detected`}
        </h2>
      </div>

      {!healthy && (
        <div className="detections-list">
          {detections.map((det, i) => (
            <div key={i} className="detection-item">
              <Leaf size={14} className="icon--muted" />
              <div>
                <p className="detection-item__name">
                  {det.class_name.replace(/_/g, " ")}
                </p>
                <p className="detection-item__confidence">
                  {Math.round(det.confidence * 100)}% confidence
                </p>
              </div>
            </div>
          ))}
        </div>
      )}

      <div className="recommendations">
        <p className="recommendations__label">Recommendations</p>
        <div className="recommendations__text">
          <ReactMarkdown>{recommendations}</ReactMarkdown>
        </div>
      </div>
    </div>
  );
};

export default ResultsPanel;