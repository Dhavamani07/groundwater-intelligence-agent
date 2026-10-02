# Groundwater Intelligence Agent

**Existing project preserved:** Real-Time Groundwater Resource Evaluation Using DWLR Data.

This version turns the existing dashboard into a modular, portable and verifiable groundwater intelligence agent. The original React + Flask + SQLite flow remains; the agent logic is isolated from the UI and transport layer.

## What was added

- **Portable agent core:** `agent/core.py`
- **Behavior contract:** `agent/contract.json`
- **Agent Passport:** `agent/passport.json` and `/.well-known/agent-passport.json`
- **Machine API:** `/agent/invoke`
- **Independent verification:** `/agent/verify` and `verify_agent.py`
- **Health/discovery endpoint:** `/health`
- **CLI transport:** `agent_cli.py` accepts JSON on stdin and emits JSON on stdout
- **Verification tests:** `tests/test_agent_contract.py`
- **Frontend agent panel:** run an assessment from the existing dashboard

The challenge emphasizes portability across frameworks/runtimes, behavior contracts, technical verification and documentation. This architecture keeps the groundwater capability independent of React and Flask, while exposing a stable JSON contract that another runtime can call. citeturn1search0turn1search6

## Run locally

### 1. Backend

```bash
python -m venv .venv
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

API: `http://127.0.0.1:5000`

### 2. Frontend

Open a second terminal:

```bash
npm install
npm start
```

Dashboard: `http://localhost:3000`

## Agent API

### Health
`GET /health`

### Passport
`GET /agent/passport`

### Invoke
`POST /agent/invoke`

```json
{"waterLevel": 8.5, "location": "Karur"}
```

### Verify
`POST /agent/verify`

Send the agent response together with the original `waterLevel`; the verifier recomputes the deterministic assessment and reports which checks passed.

## Framework/runtime portability

The portable boundary is JSON. The same agent core can be called by:

1. Flask (`/agent/invoke`)
2. CLI (`python agent_cli.py`)
3. Another HTTP client or agent runtime using the documented input/output contract

This avoids putting groundwater business logic inside React or a framework-specific agent class.

## Local verification

No Flask or Node dependency is needed for the basic agent verification:

```bash
python verify_agent.py
```

Expected result contains:

```json
{"verified": true}
```

## Important note about the passport

The local passport is a project-level identity/capability manifest for the challenge. It is **not** a cryptographically issued third-party passport token. Official challenge/platform verification must still be completed through the designated HiDevs checkpoints. citeturn1search2turn1search4
