import ReactMarkdown from "react-markdown";
import Spark from "./Spark.jsx";

export default function Message({ role, content, error, streaming }) {
  if (role === "user") {
    return (
      <div className="msg user">
        <div className="bubble">{content}</div>
      </div>
    );
  }
  return (
    <div className={"msg ai" + (error ? " bad" : "")}>
      <Spark size={20} spin={streaming} />
      <div className="bubble md">
        <ReactMarkdown>{content}</ReactMarkdown>
        {streaming && <span className="caret" />}
      </div>
    </div>
  );
}
