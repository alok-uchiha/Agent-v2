import { useRef } from "react";

export default function Composer({ value, onChange, onSend, busy }) {
  const ref = useRef(null);

  const handleInput = (e) => {
    onChange(e.target.value);
    e.target.style.height = "auto";
    e.target.style.height = Math.min(e.target.scrollHeight, 180) + "px";
  };

  const handleKey = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      submit();
    }
  };

  const submit = () => {
    if (!value.trim() || busy) return;
    onSend();
    if (ref.current) ref.current.style.height = "auto";
  };

  return (
    <div className="composer">
      <textarea
        ref={ref}
        rows={1}
        autoFocus
        placeholder="Ask aroku support"
        value={value}
        onChange={handleInput}
        onKeyDown={handleKey}
      />
      <button className="send" onClick={submit} disabled={!value.trim() || busy} aria-label="Send message">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round">
          <path d="M12 19V5M5 12l7-7 7 7" />
        </svg>
      </button>
    </div>
  );
}
