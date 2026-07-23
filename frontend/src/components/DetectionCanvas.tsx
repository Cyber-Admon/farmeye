import { useEffect, useRef } from "react";
import type { Detection } from "../types";

interface Props {
  imageFile: File;
  detections: Detection[];
}

const DetectionCanvas = ({ imageFile, detections }: Props) => {
  const canvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    const img = new Image();
    img.src = URL.createObjectURL(imageFile);

    img.onload = () => {
      canvas.width = img.width;
      canvas.height = img.height;

      ctx.drawImage(img, 0, 0);

      detections.forEach((det) => {
        const { x1, y1, x2, y2 } = det.bbox;

        ctx.strokeStyle = "#C0392B";
        ctx.lineWidth = 2;
        ctx.strokeRect(x1, y1, x2 - x1, y2 - y1);

        const label = `${det.class_name.replace(/_/g, " ")} ${Math.round(det.confidence * 100)}%`;
        ctx.font = "13px Inter, sans-serif";

        const textWidth = ctx.measureText(label).width;
        ctx.fillStyle = "#C0392B";
        ctx.fillRect(x1, y1 - 22, textWidth + 12, 22);

        ctx.fillStyle = "#FFFFFF";
        ctx.fillText(label, x1 + 6, y1 - 6);
      });
    };
  }, [imageFile, detections]);

  return (
    <div className="canvas-wrapper">
      <canvas ref={canvasRef} className="detection-canvas" />
    </div>
  );
};

export default DetectionCanvas;