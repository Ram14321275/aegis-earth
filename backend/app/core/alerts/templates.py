from typing import Dict

ALERT_TEMPLATES: Dict[str, Dict[str, Dict[str, str]]] = {
    "flood": {
        "HIGH": {
            "title": "Flood Warning",
            "message": "Significant flooding risk detected.",
        },
        "CRITICAL": {
            "title": "Emergency Flood Alert",
            "message": "Critical flooding risk detected. Immediate action may be required.",
        },
    },
    "wildfire": {
        "MODERATE": {
            "title": "Wildfire Watch",
            "message": "Elevated wildfire risk detected. Conditions are favorable for wildfire spread.",
        },
        "HIGH": {
            "title": "Wildfire Warning",
            "message": "Significant wildfire risk detected.",
        },
        "CRITICAL": {
            "title": "Critical Wildfire Alert",
            "message": "Critical wildfire risk detected. Immediate action may be required.",
        },
    },
}


def get_template(hazard_type: str, severity: str) -> Dict[str, str]:
    default = {
        "title": f"{hazard_type.capitalize()} Alert",
        "message": f"{severity.capitalize()} risk detected.",
    }
    return ALERT_TEMPLATES.get(hazard_type.lower(), {}).get(severity.upper(), default)
