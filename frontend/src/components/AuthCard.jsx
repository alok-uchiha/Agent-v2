import { useState } from "react";
import { login, register } from "../api";
import { useAuth } from "../App.jsx";

export default function AuthCard() {
  const [mode, setMode] = useState("login");
  const [form, setForm] = useState({ username: "", email: "", password: "" });
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);
  const { refresh } = useAuth();
  const set = (k) => (e) => setForm({ ...form, [k]: e.target.value });

  async function submit(e) {
    e.preventDefault();
    setError("");
    setBusy(true);
    try {
      if (mode === "login") await login(form.username, form.password);
      else await register(form.username, form.email, form.password);
      await refresh();
    } catch (err) {
      setError(err.message);
    } finally {
      setBusy(false);
    }
  }

  return (
    <form className="card" onSubmit={submit}>
      <div className="tabs" data-mode={mode}>
        <button type="button" className={mode === "login" ? "on" : ""} onClick={() => setMode("login")}>Log in</button>
        <button type="button" className={mode === "register" ? "on" : ""} onClick={() => setMode("register")}>Create account</button>
      </div>

      <input placeholder={mode === "login" ? "Username or email" : "Username"} value={form.username} onChange={set("username")} required autoComplete="username" />
      {mode === "register" && (
        <input className="slide-in" type="email" placeholder="Email" value={form.email} onChange={set("email")} required />
      )}
      <input type="password" placeholder="Password" value={form.password} onChange={set("password")} required autoComplete={mode === "login" ? "current-password" : "new-password"} />

      {error && <p className="err">{error}</p>}
      <button className="primary" disabled={busy}>
        {busy ? "Please wait…" : mode === "login" ? "Log in" : "Create account"}
      </button>
    </form>
  );
}
