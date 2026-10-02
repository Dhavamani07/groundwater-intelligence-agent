import json
from pathlib import Path
from agent.core import AGENT_ID, build_agent_response, evaluate_groundwater


def test_deterministic_evaluation():
    assert evaluate_groundwater(8.5) == evaluate_groundwater(8.5)


def test_agent_response_contract():
    result = build_agent_response({"waterLevel": 8.5, "location": "Karur"})
    assert result["agent"]["id"] == AGENT_ID
    assert set(result["assessment"]) == {"waterLevel", "status", "risk", "recommendation"}


def test_passport_files_exist():
    assert Path("agent/passport.json").exists()
    assert Path(".well-known/agent-passport.json").exists()
    json.loads(Path("agent/passport.json").read_text())
