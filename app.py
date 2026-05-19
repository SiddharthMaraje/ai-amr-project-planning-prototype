import streamlit as st
import ollama
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from io import BytesIO

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


def get_pm_rules(integration_complexity):
    if integration_complexity == "Low":
        return {
            "planning_depth": "Lightweight planning",
            "mandatory_workstreams": [
                "Basic IT Readiness",
                "Operational Preparation",
                "Basic User Training"
            ],
            "mandatory_risks": [
                "Minor configuration delays",
                "Basic user adoption issues",
                "Limited process disruption"
            ],
            "mandatory_milestones": [
                "Basic requirements confirmed",
                "System access validated",
                "Go-live readiness confirmed"
            ],
            "governance_level": "Simple weekly project check-in"
        }

    elif integration_complexity == "Medium":
        return {
            "planning_depth": "Moderate planning and coordination",
            "mandatory_workstreams": [
                "WMS/ERP Interface Planning",
                "System Integration Testing",
                "Operational Readiness",
                "Stakeholder Training",
                "Pilot Validation"
            ],
            "mandatory_risks": [
                "Interface mapping delays",
                "Incomplete data exchange requirements",
                "Operational disruption during pilot",
                "User resistance during transition"
            ],
            "mandatory_milestones": [
                "Interface requirements confirmed",
                "Integration test completed",
                "Pilot completed",
                "Operational readiness approved"
            ],
            "governance_level": "Weekly project meeting with integration checkpoint"
        }

    elif integration_complexity == "High":
        return {
            "planning_depth": "Detailed planning, governance, testing, and risk control",
            "mandatory_workstreams": [
                "Detailed WMS/ERP Integration Design",
                "API and Data Exchange Validation",
                "End-to-End System Testing",
                "Cybersecurity and Access Control Review",
                "Operational Change Management",
                "Safety and Compliance Validation",
                "Go/No-Go Governance"
            ],
            "mandatory_risks": [
                "WMS/ERP integration failure",
                "Incorrect data exchange between systems",
                "Delayed end-to-end testing",
                "Operational downtime during rollout",
                "Safety validation failure",
                "Stakeholder alignment issues"
            ],
            "mandatory_milestones": [
                "Integration design approved",
                "API/data exchange validated",
                "End-to-end test completed",
                "Safety validation approved",
                "Go/no-go decision completed"
            ],
            "governance_level": "Formal steering committee with phase-gate approvals"
        }


def generate_pm_output(integration_complexity, output_type):
    rules = get_pm_rules(integration_complexity)

    prompt = f"""
You are a project management assistant.

Create a customized {output_type} for an AMR deployment project in warehouse logistics.

Project parameter:
Integration Complexity = {integration_complexity}

The following deterministic PM rules MUST be followed.

Planning depth:
{rules["planning_depth"]}

Mandatory workstreams:
{rules["mandatory_workstreams"]}

Mandatory risks:
{rules["mandatory_risks"]}

Mandatory milestones:
{rules["mandatory_milestones"]}

Governance level:
{rules["governance_level"]}

Output requirements:
- Generate only the selected output type: {output_type}
- Keep the output practical and project-management-focused.
- Use clear headings.
- Include the mandatory elements from the deterministic rules.
- Do not ignore the mandatory workstreams, risks, milestones, or governance level.
- Do not write generic theory.
- Make the output suitable for a capstone prototype.
"""

    response = ollama.chat(
        model="llama3",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        options={
            "temperature": 0.2,
            "num_predict": 700
        }
    )

    return response["message"]["content"]


def create_pdf(text, integration_complexity, output_type):
    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph("AI-Supported AMR Project Planning Output", styles["Title"]))
    story.append(Spacer(1, 12))

    story.append(Paragraph(f"Selected Output: {output_type}", styles["Heading2"]))
    story.append(Paragraph(f"Integration Complexity: {integration_complexity}", styles["Heading2"]))
    story.append(Spacer(1, 12))

    for line in text.split("\n"):
        if line.strip():
            story.append(Paragraph(line, styles["BodyText"]))
            story.append(Spacer(1, 6))

    doc.build(story)

    buffer.seek(0)
    return buffer


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
        file_name=f"amr_{output_type.lower().replace(' ', '_')}.pdf",
        mime="application/pdf"
    )