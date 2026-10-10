import { createContext, useContext, useEffect, useState } from "react";
import { Routes, Route, Navigate, useNavigate } from "react-router-dom";
import { getToken, setToken, me } from "./api";
import Home from "./pages/Home.jsx";
import Chat from "./pages/Chat.jsx";

const AuthCtx = createContext(null);
export const useAuth = () => useContext(AuthCtx);

export default function App() {
  const [user, setUser] = useState(null);
  const [ready, setReady] = useState(false);
  const navigate = useNavigate();

  const refresh = async () => {
    if (!getToken()) return setUser(null);
    try {
      setUser(await me());
    } catch {
      setUser(null);
    }
  };

  useEffect(() => {
    refresh().finally(() => setReady(true));
    const onExpired = () => {
      setUser(null);
      navigate("/");
    };
    window.addEventListener("auth:expired", onExpired);
    return () => window.removeEventListener("auth:expired", onExpired);
  }, []);

  const logout = () => {
    setToken(null);
    setUser(null);
    navigate("/");
  };

  if (!ready) return null;

  return (
    <AuthCtx.Provider value={{ user, refresh, logout }}>
      <Routes>
        <Route path="/" element={user ? <Navigate to="/chat" /> : <Home />} />
        <Route path="/chat" element={user ? <Chat /> : <Navigate to="/" />} />
        <Route path="*" element={<Navigate to="/" />} />
      </Routes>
    </AuthCtx.Provider>
  );
}
