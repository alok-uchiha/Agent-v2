// Fades in text word by word
export default function RevealText({ text, as: Tag = "h1", className = "", step = 70 }) {
  return (
    <Tag className={"reveal " + className} aria-label={text}>
      {text.split(" ").map((w, i) => (
        <span key={i} aria-hidden="true" style={{ animationDelay: `${i * step}ms` }}>
          {w}&nbsp;
        </span>
      ))}
    </Tag>
  );
}
