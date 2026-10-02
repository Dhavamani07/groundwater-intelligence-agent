import { useState } from "react";

function Admin() {
  const [waterLevel, setWaterLevel] = useState("");
  const [status, setStatus] = useState("Normal");
  const [location, setLocation] = useState("Karur");

  const updateData = () => {
    fetch("http://127.0.0.1:5000/update-data", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        waterLevel: parseFloat(waterLevel),
        status: status,
        location: location,
        lastUpdated: new Date().toLocaleDateString("en-GB"),
      }),
    })
      .then((res) => res.json())
      .then(() => {
        alert("Data Updated Successfully!");
      });
  };

  return (
    <div style={{ padding: "30px", textAlign: "center" }}>
      <h1>Admin Panel</h1>

      <input
        type="number"
        placeholder="Water Level"
        value={waterLevel}
        onChange={(e) => setWaterLevel(e.target.value)}
      />

      <br /><br />

      <select value={status} onChange={(e) => setStatus(e.target.value)}>
        <option>Normal</option>
        <option>Danger</option>
      </select>

      <br /><br />

      <input
        type="text"
        value={location}
        onChange={(e) => setLocation(e.target.value)}
      />

      <br /><br />

      <button onClick={updateData}>
        Update Data
      </button>
    </div>
  );
}

export default Admin;