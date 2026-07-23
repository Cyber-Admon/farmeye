import axios from "axios";
import type { DetectionResponse } from "../types";

const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

export const detectDisease = async (file: File): Promise<DetectionResponse> => {
  const formData = new FormData();
  formData.append("file", file);

  const response = await axios.post<DetectionResponse>(
    `${API_BASE_URL}/api/detect`,
    formData,
    {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    }
  );

  return response.data;
};