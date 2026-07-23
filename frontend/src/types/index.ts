export interface BoundingBox {
  x1: number;
  y1: number;
  x2: number;
  y2: number;
}

export interface Detection {
  class_name: string;
  confidence: number;
  bbox: BoundingBox;
  image_width: number;
  image_height: number;
}

export interface DetectionResponse {
  detections: Detection[];
  recommendations: string;
}
