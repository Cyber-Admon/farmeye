import os
from openai import AsyncOpenAI
from dotenv import load_dotenv
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

if OPENAI_API_KEY:
    client = AsyncOpenAI(api_key=OPENAI_API_KEY)
    print("[advisor] OpenAI ready")
else:
    client = None
    print("[advisor] No OPENAI_API_KEY found. Using fallback.")


async def get_recommendations(detections: list[dict]) -> str:
    if not client:
        return _fallback_recommendations(detections)

    disease_summary = ", ".join(
        f"{d['class_name'].replace('_', ' ')} ({round(d['confidence'] * 100)}% confidence)"
        for d in detections
    )

    prompt = f"""
You are an expert agricultural advisor helping smallholder farmers in Nigeria.

The following crop diseases have been detected on a plant:
{disease_summary}

Provide a concise, practical response covering:
1. A brief explanation of each detected disease
2. Immediate action the farmer should take
3. Preventive measures to avoid future outbreaks

Use simple, clear language. Keep your response under 250 words.
"""

    try:
        response = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=400,
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"[advisor] OpenAI call failed: {e}")
        return _fallback_recommendations(detections)


def _fallback_recommendations(detections: list[dict]) -> str:
    names = [d["class_name"].replace("_", " ") for d in detections]
    return (
        f"Detected: {', '.join(names)}. "
        "Please consult an agricultural extension officer for treatment advice. "
        "(Recommendation engine unavailable — set OPENAI_API_KEY to enable.)"
    )