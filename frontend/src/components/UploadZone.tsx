import { useRef, useState } from "react";
import { Upload, ImagePlus } from "lucide-react";

interface Props {
  onFileSelect: (file: File) => void;
  disabled: boolean;
}

const UploadZone = ({ onFileSelect, disabled }: Props) => {
  const inputRef = useRef<HTMLInputElement>(null);
  const [dragging, setDragging] = useState(false);

  const handleFile = (file: File) => {
    if (file && (file.type === "image/jpeg" || file.type === "image/png")) {
      onFileSelect(file);
    }
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setDragging(false);
    const file = e.dataTransfer.files[0];
    handleFile(file);
  };

  return (
    <div
      className={`upload-zone ${dragging ? "upload-zone--dragging" : ""} ${disabled ? "upload-zone--disabled" : ""}`}
      onClick={() => !disabled && inputRef.current?.click()}
      onDragOver={(e) => { e.preventDefault(); setDragging(true); }}
      onDragLeave={() => setDragging(false)}
      onDrop={handleDrop}
    >
      <input
        ref={inputRef}
        type="file"
        accept="image/jpeg,image/png"
        style={{ display: "none" }}
        onChange={(e) => e.target.files && handleFile(e.target.files[0])}
      />
      <div className="upload-zone__icon">
        {dragging ? <ImagePlus size={32} /> : <Upload size={32} />}
      </div>
      <p className="upload-zone__title">Drop your plant image here</p>
      <p className="upload-zone__subtitle">JPEG or PNG — tomato and pepper plants only</p>
    </div>
  );
};

export default UploadZone;