// App.jsx
import { useState } from "react";
import SearchBar from "./components/SearchBar";
import LoadingState from "./components/LoadingState";
import ProductCard from "./components/ProductCard";

export default function App() {
  const [isLoading, setIsLoading] = useState(false);
  const [products, setProducts] = useState([]);
  const [error, setError] = useState(null);
  const [lastQuery, setLastQuery] = useState("");
  const [message, setMessage] = useState(null);

  const handleSearch = async (query) => {
    setIsLoading(true);
    setProducts([]);
    setError(null);
    setMessage(null);
    setLastQuery(query);

    try {
      const response = await fetch("/api/search", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query }),
      });

      const data = await response.json();

      if (!response.ok) {
        setError(data.error || "Something went wrong. Please try again.");
        return;
      }

      setProducts(data.products || []);
      setMessage(data.message || null);

    } catch (err) {
      setError("Could not reach the server. Make sure the backend is running.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div style={{ minHeight: "100vh" }}>

      {/* sticky search bar */}
      <div
        style={{
          position: "sticky",
          top: 0,
          zIndex: 10,
          padding: "16px",
          background: "rgba(253, 244, 248, 0.88)",
          backdropFilter: "blur(12px)",
          WebkitBackdropFilter: "blur(12px)",
          borderBottom: "1px solid rgba(249, 198, 216, 0.3)",
        }}
      >
        <div style={{ maxWidth: "64rem", margin: "0 auto" }}>
          <SearchBar onSearch={handleSearch} isLoading={isLoading} />
        </div>
      </div>

      {/* scrollable content */}
      <div style={{ maxWidth: "64rem", margin: "0 auto", padding: "2.5rem 1rem" }}>
        <div style={{ display: "flex", flexDirection: "column", gap: "2.5rem" }}>

          {isLoading && <LoadingState />}

          {error && !isLoading && (
            <div className="rounded-2xl p-6 text-center" style={{ background: "var(--gradient-dreamy)" }}>
              <p style={{ color: "var(--text-primary)" }}>⚠️ {error}</p>
            </div>
          )}

          {message && !isLoading && products.length === 0 && (
            <div className="rounded-2xl p-6 text-center" style={{ background: "var(--gradient-dreamy)" }}>
              <p style={{ color: "var(--text-secondary)" }}>🌸 {message}</p>
            </div>
          )}

          {products.length > 0 && !isLoading && (
            <div className="text-center">
              <p className="text-sm" style={{ color: "var(--text-muted)" }}>
                Found <strong>{products.length}</strong> products for "{lastQuery}"
              </p>
            </div>
          )}

          {products.length > 0 && !isLoading && (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {products.map((product, index) => (
                <ProductCard key={index} product={product} />
              ))}
            </div>
          )}

        </div>
      </div>
    </div>
  );
}