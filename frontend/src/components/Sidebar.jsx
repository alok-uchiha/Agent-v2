import Spark from "./Spark.jsx";

const Icon = ({ d }) => (
  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d={d} />
  </svg>
);

export default function Sidebar({ username, onNew, onLogout }) {
  return (
    <aside className="rail">
      <Spark />
      <button className="icon" title="New chat" onClick={onNew}><Icon d="M12 5v14M5 12h14" /></button>
      <div className="grow" />
      <button className="icon" title="Log out" onClick={onLogout}>
        <Icon d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4M16 17l5-5-5-5M21 12H9" />
      </button>
      <span className="avatar" title={username}>{username[0].toUpperCase()}</span>
    </aside>
  );
}
