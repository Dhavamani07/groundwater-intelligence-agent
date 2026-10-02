"""Local, dependency-free verification for the Groundwater Intelligence Agent."""
import json
from agent.core import AGENT_ID, AGENT_VERSION, build_agent_response, evaluate_groundwater


def check(condition, message):
    if not condition:
        raise AssertionError(message)


def main():
    sample = build_agent_response({"waterLevel": 8.5, "location": "Karur"})
    expected = evaluate_groundwater(8.5)
    check(sample["agent"]["id"] == AGENT_ID, "agent id mismatch")
    check(sample["agent"]["version"] == AGENT_VERSION, "agent version mismatch")
    check(sample["assessment"] == expected, "assessment mismatch")
    check("timestamp" in sample, "timestamp missing")
    print(json.dumps({"verified": True, "checks": ["identity", "contract", "deterministic-assessment", "timestamp"]}, indent=2))


if __name__ == "__main__":
    main()
