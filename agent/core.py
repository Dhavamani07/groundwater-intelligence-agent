from datetime import datetime, timezone

AGENT_ID = "groundwater-intelligence-agent"
AGENT_VERSION = "1.0.0"


def utc_now():
    return datetime.now(timezone.utc).isoformat()


def evaluate_groundwater(water_level):
    """Simple transparent rule-based evaluation for DWLR water-level data."""
    level = float(water_level)
    if level < 5:
        status = "Critical"
        risk = "high"
        recommendation = "Alert the responsible authority and inspect the monitoring point."
    elif level < 10:
        status = "Danger"
        risk = "medium"
        recommendation = "Increase monitoring frequency and review local groundwater conditions."
    else:
        status = "Normal"
        risk = "low"
        recommendation = "Continue routine monitoring."
    return {
        "waterLevel": level,
        "status": status,
        "risk": risk,
        "recommendation": recommendation,
    }


def build_agent_response(data):
    evaluation = evaluate_groundwater(data["waterLevel"])
    return {
        "agent": {"id": AGENT_ID, "version": AGENT_VERSION},
        "input": {
            "waterLevel": evaluation["waterLevel"],
            "location": data.get("location", "Unknown"),
        },
        "assessment": evaluation,
        "timestamp": utc_now(),
    }
