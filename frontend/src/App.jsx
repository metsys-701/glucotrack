import { useState, useEffect } from "react";

function App() {

  // Login fields
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  // JWT token
  const [token, setToken] = useState(localStorage.getItem("token"));

  // Glucose list
  const [glucoseData, setGlucoseData] = useState([]);

  // New record inputs
  const [newGlucose, setNewGlucose] = useState("");
  const [note, setNote] = useState("");

  const [error, setError] = useState("");


  // Fetch records when token changes
  useEffect(() => {
    if (token) {
      fetchGlucose();
    }
  }, [token]);



  // Login user
  const handleLogin = async (e) => {

    e.preventDefault();

    try {

      const response = await fetch("http://127.0.0.1:8000/auth/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
        body: new URLSearchParams({
          username: email,
          password: password,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Login failed");
      }

      // Save token
      localStorage.setItem("token", data.access_token);
      setToken(data.access_token);

      setError("");

    } catch (err) {

      setError(err.message);

    }
  };



  // Fetch glucose records
  const fetchGlucose = async () => {

    try {

      const response = await fetch(
        "http://127.0.0.1:8000/glucose/?skip=0&limit=10",
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      const data = await response.json();

      setGlucoseData(data.data || []);

    } catch (err) {

      console.error("Fetch error:", err);

    }
  };



  // Add new glucose record
  const addGlucose = async (e) => {

    e.preventDefault();

    try {

      const response = await fetch("http://127.0.0.1:8000/glucose/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          glucose_value: Number(newGlucose),
          note: note,
        }),
      });

      if (!response.ok) {
        throw new Error("Failed to add record");
      }

      // Clear form
      setNewGlucose("");
      setNote("");

      // Refresh list
      fetchGlucose();

    } catch (err) {

      console.error("Add error:", err);

    }
  };



  // Delete glucose record
  const deleteRecord = async (id) => {

    try {

      const response = await fetch(
        `http://127.0.0.1:8000/glucose/${id}`,
        {
          method: "DELETE",
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      if (!response.ok) {
        throw new Error("Delete failed");
      }

      // Refresh records
      fetchGlucose();

    } catch (err) {

      console.error("Delete error:", err);

    }
  };



  // Logout user
  const logout = () => {

    localStorage.removeItem("token");
    setToken(null);
    setGlucoseData([]);

  };



  return (
    <div style={{ padding: "40px", fontFamily: "Arial" }}>

      <h2>GlucoTrack</h2>

      {!token ? (

        <form onSubmit={handleLogin}>

          <input
            type="email"
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />

          <br /><br />

          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />

          <br /><br />

          <button type="submit">Login</button>

          {error && <p style={{ color: "red" }}>{error}</p>}

        </form>

      ) : (

        <div>

          <button onClick={logout}>Logout</button>

          <br /><br />

          <h3>Add Glucose Record</h3>

          <form onSubmit={addGlucose}>

            <input
              type="number"
              placeholder="Glucose value"
              value={newGlucose}
              onChange={(e) => setNewGlucose(e.target.value)}
              required
            />

            <input
              type="text"
              placeholder="Note"
              value={note}
              onChange={(e) => setNote(e.target.value)}
            />

            <button type="submit">Add</button>

          </form>

          <br />

          <h3>Glucose Records</h3>

          {glucoseData.length === 0 ? (

            <p>No records found</p>

          ) : (

            <ul>

              {glucoseData.map((record) => (

                <li key={record.id}>

                  {record.glucose_value} mg/dL — {record.note}

                  <button
                    style={{ marginLeft: "10px" }}
                    onClick={() => deleteRecord(record.id)}
                  >
                    Delete
                  </button>

                </li>

              ))}

            </ul>

          )}

        </div>

      )}

    </div>
  );
}

export default App;