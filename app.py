import streamlit as st
import ollama
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from io import BytesIO

st.title("AI-Supported AMR Project Planning Prototype")

st.write(
    "This prototype generates customized project management outputs "
    "based on selected project parameters."
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


def generate_pm_output(integration_complexity, output_type):
    prompt = f"""
You are a project management assistant.

Create a customized {output_type} for an AMR deployment project in warehouse logistics.

Project parameter:
Integration Complexity = {integration_complexity}

Rules:
- If integration complexity is Low, keep the output simple and lightweight.
- If integration complexity is Medium, include moderate planning, coordination, and testing.
- If integration complexity is High, include detailed integration planning, testing, validation, governance, and risk control.

Output requirements:
- Keep it practical and project-management-focused.
- Use clear headings.
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
            "temperature": 0.3,
            "num_predict": 500
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