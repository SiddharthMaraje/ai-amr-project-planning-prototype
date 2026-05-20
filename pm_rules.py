def get_deployment_scale_rules(deployment_scale):
    scale_rules = {
        "Pilot": {
            "planning_depth": "Light planning depth",
            "rollout_strategy": "Small controlled pilot in one limited warehouse area",
            "additional_workstreams": [
                "Pilot validation",
                "User feedback collection",
                "Basic performance review"
            ],
            "additional_risks": [
                "Pilot results may not represent full warehouse complexity",
                "Limited user adoption during pilot phase"
            ],
            "key_milestones": [
                "Pilot scope approved",
                "Pilot deployment completed",
                "Pilot feedback reviewed"
            ]
        },

        "Single-Zone Rollout": {
            "planning_depth": "Moderate planning depth",
            "rollout_strategy": "Deployment in one defined operational zone",
            "additional_workstreams": [
                "Zone readiness assessment",
                "Zone-specific training",
                "Operational handover"
            ],
            "additional_risks": [
                "Disruption in selected warehouse zone",
                "Insufficient coordination with zone supervisors"
            ],
            "key_milestones": [
                "Zone readiness confirmed",
                "Single-zone rollout completed",
                "Zone handover completed"
            ]
        },

        "Multi-Zone Rollout": {
            "planning_depth": "High planning depth",
            "rollout_strategy": "Phased rollout across multiple warehouse zones",
            "additional_workstreams": [
                "Phased rollout planning",
                "Cross-zone dependency management",
                "Multi-zone training coordination",
                "Operational continuity planning"
            ],
            "additional_risks": [
                "Interdependency conflicts between warehouse zones",
                "Inconsistent adoption across zones",
                "Higher coordination complexity"
            ],
            "key_milestones": [
                "Multi-zone rollout plan approved",
                "First zone deployed",
                "All selected zones deployed",
                "Cross-zone operations stabilized"
            ]
        },

        "Full Warehouse Rollout": {
            "planning_depth": "Very high planning depth",
            "rollout_strategy": "End-to-end deployment across warehouse logistics operations",
            "additional_workstreams": [
                "Full warehouse transition planning",
                "Change management",
                "Large-scale training",
                "Cutover planning",
                "Post-go-live stabilization"
            ],
            "additional_risks": [
                "Major operational disruption during rollout",
                "Resistance to process change",
                "High dependency on vendor and internal teams",
                "Insufficient stabilization after go-live"
            ],
            "key_milestones": [
                "Full rollout plan approved",
                "Warehouse-wide training completed",
                "Go-live completed",
                "Post-go-live stabilization completed"
            ]
        }
    }

    return scale_rules.get(deployment_scale, scale_rules["Pilot"])


def get_pm_rules(integration_complexity, deployment_scale):
    complexity_rules = {
        "Low": {
            "governance_level": "Light governance",
            "mandatory_workstreams": [
                "Project initiation",
                "Basic stakeholder alignment",
                "Vendor coordination",
                "Pilot deployment",
                "Basic training"
            ],
            "risks": [
                "Limited stakeholder involvement",
                "Underestimated operational impact"
            ],
            "milestones": [
                "Project charter approved",
                "Pilot deployment completed",
                "Basic training completed"
            ]
        },

        "Medium": {
            "governance_level": "Structured governance",
            "mandatory_workstreams": [
                "Project initiation",
                "Stakeholder management",
                "System integration planning",
                "Operational readiness",
                "Training and change management",
                "Rollout coordination"
            ],
            "risks": [
                "Integration delays",
                "Stakeholder misalignment",
                "Operational disruption during rollout"
            ],
            "milestones": [
                "Project charter approved",
                "Integration plan approved",
                "Operational readiness confirmed",
                "Rollout completed"
            ]
        },

        "High": {
            "governance_level": "Strong governance",
            "mandatory_workstreams": [
                "Project initiation",
                "Detailed stakeholder management",
                "Complex system integration planning",
                "Dependency management",
                "Risk and issue management",
                "Change management",
                "Training strategy",
                "Phased rollout planning",
                "Post-go-live stabilization"
            ],
            "risks": [
                "Complex integration dependencies",
                "High operational disruption risk",
                "Resistance to change",
                "Vendor delivery delays",
                "Insufficient rollout governance"
            ],
            "milestones": [
                "Project charter approved",
                "Integration design approved",
                "Risk review completed",
                "Phased rollout completed",
                "Stabilization completed"
            ]
        }
    }

    rules = complexity_rules.get(integration_complexity, complexity_rules["Medium"])
    scale_rules = get_deployment_scale_rules(deployment_scale)

    return {
        "integration_complexity": integration_complexity,
        "deployment_scale": deployment_scale,
        "governance_level": rules["governance_level"],
        "planning_depth": scale_rules["planning_depth"],
        "rollout_strategy": scale_rules["rollout_strategy"],
        "mandatory_workstreams": rules["mandatory_workstreams"] + scale_rules["additional_workstreams"],
        "risks": rules["risks"] + scale_rules["additional_risks"],
        "milestones": rules["milestones"] + scale_rules["key_milestones"]
    }