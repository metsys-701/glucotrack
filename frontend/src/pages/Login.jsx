import { useState } from "react";
import { loginUser } from "../services/api";

function Login({ setToken }) {

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const handleLogin = async (e) => {
    e.preventDefault();

    try {

      const data = await loginUser(email, password);

      localStorage.setItem("token", data.access_token);
      setToken(data.access_token);

    } catch (err) {

      setError(err.message);

    }
  };

  return (
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

      {error && <p style={{color:"red"}}>{error}</p>}

    </form>
  );
}

export default Login;