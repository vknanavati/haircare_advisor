import { useState, useEffect } from "react";

const LOADING_MESSAGES = [
  "🔍 Searching Reddit communities...",
  "💬 Reading what people are saying...",
  "✨ Identifying recommended products...",
  "🔬 Researching each product...",
  "📊 Analyzing reviews and ratings...",
  "🌸 Almost done — putting it all together...",
];

export default function LoadingState() {
  const [messageIndex, setMessageIndex] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setMessageIndex((prev) => (prev + 1) % LOADING_MESSAGES.length);
    }, 4000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div style={{
      display: "flex",
      flexDirection: "column",
      alignItems: "center",
      justifyContent: "center",
      padding: "60px 16px",
      gap: "20px",
      textAlign: "center",
    }}>

      {/* spinner ring */}
      <div style={{
        width: "56px",
        height: "56px",
        borderRadius: "50%",
        border: "3px solid rgba(255,255,255,0.2)",
        borderTopColor: "white",
        animation: "spin 0.9s linear infinite",
      }} />

      {/* spinner keyframe */}
      <style>{`
        @keyframes spin {
          to { transform: rotate(360deg); }
        }
      `}</style>

      <p style={{
        fontFamily: "'DM Sans', sans-serif",
        fontSize: "1rem",
        fontWeight: 500,
        color: "white",
      }}>
        {LOADING_MESSAGES[messageIndex]}
      </p>

      <p style={{
        fontFamily: "'DM Sans', sans-serif",
        fontSize: "0.8rem",
        color: "rgba(255,255,255,0.6)",
      }}>
        This takes about 30–60 seconds — we're reading real Reddit discussions for you
      </p>

    </div>
  );
}