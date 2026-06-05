// SearchBar.jsx
// ─────────────────────────────────────────────────────────────────────────────
// The search input and submit button at the top of the app.
// Accepts the user's natural language query and triggers the search.
//
// Plain explanation:
//   This component renders a text input and a button. When the user
//   types a query and clicks Search (or presses Enter), it calls the
//   onSearch function passed down from App.jsx with the query string.
//   While a search is in progress, the button is disabled so the user
//   can't submit multiple requests at once.
//
// Analogy:
//   Think of this as the front desk of the research operation. The user
//   walks up, states their request, and the front desk (SearchBar) passes
//   it back to the manager (App.jsx) to kick off the pipeline.
// ─────────────────────────────────────────────────────────────────────────────

import { useState } from "react";  // useState lets us track what the user typed

export default function SearchBar({ onSearch, isLoading }) {
  // query holds whatever the user has typed in the input box
  const [query, setQuery] = useState("");

  // called when the user clicks Search or presses Enter
  const handleSubmit = () => {
    const trimmed = query.trim();  // remove leading/trailing whitespace
    if (trimmed && !isLoading) {   // only search if there's a query and we're not already loading
      onSearch(trimmed);           // pass the query up to App.jsx
    }
  };

  // allows pressing Enter to submit instead of clicking the button
  const handleKeyDown = (e) => {
    if (e.key === "Enter") handleSubmit();
  };

  return (
    <div className="w-full max-w-2xl mx-auto">

      {/* ── Title and subtitle ──────────────────────────────────────────── */}
      <div className="text-center mb-8">
        <h1 className="text-4xl font-bold mb-2" style={{ color: "var(--text-primary)" }}>
          ✨ Haircare Advisor
        </h1>
        <p className="text-lg" style={{ color: "var(--text-secondary)" }}>
          Real recommendations from real people — powered by Reddit & AI
        </p>
      </div>

      {/* ── Search input row ────────────────────────────────────────────── */}
      <div className="flex gap-3">
        <input
          type="text"
          className="input-dreamy flex-1 px-6 py-4 text-base"
          placeholder="e.g. heat protectants for fine thick hair..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}  // update query as user types
          onKeyDown={handleKeyDown}                    // submit on Enter key
          disabled={isLoading}                         // disable while loading
          style={{ color: "var(--text-primary)" }}
        />

        <button
          className="btn-dreamy px-8 py-4 text-base"
          onClick={handleSubmit}
          disabled={isLoading || !query.trim()}  // disable if loading or empty
        >
          {isLoading ? "Searching..." : "Search"}
        </button>
      </div>

      {/* ── Helper text below the search bar ────────────────────────────── */}
      <p className="text-center mt-3 text-sm" style={{ color: "var(--text-muted)" }}>
        Try: "moisturizers for curly hair" · "shampoo for oily scalp" · "products for bleached hair"
      </p>

    </div>
  );
}