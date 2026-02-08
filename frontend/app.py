import streamlit as st
import requests

st.set_page_config(page_title="Quantum Calibration Copilot", layout="centered")
st.title("🧪 Quantum Calibration Copilot")

files = st.file_uploader(
    "Upload resonator / calibration plots",
    accept_multiple_files=True,
    type=["png", "jpg", "jpeg"]
)

if st.button("Analyze"):

    if not files:
        st.warning("Please upload at least one image.")
        st.stop()

    with st.spinner("Analyzing calibration plots…"):
        response = requests.post(
            "http://localhost:8000/analyze/resonator",
            files=[("files", f) for f in files],
            timeout=60
        )

    # ---- Error handling ----
    if response.status_code != 200:
        st.error(f"Backend error ({response.status_code})")
        st.code(response.text)
        st.stop()

    try:
        result = response.json()
    except Exception:
        st.error("Failed to parse JSON response")
        st.code(response.text)
        st.stop()

    # ---- Results ----
    st.success("Analysis complete")

    # Decision
    decision = result["has_clear_resonance"].upper()
    confidence = int(result["confidence"] * 100)

    col1, col2 = st.columns(2)
    col1.metric("Decision", decision)
    col2.metric("Confidence", f"{confidence}%")

    # Explanation
    st.subheader("🔍 Interpretation")
    st.write(result["explanation"])

    # Detected issues
    if result.get("detected_issues"):
        st.subheader("⚠️ Detected Issues")
        for issue in result["detected_issues"]:
            st.warning(issue)

    # Suggested next steps
    if result.get("suggested_next_steps"):
        st.subheader("🛠 Suggested Next Steps")
        for step in result["suggested_next_steps"]:
            st.info(step)
