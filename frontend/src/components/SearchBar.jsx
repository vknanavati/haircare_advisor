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
    </div>
  );
}