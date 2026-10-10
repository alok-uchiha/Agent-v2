import { useEffect, useRef, useState } from "react";
import { useAuth } from "../App.jsx";
import useChat from "../hooks/useChat.js";
import Glow from "../components/Glow.jsx";
import Sidebar from "../components/Sidebar.jsx";
import Composer from "../components/Composer.jsx";
import Message from "../components/Message.jsx";
import Typing from "../components/Typing.jsx";
import RevealText from "../components/RevealText.jsx";

const SUGGESTIONS = ["Where is my order?", "Cancel my last order", "Check my payment status"];

export default function Chat() {
  const { user, logout } = useAuth();
  const { messages, loading, send, reset } = useChat();
  const [text, setText] = useState("");
  const endRef = useRef(null);

  useEffect(() => {
    endRef.current?.scrollIntoView({ behavior: "smooth", block: "end" });
  }, [messages, loading]);

  const submit = (value) => {
    const v = (value ?? text).trim();
    if (!v || loading) return;
    setText("");
    send(v);
  };

  const empty = messages.length === 0;
  const last = messages.at(-1);
  const waiting = loading && last?.role === "user";

  return (
    <div className="stage chat">
      <Glow />
      <Sidebar username={user.username} onNew={reset} onLogout={logout} />

      <main className={"pane" + (empty ? " empty" : "")}>
        {empty ? (
          <div className="center">
            <RevealText className="greet" text={`Let's jump in, ${user.username}`} />
            <div className="rise-1"><Composer value={text} onChange={setText} onSend={() => submit()} busy={loading} /></div>
            <div className="chips rise-2">
              {SUGGESTIONS.map((s) => (
                <button key={s} onClick={() => submit(s)}>{s}</button>
              ))}
            </div>
          </div>
        ) : (
          <>
            <div className="thread">
              <div className="thread-inner">
                {messages.map((m, i) => (
                  <Message key={i} {...m} streaming={loading && i === messages.length - 1 && m.role === "ai"} />
                ))}
                {waiting && <Typing />}
                <div ref={endRef} />
              </div>
            </div>
            <div className="dock">
              <Composer value={text} onChange={setText} onSend={() => submit()} busy={loading} />
            </div>
          </>
        )}
      </main>
    </div>
  );
}
