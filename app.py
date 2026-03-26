import streamlit as st
from src.pipeline import RegulatoryPipeline
from src.memo import generate_memo

st.set_page_config(page_title="PrecisionReg Navigator", layout="wide")
st.title("PrecisionReg Navigator")
st.caption("FDA regulatory intelligence for oncology IVDs, tumor profiling, and companion diagnostics")

pipeline = RegulatoryPipeline()

with st.sidebar:
    st.header("Product Intake")
    disease = st.text_input("Disease", "NSCLC")
    intended_use = st.text_area(
        "Intended Use",
        "NGS-based tumor profiling assay intended to identify actionable genomic alterations in patients with advanced non-small cell lung cancer to support therapy selection."
    )
    biomarkers = st.text_input("Biomarkers (comma-separated)", "EGFR, ALK, ROS1, KRAS")
    therapy_linked = st.checkbox("Therapy linked?", value=True)
    specimen_type = st.selectbox(
        "Specimen Type",
        ["FFPE tissue", "Plasma", "Whole blood", "Bone marrow", "Saliva", "Other"]
    )
    platform = st.selectbox(
        "Platform",
        ["NGS targeted panel", "Liquid biopsy", "PCR", "FISH", "IHC"]
    )
    software_involved = st.checkbox("Software involved?", value=True)

    run_btn = st.button("Run Assessment")

def build_markdown_memo(memo):
    lines = []
    lines.append(f"# {memo.title}")
    lines.append("")
    lines.append("## Executive Summary")
    lines.append(memo.executive_summary)
    lines.append("")
    lines.append("## Product Assessment")
    lines.append(memo.product_assessment)
    lines.append("")
    lines.append("## Evidence Gaps")
    for item in memo.evidence_gaps:
        lines.append(f"- {item}")
    lines.append("")
    lines.append("## Recommended Actions")
    for item in memo.recommended_actions:
        lines.append(f"- {item}")
    lines.append("")
    lines.append("## Citations and Precedents")
    for item in memo.citations:
        lines.append(f"- {item}")
    lines.append("")
    return "\n".join(lines)

if run_btn:
    product_input = {
        "disease": disease,
        "intended_use": intended_use,
        "biomarkers": [b.strip() for b in biomarkers.split(",") if b.strip()],
        "therapy_linked": therapy_linked,
        "specimen_type": specimen_type,
        "platform": platform,
        "software_involved": software_involved,
    }

    with st.spinner("Running assessment..."):
        result = pipeline.run(product_input)
        memo = generate_memo(
            product_input,
            result["classification"],
            result["assessment"],
            result["guidance_hits"],
            result["precedent_hits"]
        )
        memo_md = build_markdown_memo(memo)

    tab1, tab2, tab3, tab4 = st.tabs(["Snapshot", "Guidance", "Precedents", "Memo"])

    with tab1:
        c1, c2 = st.columns(2)

        with c1:
            st.subheader("Classification")
            st.write(f"**Product Type:** {result['classification'].product_type}")
            st.write(f"**Likely CDx:** {result['classification'].likely_cdx}")
            st.write(f"**Likely Tumor Profiling:** {result['classification'].likely_tumor_profiling}")
            st.write(f"**Likely Investigational Use:** {result['classification'].likely_investigational_use}")

        with c2:
            st.subheader("Assessment Snapshot")
            st.write(f"**Probable Route:** {result['assessment'].probable_route}")
            st.write("**Top Risks:**")
            for risk in result["assessment"].key_risks[:5]:
                st.write(f"- {risk}")

    with tab2:
        st.subheader("Top Guidance Hits")
        for hit in result["guidance_hits"]:
            with st.expander(f"{hit['title']} - {hit['section']}"):
                st.write(hit["text"][:1500])
                st.caption(f"Citation: {hit['citation']}")

    with tab3:
        st.subheader("Top FDA Precedents")
        if result["precedent_hits"]:
            for p in result["precedent_hits"]:
                with st.container():
                    st.markdown(f"**{p.trade_name}**")
                    st.write(f"Submission: {p.submission_number}")
                    st.write(f"Sponsor: {p.sponsor}")
                    st.write(f"Disease/Use: {p.disease_use}")
                    st.write(f"Biomarker: {p.biomarker}")
                    st.write(f"Platform: {p.platform}")
                    st.write(f"Specimen Type: {p.specimen_type}")
                    st.write(f"Route: {p.route}")
                    st.write(f"CDx: {p.cdx_flag}")
                    st.divider()
        else:
            st.info("No precedent matches found.")

    with tab4:
        st.subheader(memo.title)
        st.write("### Executive Summary")
        st.write(memo.executive_summary)

        st.write("### Product Assessment")
        st.write(memo.product_assessment)

        st.write("### Evidence Gaps")
        for item in memo.evidence_gaps:
            st.write(f"- {item}")

        st.write("### Recommended Actions")
        for item in memo.recommended_actions:
            st.write(f"- {item}")

        st.write("### Citations and Precedents")
        for c in memo.citations:
            st.write(f"- {c}")

        st.download_button(
            label="Download Memo as Markdown",
            data=memo_md,
            file_name="precisionreg_memo.md",
            mime="text/markdown"
        )
