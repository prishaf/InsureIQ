import streamlit as st

from src.extractor import extract_text_from_pdf, basic_field_extraction
from src.nlp_pipeline import extract_entities
from src.similarity import compute_similarity
from src.llm_engine import generate_insights

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="Insurance Analyzer", layout="wide")

# ---------- CLEAN PROFESSIONAL THEME ----------
st.markdown("""
<style>

/* ================= GLOBAL ================= */
.stApp {
    background-color: #f5f7fb;
    color: #1f2937;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
}

/* Remove Streamlit default header/footer */
header {visibility: hidden;}
footer {visibility: hidden;}

/* Content width */
.block-container {
    max-width: 1100px;
    padding-top: 2rem;
}

/* ================= SIDEBAR ================= */
section[data-testid="stSidebar"] {
    background-color: #0b3c5d;
}
section[data-testid="stSidebar"] * {
    color: white !important;
}

/* ================= HEADINGS ================= */
h1, h2, h3 {
    color: #1f2937;
    font-weight: 600;
}

/* ================= FILE UPLOADER ================= */
div[data-testid="stFileUploader"] {
    background: white !important;
    border: 1px solid #e5e7eb !important;
    border-radius: 12px !important;
    padding: 20px !important;
}

/* Dropzone */
div[data-testid="stFileUploaderDropzone"] {
    background: #ffffff !important;
    border: 2px dashed #cbd5e1 !important;
    border-radius: 10px !important;
    padding: 20px;
}

/* Upload button */
div[data-testid="stFileUploader"] button[kind="secondary"] {
    background-color: #0b3c5d !important;
    color: white !important;
    border-radius: 8px !important;
    border: none !important;
    font-weight: 600 !important;
}

/* Upload helper text */
div[data-testid="stFileUploader"] small {
    color: #6b7280 !important;
}

/* Uploaded file name */
div[data-testid="stFileUploader"] p {
    color: #111827 !important;
}

/* ================= BUTTONS ================= */
.stButton > button {
    background-color: #0b3c5d;
    color: white;
    border-radius: 8px;
    padding: 10px 20px;
    border: none;
    font-weight: 600;
}
.stButton > button:hover {
    background-color: #145374;
}

/* Download button */
.stDownloadButton > button {
    background-color: #0b3c5d !important;
    color: white !important;
    border-radius: 8px;
    border: none;
    font-weight: 600;
}
.stDownloadButton > button:hover {
    background-color: #145374 !important;
}

/* ================= METRICS ================= */
[data-testid="stMetric"] {
    background: white;
    padding: 15px;
    border-radius: 10px;
    border: 1px solid #e5e7eb;
}

/* Metric label */
[data-testid="stMetric"] label {
    color: #6b7280 !important;
    font-weight: 500;
}

/* Metric value */
[data-testid="stMetric"] div {
    color: #111827 !important;
    font-size: 28px;
    font-weight: 600;
}

/* ================= TEXT AREAS ================= */
textarea {
    background-color: white !important;
    color: #111827 !important;
    border-radius: 8px !important;
    
}
            /* FORCE WHITE TEXT IN UPLOAD BUTTON */
div[data-testid="stFileUploader"] button[kind="secondary"] * {
    color: white !important;
    fill: white !important;
}

/* Fix icon inside button */
div[data-testid="stFileUploader"] button svg {
    fill: white !important;
}

/* ================= JSON / CODE ================= */
code, pre {
    color: #111827 !important;
    background-color: #ffffff !important;
}

/* ================= PROGRESS BAR ================= */
.stProgress > div > div {
    background-color: #2563eb;
}

/* ================= ALERTS ================= */
.stAlert {
    border-radius: 10px;
}

/* ================= SPACING ================= */
hr {
    border: none;
    border-top: 1px solid #e5e7eb;
    margin: 20px 0;
}

</style>
""", unsafe_allow_html=True)

# ---------- SIDEBAR ----------
st.sidebar.title("InsureIQ")
page = st.sidebar.radio("Navigation", ["Overview", "Analysis", "Insights"])

st.sidebar.markdown("---")
st.sidebar.caption("System Status")
st.sidebar.write("Production")
st.sidebar.write("Model: Mistral (Local)")

# ---------- HEADER ----------
st.title("Insurance Document Analyzer")

st.markdown(
    "<p style='color:#6b7280;font-size:15px;'>Automated extraction and risk evaluation of insurance documents</p>",
    unsafe_allow_html=True
)

# ---------- FILE UPLOAD ----------
uploaded_file = st.file_uploader("Upload Insurance Document (PDF)", type=["pdf"])

if not uploaded_file:
    st.info("Upload a document to begin analysis")
    st.stop()

# ---------- PROCESS ----------
text = extract_text_from_pdf(uploaded_file)

entities = extract_entities(text)
fields = basic_field_extraction(text)
similarity_score = compute_similarity(text, "standard insurance policy")

# ---------- IMPROVED RISK SCORE ----------
def calculate_risk_score(text):
    text = text.lower()

    high = ["breach", "fraud", "lawsuit", "penalty", "liability"]
    medium = ["failure", "error", "delay", "downtime"]
    exclusions = ["not covered", "excluded", "limitation"]

    score = 0
    score += sum(text.count(w) for w in high) * 8
    score += sum(text.count(w) for w in medium) * 4
    score += sum(text.count(w) for w in exclusions) * 10

    return min(score, 100)

# ---------- OVERVIEW ----------
if page == "Overview":

    col1, col2, col3 = st.columns(3)

    col1.metric("Entities", len(entities))
    col2.metric("Similarity", round(similarity_score, 2))
    col3.metric("Length", len(text))

    st.markdown("### Extracted Text")
    st.text_area("", text[:3000], height=250)

# ---------- ANALYSIS ----------
elif page == "Analysis":

    st.markdown("### Extracted Fields")
    st.json(fields)

    st.markdown("### Named Entities")
    st.dataframe(entities, use_container_width=True)

# ---------- INSIGHTS ----------
# ---------- INSIGHTS ----------
elif page == "Insights":

    st.markdown("---")
    st.markdown("## Risk Intelligence Dashboard")

    # ✅ SINGLE BUTTON WITH KEY
    if st.button("Run Risk Analysis", key="run_analysis_btn"):

        with st.spinner("Analyzing document..."):
            insights = generate_insights(text)

        # ✅ DEFINE SCORE
        risk_score = calculate_risk_score(text)

        st.divider()

        col1, col2 = st.columns([1, 2])

        # ---------- LEFT SIDE ----------
        with col1:
            st.metric("Risk Score", f"{risk_score}/100")
            st.progress(risk_score / 100)

            # GRAPH
            import matplotlib.pyplot as plt
            fig, ax = plt.subplots()
            ax.bar(["Risk"], [risk_score])
            ax.set_ylim(0, 100)
            ax.set_title("Risk Level")
            st.pyplot(fig)

            # STATUS
            if risk_score > 70:
                st.error("High Risk Document")
            elif risk_score > 40:
                st.warning("Moderate Risk Document")
            else:
                st.success("Low Risk Document")

        # ---------- RIGHT SIDE ----------
        with col2:
            st.markdown("### AI Risk Analysis")
            st.markdown(insights)

        # ---------- DOWNLOAD BUTTON ----------
        st.download_button(
            label="Download Report",
            data=insights,
            file_name="risk_report.txt",
            mime="text/plain",
            key="download_report_btn"
        )