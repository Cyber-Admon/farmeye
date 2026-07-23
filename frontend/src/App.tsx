import { useState } from "react";
import UploadZone from "./components/UploadZone";
import DetectionCanvas from "./components/DetectionCanvas";
import ResultsPanel from "./components/ResultsPanel";
import Loader from "./components/Loader";
import { detectDisease } from "./services/api";
import type { DetectionResponse } from "./types";
import { ScanLine } from "lucide-react";

const App = () => {
  const [imageFile, setImageFile] = useState<File | null>(null);
  const [result, setResult] = useState<DetectionResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleFileSelect = async (file: File) => {
    setImageFile(file);
    setResult(null);
    setError(null);
    setLoading(true);

    try {
      const data = await detectDisease(file);
      setResult(data);
    } catch (err) {
      setError("Something went wrong. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setImageFile(null);
    setResult(null);
    setError(null);
  };

  return (
    <div className="app">
      <header className="header">
        <div className="header__inner">
          <div className="header__brand">
            <ScanLine size={20} />
            <span className="header__logo">FarmEye</span>
          </div>
          <p className="header__tagline">Crop Disease Detection</p>
        </div>
      </header>

      <main className="main">
        <section className="hero">
          <h1 className="hero__title">Detect crop disease instantly</h1>
          <p className="hero__subtitle">
            Upload a photo of your tomato or pepper plant and get an instant diagnosis with treatment recommendations.
          </p>
        </section>

        <section className="workspace">
          {!imageFile && (
            <UploadZone onFileSelect={handleFileSelect} disabled={loading} />
          )}

          {loading && <Loader />}

          {imageFile && result && (
            <div className="results-layout">
              <DetectionCanvas imageFile={imageFile} detections={result.detections} />
              <ResultsPanel detections={result.detections} recommendations={result.recommendations} />
            </div>
          )}

          {error && (
            <div className="error-box">
              <p>{error}</p>
            </div>
          )}

          {imageFile && !loading && (
            <button className="btn-reset" onClick={handleReset}>
              Scan another plant
            </button>
          )}
        </section>
      </main>
    </div>
  );
};

export default App;