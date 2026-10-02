import json
import sys
from agent.core import build_agent_response


def main():
    raw = sys.stdin.read().strip()
    if not raw:
        print(json.dumps({"error": "Provide JSON on stdin"}))
        return 1
    try:
        payload = json.loads(raw)
        print(json.dumps(build_agent_response(payload), indent=2))
        return 0
    except (json.JSONDecodeError, KeyError, TypeError, ValueError) as exc:
        print(json.dumps({"error": str(exc)}))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
