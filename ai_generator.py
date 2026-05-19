import ollama
from pm_rules import get_pm_rules


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