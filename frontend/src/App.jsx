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
  const [hasSearched, setHasSearched] = useState(false);

  const handleSearch = async (query) => {
    setIsLoading(true);
    setHasSearched(true);
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
    <div>
      <div style={{
        position: "sticky",
        top: 0,
        zIndex: 100,
        backgroundColor: "rgba(255, 255, 255, 0.08)",
        backdropFilter: "blur(20px)",
        WebkitBackdropFilter: "blur(20px)",
        borderBottom: "1px solid rgba(255, 255, 255, 0.15)",
        padding: hasSearched ? "12px 16px" : "52px 16px 28px",
        transition: "padding 0.3s ease",
      }}>
        {!hasSearched && (
          <div style={{ textAlign: "center", marginBottom: "20px" }}>
            <h1 style={{
              fontFamily: "'Playfair Display', serif",
              fontSize: "clamp(2.2rem, 5vw, 3.4rem)",
              fontWeight: 700,
              color: "white",
              lineHeight: 1.1,
              marginBottom: "10px",
            }}>
              <span style={{ color: "#fbbf24" }}>✨</span> Haircare Advisor <span style={{ color: "#38bdf8" }}>✨</span>
            </h1>
            <p style={{
              fontFamily: "'DM Sans', sans-serif",
              fontSize: "1rem",
              color: "rgba(255,255,255,0.8)",
              fontWeight: 300,
            }}>
              Recommendations from real people — powered by Reddit &amp; AI
            </p>
          </div>
        )}
        <div style={{ maxWidth: "680px", margin: "0 auto" }}>
          <SearchBar onSearch={handleSearch} isLoading={isLoading} />
        </div>
      </div>
      <div style={{ maxWidth: "72rem", margin: "0 auto", padding: "2.5rem 1rem" }}>
        <div style={{ display: "flex", flexDirection: "column", gap: "2rem" }}>
          {isLoading && <LoadingState />}
          {error && !isLoading && (
            <div className="card-glass" style={{ padding: "24px", textAlign: "center" }}>
              <p style={{ color: "white" }}>⚠️ {error}</p>
            </div>
          )}
          {message && !isLoading && products.length === 0 && (
            <div className="card-glass" style={{ padding: "24px", textAlign: "center" }}>
              <p style={{ color: "rgba(255,255,255,0.85)" }}>✨ {message}</p>
            </div>
          )}
          {products.length > 0 && !isLoading && (
            <p style={{ textAlign: "center", fontSize: "0.85rem", color: "rgba(255,255,255,0.7)" }}>
              Found <strong>{products.length}</strong> products for "{lastQuery}"
            </p>
          )}
          {products.length > 0 && !isLoading && (
            <div style={{
              display: "grid",
              gridTemplateColumns: "repeat(2, minmax(0, 1fr))",
              gap: "24px",
            }}>
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
