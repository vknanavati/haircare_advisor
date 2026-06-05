// LoadingState.jsx
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
    <div className="flex flex-col items-center justify-center py-20 gap-6">

      <div className="relative w-16 h-16">
        <div
          className="absolute inset-0 rounded-full animate-spin"
          style={{ background: "var(--gradient-glow)", padding: "3px" }}
        >
          <div className="w-full h-full rounded-full bg-white opacity-90" />
        </div>
        <div className="absolute inset-0 flex items-center justify-center text-xl">
          ✨
        </div>
      </div>

      <p
        className="text-base font-medium transition-opacity duration-500"
        style={{ color: "var(--text-secondary)" }}
      >
        {LOADING_MESSAGES[messageIndex]}
      </p>

      <p className="text-sm" style={{ color: "var(--text-muted)" }}>
        This takes about 30–60 seconds — we're reading real Reddit discussions for you
      </p>

    </div>
  );
}