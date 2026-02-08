from fastapi import FastAPI, UploadFile, File, HTTPException
import base64

from schemas.calibration import ResonatorAnalysis
from prompts.resonator import RESONATOR_PROMPT
from services.vlm_client import analyze_resonator

app = FastAPI()

@app.post("/analyze/resonator", response_model=ResonatorAnalysis)
async def analyze_resonator_endpoint(
    files: list[UploadFile] = File(...)
):
    try:
        images_b64: list[str] = []

        for file in files:
            contents = await file.read()   # ✅ bytes
            encoded = base64.b64encode(contents).decode("utf-8")
            images_b64.append(encoded)

        decision = analyze_resonator(images_b64, RESONATOR_PROMPT)

        analysis = analyze_resonator(images_b64, RESONATOR_PROMPT)

        return ResonatorAnalysis(
            has_clear_resonance=analysis["has_clear_resonance"],
            confidence=0.75,
            explanation=analysis["explanation"],
            detected_issues=analysis["detected_issues"],
            suggested_next_steps=analysis["suggested_next_steps"],
        )



    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
