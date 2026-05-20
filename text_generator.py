from io import BytesIO


def clean_ai_text(text):
    cleaned_text = text.replace("**", "")
    cleaned_text = cleaned_text.replace("*", "-")
    cleaned_text = cleaned_text.replace("#", "")
    return cleaned_text.strip()


def create_text_file(
    prompt,
    text,
    integration_complexity,
    deployment_scale,
    output_type
):

    buffer = BytesIO()

    clean_prompt = clean_ai_text(prompt)
    clean_text = clean_ai_text(text)

    content = f"""
Prototype: AI-Supported Adaptive Planning Framework for AMR Deployment in Warehouse Logistics

Selected Output: {output_type}
Integration Complexity: {integration_complexity}
Deployment Scale: {deployment_scale}

============================================================
GENERATED PROMPT
============================================================

{clean_prompt}

============================================================
AI-GENERATED OUTPUT
============================================================

{clean_text}
"""

    buffer.write(content.encode("utf-8"))
    buffer.seek(0)

    return buffer