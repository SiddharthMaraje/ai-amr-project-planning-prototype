import ollama


def create_project_charter_prompt(
    integration_complexity,
    deployment_scale,
    output_type,
    pm_rules
):

    prompt = f"""
You are an experienced project manager supporting Autonomous Mobile Robot (AMR) deployment projects in warehouse logistics.

Generate a professional Project Charter based on the selected project conditions.

Input Parameters:
- Integration Complexity: {integration_complexity}
- Deployment Scale: {deployment_scale}
- Requested Output Type: {output_type}

Project Management Rules:
- Governance Level: {pm_rules["governance_level"]}
- Planning Depth: {pm_rules["planning_depth"]}
- Rollout Strategy: {pm_rules["rollout_strategy"]}
- Estimated Timeline: {pm_rules["estimated_timeline"]}

Mandatory Workstreams:
{pm_rules["mandatory_workstreams"]}

Required Stakeholders:
{pm_rules["stakeholders"]}

Required Governance Mechanisms:
{pm_rules["governance_mechanisms"]}

Key Risks:
{pm_rules["risks"]}

Key Milestones:
{pm_rules["milestones"]}

Success Criteria:
{pm_rules["success_criteria"]}

Instructions:
- Generate ONLY a Project Charter.
- Use exactly the section structure provided below.
- Do not remove, rename, or add sections.
- Keep the output focused on project management.
- Do not go too deep into robotics engineering details.
- Make the output practical and suitable for a capstone prototype.
- Use the required stakeholders, governance mechanisms, risks, milestones, and success criteria.
- Avoid generic statements unless linked to warehouse operations.
- Make objectives SMART-style where possible.
- The depth should match the selected integration complexity.
- Mention inbound, storage, picking, and outbound operations where relevant.

Required Project Charter Format:

1. Project Title

2. Project Background

3. Business Case

4. Project Objectives

5. Project Scope

6. Out of Scope

7. Key Deliverables

8. Stakeholders

9. Governance Approach

10. Assumptions

11. Constraints

12. Risks

13. Milestones

14. Success Criteria

15. Approval / Sign-off
"""

    return prompt


def create_general_pm_prompt(
    integration_complexity,
    deployment_scale,
    output_type,
    pm_rules
):

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
- Estimated Timeline: {pm_rules["estimated_timeline"]}

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

If the requested output type is Timeline:
- Create a clear week-based timeline.
- Use project weeks, for example Week 1-2, Week 3-5, etc.
- Include activity names and short descriptions.
- Make the sequence realistic for the selected integration complexity and deployment scale.
"""

    return prompt


def generate_ai_output(
    integration_complexity,
    deployment_scale,
    output_type,
    pm_rules
):

    if output_type == "Project Charter":
        prompt = create_project_charter_prompt(
            integration_complexity,
            deployment_scale,
            output_type,
            pm_rules
        )
    else:
        prompt = create_general_pm_prompt(
            integration_complexity,
            deployment_scale,
            output_type,
            pm_rules
        )

    response = ollama.chat(
        model="deepseek-r1:7b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    ai_output = response["message"]["content"]

    return prompt, ai_output


def generate_timeline_json_from_text(timeline_text):

    prompt = f"""
You are a project planning data extraction assistant.

Convert the following AI-generated project timeline into structured JSON for a Gantt chart.

AI-GENERATED TIMELINE:
{timeline_text}

Return ONLY valid JSON.

Required JSON format:

[
  {{
    "task": "Project Initiation",
    "start_week": 1,
    "duration_weeks": 2
  }},
  {{
    "task": "Stakeholder Alignment",
    "start_week": 3,
    "duration_weeks": 2
  }}
]

Rules:
- Return only a JSON array.
- Do not include markdown.
- Do not include explanation.
- Do not include text before or after the JSON.
- Use double quotes only.
- Use integer values only.
- start_week must be the first week of the task.
- duration_weeks must be the number of weeks the task lasts.
- Preserve the same task sequence from the AI-generated timeline.
- Do not invent unrelated tasks.
"""

    response = ollama.chat(
        model="deepseek-r1:7b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"]