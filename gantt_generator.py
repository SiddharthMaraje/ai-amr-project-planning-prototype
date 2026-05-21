import json
import re
from io import BytesIO
import matplotlib.pyplot as plt


def extract_json_array(llm_response):
    cleaned = llm_response.strip()
    cleaned = cleaned.replace("```json", "")
    cleaned = cleaned.replace("```", "")
    cleaned = cleaned.strip()

    match = re.search(r"\[.*\]", cleaned, re.DOTALL)

    if match:
        return match.group(0)

    return cleaned


def parse_timeline_json(llm_response):
    cleaned_response = extract_json_array(llm_response)

    try:
        timeline_data = json.loads(cleaned_response)

        valid_timeline = []

        for item in timeline_data:
            if (
                "task" in item
                and "start_week" in item
                and "duration_weeks" in item
            ):
                valid_timeline.append(
                    {
                        "task": str(item["task"]),
                        "start_week": int(item["start_week"]),
                        "duration_weeks": int(item["duration_weeks"])
                    }
                )

        return valid_timeline

    except Exception:
        return []


def create_gantt_chart(timeline_data):
    if not timeline_data:
        return None, None

    tasks = [item["task"] for item in timeline_data]
    start_weeks = [item["start_week"] for item in timeline_data]
    durations = [item["duration_weeks"] for item in timeline_data]

    fig, ax = plt.subplots(figsize=(12, 7))

    ax.barh(tasks, durations, left=start_weeks)

    ax.set_xlabel("Project Week")
    ax.set_ylabel("Project Activities")
    ax.set_title("Gantt Chart Generated from AI Timeline")

    ax.invert_yaxis()
    ax.grid(axis="x", linestyle="--", alpha=0.5)

    buffer = BytesIO()
    fig.tight_layout()
    fig.savefig(buffer, format="png", dpi=150)
    buffer.seek(0)

    return fig, buffer