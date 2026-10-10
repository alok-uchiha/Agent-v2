import { useCallback, useState } from "react";
import { streamChat } from "../api";

export default function useChat() {
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  const send = useCallback(async (text) => {
    setMessages((m) => [...m, { role: "user", content: text }]);
    setLoading(true);
    let started = false;
    try {
      await streamChat(text, (tok) => {
        const first = !started;
        started = true;
        setMessages((m) =>
          first
            ? [...m, { role: "ai", content: tok }]
            : m.map((x, i) => (i === m.length - 1 ? { ...x, content: x.content + tok } : x))
        );
      });
    } catch (err) {
      setMessages((m) => [...m, { role: "ai", content: err.message, error: true }]);
    } finally {
      setLoading(false);
    }
  }, []);

  const reset = useCallback(() => setMessages([]), []);
  return { messages, loading, send, reset };
}
