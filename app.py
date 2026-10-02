from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from pathlib import Path
import json

from agent.core import AGENT_ID, AGENT_VERSION, build_agent_response, evaluate_groundwater, utc_now

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "instance" / "water.db"
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

app = Flask(__name__)
CORS(app)
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_PATH.as_posix()}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class WaterData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    waterLevel = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    lastUpdated = db.Column(db.String(50), nullable=False)


def serialize(record):
    return {
        "id": record.id,
        "waterLevel": record.waterLevel,
        "status": record.status,
        "location": record.location,
        "lastUpdated": record.lastUpdated,
    }


@app.get("/")
def root():
    return jsonify({
        "name": "Groundwater Intelligence Agent",
        "version": AGENT_VERSION,
        "message": "Groundwater monitoring API is running.",
        "endpoints": ["/health", "/water-data", "/agent/passport", "/agent/invoke", "/agent/verify"],
    })


@app.get("/health")
def health():
    return jsonify({"status": "ok", "agentId": AGENT_ID, "version": AGENT_VERSION, "timestamp": utc_now()})


@app.get("/water-data")
def water_data():
    data = WaterData.query.order_by(WaterData.id.asc()).first()
    if not data:
        evaluation = evaluate_groundwater(16.8)
        data = WaterData(
            waterLevel=evaluation["waterLevel"],
            status=evaluation["status"],
            location="Karur",
            lastUpdated=utc_now(),
        )
        db.session.add(data)
        db.session.commit()
    return jsonify(serialize(data))


@app.post("/update-data")
def update_data():
    payload = request.get_json(silent=True) or {}
    if "waterLevel" not in payload or "location" not in payload:
        return jsonify({"error": "waterLevel and location are required"}), 400
    try:
        evaluation = evaluate_groundwater(payload["waterLevel"])
    except (TypeError, ValueError):
        return jsonify({"error": "waterLevel must be a number"}), 400

    record = WaterData.query.order_by(WaterData.id.asc()).first()
    if record is None:
        record = WaterData()
        db.session.add(record)
    record.waterLevel = evaluation["waterLevel"]
    record.status = payload.get("status") or evaluation["status"]
    record.location = str(payload["location"])
    record.lastUpdated = utc_now()
    db.session.commit()
    return jsonify({"message": "Data Updated Successfully", "data": serialize(record), "agentAssessment": evaluation})


@app.get("/.well-known/agent-passport.json")
def well_known_passport():
    passport_path = BASE_DIR / "agent" / "passport.json"
    return jsonify(json.loads(passport_path.read_text(encoding="utf-8")))


@app.get("/agent/passport")
def passport():
    passport_path = BASE_DIR / "agent" / "passport.json"
    return jsonify(json.loads(passport_path.read_text(encoding="utf-8")))


@app.post("/agent/invoke")
def invoke_agent():
    payload = request.get_json(silent=True) or {}
    if "waterLevel" not in payload:
        return jsonify({"error": "waterLevel is required"}), 400
    try:
        result = build_agent_response({
            "waterLevel": payload["waterLevel"],
            "location": payload.get("location", "Unknown"),
        })
    except (TypeError, ValueError):
        return jsonify({"error": "waterLevel must be a number"}), 400
    return jsonify(result)


@app.post("/agent/verify")
def verify_agent():
    payload = request.get_json(silent=True) or {}
    try:
        expected = evaluate_groundwater(payload["waterLevel"])
    except (KeyError, TypeError, ValueError):
        return jsonify({"verified": False, "error": "waterLevel is required and must be numeric"}), 400
    supplied = payload.get("assessment", {})
    checks = {
        "agentId": payload.get("agent", {}).get("id") == AGENT_ID,
        "version": payload.get("agent", {}).get("version") == AGENT_VERSION,
        "waterLevel": supplied.get("waterLevel") == expected["waterLevel"],
        "status": supplied.get("status") == expected["status"],
        "risk": supplied.get("risk") == expected["risk"],
    }
    return jsonify({
        "verified": all(checks.values()),
        "agentId": AGENT_ID,
        "checks": checks,
        "expected": expected,
        "timestamp": utc_now(),
    })


with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
