import { useState, useEffect } from "react";

function App() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [token, setToken] = useState(localStorage.getItem("token") || null);
  const [glucoseData, setGlucoseData] = useState([]);
  const [error, setError] = useState("");

  // Fetch glucose records after login
  useEffect(() => {
    if (token) {
      fetchGlucose();
    }
  }, [token]);

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

      localStorage.setItem("token", data.access_token);
      setToken(data.access_token);
      setError("");

    } catch (err) {
      setError(err.message);
    }
  };

  const fetchGlucose = async () => {
    if (!token) return;

    try {
      const response = await fetch(
        "http://127.0.0.1:8000/glucose/?skip=0&limit=5",
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      if (!response.ok) {
        console.error("Unauthorized or server error");
        setGlucoseData([]);
        return;
      }

      const data = await response.json();

      // Backend pagination response
      if (data.data) {
        setGlucoseData(data.data);
      } else {
        setGlucoseData([]);
      }

    } catch (err) {
      console.error("Error fetching glucose data:", err);
      setGlucoseData([]);
    }
  };

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

          <h3>Glucose Records</h3>

          {glucoseData.length === 0 ? (
            <p>No records found</p>
          ) : (
            <ul>
              {glucoseData.map((record) => (
                <li key={record.id}>
                  {record.glucose_value} mg/dL — {record.note}
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