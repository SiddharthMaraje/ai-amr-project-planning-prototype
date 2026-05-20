import json
from io import BytesIO
import matplotlib.pyplot as plt


def clean_timeline_json(llm_response):
    cleaned_response = llm_response.strip()

    cleaned_response = cleaned_response.replace("```json", "")
    cleaned_response = cleaned_response.replace("```", "")

    return cleaned_response.strip()


def parse_timeline_json(llm_response):
    cleaned_response = clean_timeline_json(llm_response)

    try:
        timeline_data = json.loads(cleaned_response)
        return timeline_data
    except json.JSONDecodeError:
        return []


def create_gantt_chart(timeline_data):
    if not timeline_data:
        return None, None

    tasks = [item["task"] for item in timeline_data]
    start_weeks = [item["start_week"] for item in timeline_data]
    durations = [item["duration_weeks"] for item in timeline_data]

    fig, ax = plt.subplots(figsize=(11, 6))

    ax.barh(tasks, durations, left=start_weeks)

    ax.set_xlabel("Project Week")
    ax.set_ylabel("Project Activities")
    ax.set_title("AI-Generated AMR Deployment Gantt Chart")

    ax.invert_yaxis()
    ax.grid(axis="x", linestyle="--", alpha=0.5)

    buffer = BytesIO()
    fig.tight_layout()
    fig.savefig(buffer, format="png")
    buffer.seek(0)

    return fig, buffer