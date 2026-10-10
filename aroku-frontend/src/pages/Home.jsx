import Glow from "../components/Glow.jsx";
import Spark from "../components/Spark.jsx";
import RevealText from "../components/RevealText.jsx";
import AuthCard from "../components/AuthCard.jsx";

export default function Home() {
  return (
    <div className="stage">
      <Glow />
      <header className="topbar">
        <span className="brand"><Spark size={22} spin />aroku</span>
      </header>
      <main className="home">
        <RevealText className="hero" text="Support that knows your order" />
        <p className="sub">Ask about orders, payments and cancellations. Log in to chat with the aroku support agent.</p>
        <AuthCard />
      </main>
    </div>
  );
}
