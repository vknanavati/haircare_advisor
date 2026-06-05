import { useState } from "react";

export default function SearchBar({ onSearch, isLoading }) {
  const [query, setQuery] = useState("");

  const handleSubmit = () => {
    const trimmed = query.trim();
    if (trimmed && !isLoading) onSearch(trimmed);
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter") handleSubmit();
  };

  return (
    <div style={{ width: "100%", maxWidth: "680px", margin: "0 auto" }}>

      {/* title */}
      <div style={{ textAlign: "center", marginBottom: "28px" }}>
        <h1 style={{
          fontFamily: "'Fraunces', serif",
          fontSize: "clamp(2rem, 5vw, 3.2rem)",
          fontWeight: 700,
          color: "white",
          lineHeight: 1.1,
          marginBottom: "8px",
          letterSpacing: "-0.01em",
        }}>
          <span style={{ color: "var(--gold-star)" }}>✦</span> Haircare Advisor <span style={{ color: "var(--pool-blue)" }}>✦</span>
        </h1>
        <p style={{
          fontFamily: "'DM Sans', sans-serif",
          fontSize: "1rem",
          color: "rgba(255,255,255,0.75)",
          fontWeight: 300,
        }}>
          Real recommendations from real people — powered by Reddit &amp; AI
        </p>
      </div>

      {/* search row */}
      <div style={{ display: "flex", gap: "10px", alignItems: "center" }}>
        <input
          type="text"
          className="input-glass"
          style={{ flex: 1, padding: "14px 24px", fontSize: "0.95rem" }}
          placeholder="e.g. heat protectants for fine thick hair..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={handleKeyDown}
          disabled={isLoading}
        />
        <button
          className="btn-pill"
          style={{ padding: "14px 28px", fontSize: "0.95rem" }}
          onClick={handleSubmit}
          disabled={isLoading || !query.trim()}
        >
          {isLoading ? "Searching..." : "Search"}
        </button>
      </div>

      {/* helper */}
      <p style={{
        textAlign: "center",
        marginTop: "12px",
        fontSize: "0.8rem",
        color: "rgba(255,255,255,0.5)",
        fontFamily: "'DM Sans', sans-serif",
      }}>
        Try: "moisturizers for curly hair" · "shampoo for oily scalp" · "products for bleached hair"
      </p>

    </div>
  );
}