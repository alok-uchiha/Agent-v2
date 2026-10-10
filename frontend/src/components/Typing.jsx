import Spark from "./Spark.jsx";

export default function Typing() {
  return (
    <div className="msg ai">
      <Spark size={20} spin />
      <div className="dots"><i /><i /><i /></div>
    </div>
  );
}
