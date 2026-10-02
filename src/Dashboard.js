import "./App.css";
import { useState, useEffect } from "react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";
import {
  FaTint,
  FaMapMarkerAlt,
  FaClock,
  FaExclamationTriangle,
} from "react-icons/fa";

function Dashboard() {
  const [waterData, setWaterData] = useState({});
  const [chartData, setChartData] = useState([]);
  const [agentResult, setAgentResult] = useState(null);
  const [agentError, setAgentError] = useState("");

  const fetchWaterData = () => {
    fetch("http://127.0.0.1:5000/water-data")
      .then((res) => res.json())
      .then((data) => {
        setWaterData(data);

        setChartData((prev) => [
          ...prev.slice(-9),
          {
            time: new Date().toLocaleTimeString(),
            level: data.waterLevel,
          },
        ]);
      });
  };

  const runAgent = () => {
    setAgentError("");
    fetch("http://127.0.0.1:5000/agent/invoke", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ waterLevel: waterData.waterLevel, location: waterData.location }),
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.error) throw new Error(data.error);
        setAgentResult(data);
      })
      .catch((err) => setAgentError(err.message));
  };

  useEffect(() => {
    fetchWaterData();

    const interval = setInterval(fetchWaterData, 5000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="container">
      <h1>🌊 Real-Time Groundwater Resource Evaluation Using DWLR Data</h1>

      <button className="refresh-btn" onClick={fetchWaterData}>
        🔄 Refresh Data
      </button>

      <div className="card agent-card">
        <h2>🤖 Groundwater Intelligence Agent</h2>
        <p>The agent evaluates the current DWLR reading using transparent, deterministic rules.</p>
        <button className="refresh-btn" onClick={runAgent}>Run Agent Assessment</button>
        {agentError && <p className="error">{agentError}</p>}
        {agentResult && (
          <div className="agent-result">
            <p><strong>Risk:</strong> {agentResult.assessment.risk}</p>
            <p><strong>Assessment:</strong> {agentResult.assessment.status}</p>
            <p><strong>Recommendation:</strong> {agentResult.assessment.recommendation}</p>
            <small>Agent: {agentResult.agent.id} v{agentResult.agent.version}</small>
          </div>
        )}
      </div>

      <div className="card">
        <h2><FaTint /> Water Level : {waterData.waterLevel} m</h2>

        <h3 style={{ color: waterData.status === "Danger" ? "red" : "green" }}>
          <FaExclamationTriangle /> Status : {waterData.status}
        </h3>

        <p><FaMapMarkerAlt /> Location : {waterData.location}</p>

        <p><FaClock /> Last Updated : {waterData.lastUpdated}</p>
      </div>

      <div style={{ width: "100%", height: 350 }}>
        <ResponsiveContainer>
          <LineChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="time" />
            <YAxis />
            <Tooltip />
            <Line
              type="monotone"
              dataKey="level"
              stroke="#007bff"
              strokeWidth={3}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>
      <p style={{ textAlign: "center" }}>
  System auto-refreshes every 5 seconds.
</p>
    </div>
  );
}
export default Dashboard;