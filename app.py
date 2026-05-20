import streamlit as st
from pm_rules import get_pm_rules
from ai_generator import generate_ai_output
from text_generator import create_text_file


st.set_page_config(
    page_title="AMR Planning Framework",
    layout="wide"
)

st.title(
    "Prototype: AI-Supported Adaptive Planning Framework for AMR Deployment in Warehouse Logistics"
)

st.write(
    "This prototype generates adaptive project management planning outputs "
    "for AMR deployment projects in warehouse logistics based on selected "
    "project conditions."
)

st.divider()

if "ai_output" not in st.session_state:
    st.session_state.ai_output = None

if "text_file" not in st.session_state:
    st.session_state.text_file = None

if "file_name" not in st.session_state:
    st.session_state.file_name = None


integration_complexity = st.selectbox(
    "Select Integration Complexity",
    ["Low", "Medium", "High"]
)

deployment_scale = st.selectbox(
    "Select Deployment Scale",
    [
        "Pilot",
        "Single-Zone Rollout",
        "Multi-Zone Rollout",
        "Full Warehouse Rollout"
    ]
)

output_type = st.selectbox(
    "Select Output Type",
    [
        "Timeline",
        "WBS",
        "Project Charter"
    ]
)

st.divider()

if st.button("Generate Planning Output"):

    try:
        with st.spinner("Generating planning output..."):

            pm_rules = get_pm_rules(
                integration_complexity=integration_complexity,
                deployment_scale=deployment_scale
            )

            ai_output = generate_ai_output(
                integration_complexity=integration_complexity,
                deployment_scale=deployment_scale,
                output_type=output_type,
                pm_rules=pm_rules
            )

            text_file = create_text_file(
                ai_output,
                integration_complexity,
                deployment_scale,
                output_type
            )

            file_name = (
                f"amr_{output_type.lower().replace(' ', '_')}_"
                f"{integration_complexity.lower()}_"
                f"{deployment_scale.lower().replace(' ', '_')}.txt"
            )

            st.session_state.ai_output = ai_output
            st.session_state.text_file = text_file
            st.session_state.file_name = file_name

    except Exception as e:
        st.error("Something went wrong while generating the output.")
        st.exception(e)


if st.session_state.ai_output:

    st.subheader("Generated Planning Output")
    st.write(st.session_state.ai_output)

    st.download_button(
        label="Download Editable Text File",
        data=st.session_state.text_file,
        file_name=st.session_state.file_name,
        mime="text/plain"
    )