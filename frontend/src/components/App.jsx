// App.jsx
// ─────────────────────────────────────────────────────────────────────────────
// Root component — manages application state and orchestrates the UI.
//
// Plain explanation:
//   App.jsx holds all the state: the current query, whether we're loading,
//   the product results, and any error messages. It passes state and
//   callbacks down to child components, and calls the Flask API when
//   the user submits a search.
//
// Analogy:
//   App.jsx is the manager of the whole frontend operation. SearchBar is
//   the front desk that takes orders, LoadingState is the "please wait"
//   sign, and ProductCard components are the finished plates. The manager
//   coordinates all of them and decides what's visible at any moment.
// ─────────────────────────────────────────────────────────────────────────────

import { useState } from "react";
import SearchBar from "./components/SearchBar";
import LoadingState from "./components/LoadingState";
import ProductCard from "./components/ProductCard";

export default function App() {
  // ── State ──────────────────────────────────────────────────────────────────
  const [isLoading, setIsLoading] = useState(false);   // true while pipeline runs
  const [products, setProducts] = useState([]);          // array of product summaries
  const [error, setError] = useState(null);              // error message string or null
  const [lastQuery, setLastQuery] = useState("");        // the query that produced results
  const [message, setMessage] = useState(null);          // info message from backend

  // ── Search handler ─────────────────────────────────────────────────────────
  const handleSearch = async (query) => {
    // reset state before starting a new search
    setIsLoading(true);
    setProducts([]);
    setError(null);
    setMessage(null);
    setLastQuery(query);

    try {
      // call the Flask API via the Vite proxy
      // /api/search gets forwarded to http://localhost:5008/search
      const response = await fetch("/api/search", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query }),  // send the query as JSON
      });

      // parse the JSON response
      const data = await response.json();

      if (!response.ok) {
        // if the server returned an error status, show the error message
        setError(data.error || "Something went wrong. Please try again.");
        return;
      }

      // update state with the results
      setProducts(data.products || []);
      setMessage(data.message || null);  // optional info message from backend

    } catch (err) {
      // network error or JSON parsing error
      setError("Could not reach the server. Make sure the backend is running.");
    } finally {
      // always turn off loading spinner when done, success or failure
      setIsLoading(false);
    }
  };

  // ── Render ─────────────────────────────────────────────────────────────────
  return (
    <div className="min-h-screen px-4 py-12">
      <div className="max-w-5xl mx-auto flex flex-col gap-10">

        {/* ── Search bar ────────────────────────────────────────────────── */}
        <SearchBar onSearch={handleSearch} isLoading={isLoading} />

        {/* ── Loading state ─────────────────────────────────────────────── */}
        {isLoading && <LoadingState />}

        {/* ── Error message ─────────────────────────────────────────────── */}
        {error && !isLoading && (
          <div
            className="rounded-2xl p-6 text-center"
            style={{ background: "var(--gradient-dreamy)" }}
          >
            <p className="text-base" style={{ color: "var(--text-primary)" }}>
              ⚠️ {error}
            </p>
          </div>
        )}

        {/* ── Info message (no results) ──────────────────────────────────── */}
        {message && !isLoading && products.length === 0 && (
          <div
            className="rounded-2xl p-6 text-center"
            style={{ background: "var(--gradient-dreamy)" }}
          >
            <p className="text-base" style={{ color: "var(--text-secondary)" }}>
              🌸 {message}
            </p>
          </div>
        )}

        {/* ── Results header ────────────────────────────────────────────── */}
        {products.length > 0 && !isLoading && (
          <div className="text-center">
            <p className="text-sm" style={{ color: "var(--text-muted)" }}>
              Found <strong>{products.length}</strong> products for "{lastQuery}"
            </p>
          </div>
        )}

        {/* ── Product cards grid ────────────────────────────────────────── */}
        {products.length > 0 && !isLoading && (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {products.map((product, index) => (
              <ProductCard key={index} product={product} />
            ))}
          </div>
        )}

      </div>
    </div>
  );
}