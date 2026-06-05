export default function ProductCard({ product }) {
  const { name, brand, reddit_sentiment, controversial, pros, cons, best_for, price_range, verdict } = product;

  return (
    <div className="card-glass" style={{ padding: "24px", display: "flex", flexDirection: "column", gap: "14px" }}>

      {/* badges */}
      <div style={{ display: "flex", flexWrap: "wrap", gap: "6px" }}>
        <span className={reddit_sentiment === "positive" ? "badge-rec" : "badge-avoid"}>
          {reddit_sentiment === "positive" ? "✦ Reddit Recommended" : "✦ Reddit Warns Against"}
        </span>
        {controversial && (
          <span className="badge-controversial">✦ Mixed Reviews</span>
        )}
      </div>

      {/* name + brand */}
      <div>
        <h2 style={{
          fontFamily: "'Playfair Display', serif",
          fontSize: "1.25rem",
          fontWeight: 700,
          color: "white",
          lineHeight: 1.2,
          marginBottom: "4px",
        }}>
          {name}
        </h2>
        <p style={{ fontSize: "0.8rem", color: "rgba(255,255,255,0.6)" }}>{brand}</p>
      </div>

      <hr className="glass-divider" />

      {/* best for + price */}
      <div style={{ display: "flex", justifyContent: "space-between", gap: "12px", flexWrap: "wrap" }}>
        <div>
          <div className="section-label">Best For</div>
          <p style={{ fontSize: "0.85rem", color: "rgba(255,255,255,0.85)" }}>{best_for}</p>
        </div>
        <div style={{ textAlign: "right" }}>
          <div className="section-label">Price</div>
          <p style={{ fontSize: "0.95rem", fontWeight: 600, color: "white" }}>{price_range}</p>
        </div>
      </div>

      {/* pros */}
      {pros && pros.length > 0 && (
        <div>
          <div className="section-label">What People Love</div>
          <ul style={{ listStyle: "none", display: "flex", flexDirection: "column", gap: "5px" }}>
            {pros.map((pro, i) => (
              <li key={i} style={{ display: "flex", gap: "8px", fontSize: "0.85rem", color: "rgba(255,255,255,0.85)", alignItems: "flex-start" }}>
                <span style={{ flexShrink: 0, marginTop: "1px" }}>🌸</span>
                <span>{pro}</span>
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* cons */}
      {cons && cons.length > 0 && (
        <div>
          <div className="section-label">Watch Out For</div>
          <ul style={{ listStyle: "none", display: "flex", flexDirection: "column", gap: "5px" }}>
            {cons.map((con, i) => (
              <li key={i} style={{ display: "flex", gap: "8px", fontSize: "0.85rem", color: "rgba(255,255,255,0.85)", alignItems: "flex-start" }}>
                <span style={{ flexShrink: 0, marginTop: "1px" }}>💧</span>
                <span>{con}</span>
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* verdict */}
      {verdict && (
        <div className="verdict-block" style={{ marginTop: "auto" }}>
          <div className="section-label" style={{ color: "rgba(224,242,254,0.8)" }}>✦ Verdict</div>
          <p style={{ fontSize: "0.85rem", fontStyle: "italic", color: "white", lineHeight: 1.6 }}>
            "{verdict}"
          </p>
        </div>
      )}

    </div>
  );
}