import streamlit as st
from ai_generator import generate_pm_output
from pdf_generator import create_pdf

st.title("AI-Supported AMR Project Planning Prototype")

st.write(
    "This prototype generates customized project management outputs "
    "based on selected project parameters and deterministic PM rules."
)

integration_complexity = st.selectbox(
    "Select Integration Complexity:",
    ["Low", "Medium", "High"]
)

output_type = st.selectbox(
    "Select Required Output:",
    ["Timeline", "Work Breakdown Structure", "Project Charter"]
)

if "ai_output" not in st.session_state:
    st.session_state.ai_output = ""

if "pdf_file" not in st.session_state:
    st.session_state.pdf_file = None

if st.button("Generate Planning Output"):
    with st.spinner("Generating planning output..."):
        st.session_state.ai_output = generate_pm_output(
            integration_complexity,
            output_type
        )

        st.session_state.pdf_file = create_pdf(
            st.session_state.ai_output,
            integration_complexity,
            output_type
        )

if st.session_state.ai_output:
    st.subheader(f"Generated {output_type}")
    st.write(st.session_state.ai_output)

    st.download_button(
        label="Download Output as PDF",
        data=st.session_state.pdf_file,
        file_name=f"amr_{output_type.lower().replace(' ', '_')}_{integration_complexity.lower()}_complexity.pdf",
        mime="application/pdf"
    )