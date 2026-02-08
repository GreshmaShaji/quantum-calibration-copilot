from openai import OpenAI

client = OpenAI()

def analyze_resonator(images_b64: list[str], prompt: str) -> dict:
    response = client.responses.create(
        model="gpt-4.1",
        input=[
            {
                "role": "user",
                "content": (
                    [{"type": "input_text", "text": prompt}]
                    + [
                        {
                            "type": "input_image",
                            "image_url": f"data:image/png;base64,{img}"
                        }
                        for img in images_b64
                    ]
                )
            }
        ],
    )

    text = response.output_text.strip()

    # VERY simple heuristics for now
    decision = "uncertain"
    if "clear resonance" in text.lower():
        decision = "yes"
    elif "no clear resonance" in text.lower() or "failed" in text.lower():
        decision = "no"

    return {
        "has_clear_resonance": decision,
        "explanation": text,
        "detected_issues": [],
        "suggested_next_steps": []
    }

