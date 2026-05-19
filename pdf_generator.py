from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4


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