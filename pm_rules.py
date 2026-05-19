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