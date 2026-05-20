import streamlit as st
from pm_rules import get_pm_rules
from ai_generator import generate_ai_output, generate_timeline_json
from text_generator import create_text_file
from gantt_generator import parse_timeline_json, create_gantt_chart


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

# Session State Initialization
if "ai_output" not in st.session_state:
    st.session_state.ai_output = None

if "text_file" not in st.session_state:
    st.session_state.text_file = None

if "file_name" not in st.session_state:
    st.session_state.file_name = None

if "gantt_fig" not in st.session_state:
    st.session_state.gantt_fig = None

if "gantt_buffer" not in st.session_state:
    st.session_state.gantt_buffer = None


# Compact Input Layout
col1, col2 = st.columns([1, 2])

with col1:

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

    if output_type == "Timeline":
        generate_gantt = st.checkbox(
            "Generate Gantt Chart from AI Timeline"
        )
    else:
        generate_gantt = False

st.divider()

# Compact Generate Button
button_col, empty_col = st.columns([1, 4])

with button_col:
    generate_button = st.button("Generate Planning Output")

# Generate Outputs
if generate_button:

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

            st.session_state.gantt_fig = None
            st.session_state.gantt_buffer = None

            # Generate Gantt Chart
            if generate_gantt:

                timeline_json_response = generate_timeline_json(
                    integration_complexity=integration_complexity,
                    deployment_scale=deployment_scale,
                    pm_rules=pm_rules
                )

                timeline_data = parse_timeline_json(
                    timeline_json_response
                )

                gantt_fig, gantt_buffer = create_gantt_chart(
                    timeline_data
                )

                st.session_state.gantt_fig = gantt_fig
                st.session_state.gantt_buffer = gantt_buffer

    except Exception as e:
        st.error("Something went wrong while generating the output.")
        st.exception(e)

# Display AI Output
if st.session_state.ai_output:

    st.subheader("Generated Planning Output")

    st.write(st.session_state.ai_output)

    download_col, empty_col = st.columns([1, 4])

    with download_col:
        st.download_button(
            label="Download Text File",
            data=st.session_state.text_file,
            file_name=st.session_state.file_name,
            mime="text/plain"
        )

# Display Gantt Chart
if st.session_state.gantt_fig:

    st.subheader("Generated Gantt Chart")

    st.pyplot(st.session_state.gantt_fig)

    gantt_download_col, empty_col = st.columns([1, 4])

    with gantt_download_col:
        st.download_button(
            label="Download Gantt PNG",
            data=st.session_state.gantt_buffer,
            file_name="amr_gantt_chart.png",
            mime="image/png"
        )