import ollama


def generate_ai_output(integration_complexity, deployment_scale, output_type, pm_rules):
    prompt = f"""
You are an experienced project manager supporting AMR deployment projects in warehouse logistics.

Generate a professional project management planning output based on the following inputs.

Input Parameters:
- Integration Complexity: {integration_complexity}
- Deployment Scale: {deployment_scale}
- Requested Output Type: {output_type}

Project Management Rules:
- Governance Level: {pm_rules["governance_level"]}
- Planning Depth: {pm_rules["planning_depth"]}
- Rollout Strategy: {pm_rules["rollout_strategy"]}

Mandatory Workstreams:
{pm_rules["mandatory_workstreams"]}

Key Risks:
{pm_rules["risks"]}

Key Milestones:
{pm_rules["milestones"]}

Instructions:
- Keep the output focused on project management.
- Do not go too deep into robotics engineering details.
- Emphasize planning, governance, stakeholder coordination, rollout, risk management, and operational readiness.
- Make the output practical and suitable for a capstone prototype.
- Format the answer clearly using headings and bullet points.
- Generate only the requested output type: {output_type}.
"""

    response = ollama.chat(
        model="llama3",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"]