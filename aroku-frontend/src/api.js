const BASE = "/api";

export const getToken = () => localStorage.getItem("token");
export const setToken = (t) =>
  t ? localStorage.setItem("token", t) : localStorage.removeItem("token");

async function req(path, opts = {}) {
  const headers = { ...(opts.headers || {}) };
  const token = getToken();
  if (token) headers.Authorization = `Bearer ${token}`;

  const res = await fetch(BASE + path, { ...opts, headers });

  if (res.status === 401 && token) {
    setToken(null);
    window.dispatchEvent(new Event("auth:expired"));
  }
  if (!res.ok) {
    let msg = "Something went wrong. Try again.";
    try {
      const j = await res.json();
      if (typeof j.detail === "string") msg = j.detail;
      else if (Array.isArray(j.detail)) msg = j.detail[0]?.msg || msg;
    } catch {}
    throw new Error(msg);
  }
  return res.json();
}

export async function login(username, password) {
  // Backend uses OAuth2PasswordRequestForm -> form-encoded, not JSON
  const data = await req("/auth/login", {
    method: "POST",
    body: new URLSearchParams({ username, password }),
  });
  setToken(data.access_token);
}

export async function register(username, email, password) {
  await req("/auth/register", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, email, password }),
  });
  await login(username, password);
}

export const me = () => req("/user/me");

// Works with the current backend (input + thread_id as query params).
// See README for the recommended backend change.
export async function sendChat(text, userId) {
  const q = new URLSearchParams({ input: text, thread_id: `user-${userId}` });
  const data = await req(`/chat/ai/chat?${q}`, { method: "POST" });
  return extractReply(data);
}

// Accepts either {reply: "text"} or the full agent state {reply: {messages: [...]}}
function extractReply(data) {
  const r = data?.reply ?? data;
  if (typeof r === "string") return r;
  const last = (r?.messages || []).at(-1);
  const c = last?.content;
  if (typeof c === "string") return c;
  if (Array.isArray(c))
    return c.map((p) => (typeof p === "string" ? p : p.text || "")).join("");
  return "No reply received.";
}

// Streaming version: reads Server-Sent Events from POST /chat/ai/stream
export async function streamChat(text, onToken) {
  const token = getToken();
  const res = await fetch(`${BASE}/chat/ai/stream?${new URLSearchParams({ input: text })}`, {
    method: "POST",
    headers: { Authorization: `Bearer ${token}` },
  });

  if (res.status === 401) {
    setToken(null);
    window.dispatchEvent(new Event("auth:expired"));
    throw new Error("Session expired. Log in again.");
  }
  if (!res.ok || !res.body) throw new Error("Could not reach the agent.");

  const reader = res.body.getReader();
  const decoder = new TextDecoder();
  let buf = "";
  while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    buf += decoder.decode(value, { stream: true });
    const events = buf.split("\n\n");
    buf = events.pop();
    for (const ev of events) {
      if (!ev.startsWith("data: ")) continue;
      const data = ev.slice(6);
      if (data === "[DONE]") return;
      const j = JSON.parse(data);
      if (j.error) throw new Error(j.error);
      if (j.token) onToken(j.token);
    }
  }
}
