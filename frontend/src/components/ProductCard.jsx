// ProductCard.jsx
// ─────────────────────────────────────────────────────────────────────────────
// Displays a single product's research summary as a styled card.
//
// Plain explanation:
//   This component receives one product summary object and renders it
//   as a visual card with the product name, sentiment badge, pros, cons,
//   best-for, price, and verdict. Each piece of data maps to a specific
//   section of the card.
//
// Analogy:
//   Think of this as a product report card. Each card is one student
//   (product) with their grades (pros/cons), a teacher's note (verdict),
//   and a gold star or warning sticker (sentiment badge) on the front.
// ─────────────────────────────────────────────────────────────────────────────

export default function ProductCard({ product }) {
  // destructure all the fields from the product summary object
  const {
    name,
    brand,
    reddit_sentiment,
    controversial,
    pros,
    cons,
    best_for,
    price_range,
    verdict,
  } = product;

  return (
    <div className="card-dreamy p-6 flex flex-col gap-4">

      {/* ── Card header — name, brand, badges ───────────────────────────── */}
      <div className="flex flex-col gap-2">

        {/* badge row */}
        <div className="flex flex-wrap gap-2">
          {/* sentiment badge — recommended or avoid */}
          <span className={reddit_sentiment === "positive" ? "badge-recommended" : "badge-avoid"}>
            {reddit_sentiment === "positive" ? "✅ Reddit Recommended" : "⚠️ Reddit Warns Against"}
          </span>

          {/* controversial badge — shown only when mixed reviews exist */}
          {controversial && (
            <span className="badge-controversial">⚡ Mixed Reviews</span>
          )}
        </div>

        {/* product name */}
        <h2 className="text-xl font-bold" style={{ color: "var(--text-primary)" }}>
          {name}
        </h2>

        {/* brand name */}
        <p className="text-sm font-medium" style={{ color: "var(--text-secondary)" }}>
          {brand}
        </p>

      </div>

      {/* ── Divider ─────────────────────────────────────────────────────── */}
      <div
        className="h-px w-full"
        style={{ background: "var(--gradient-dreamy)" }}
      />

      {/* ── Best for + Price row ─────────────────────────────────────────── */}
      <div className="flex flex-wrap gap-4">

        <div className="flex flex-col gap-1">
          <span className="text-xs font-semibold uppercase tracking-wide"
            style={{ color: "var(--text-muted)" }}>
            Best For
          </span>
          <span className="text-sm" style={{ color: "var(--text-primary)" }}>
            {best_for}
          </span>
        </div>

        <div className="flex flex-col gap-1 ml-auto text-right">
          <span className="text-xs font-semibold uppercase tracking-wide"
            style={{ color: "var(--text-muted)" }}>
            Price Range
          </span>
          <span className="text-sm font-semibold" style={{ color: "var(--text-primary)" }}>
            {price_range}
          </span>
        </div>

      </div>

      {/* ── Pros ────────────────────────────────────────────────────────── */}
      {pros && pros.length > 0 && (
        <div className="flex flex-col gap-2">
          <span className="text-xs font-semibold uppercase tracking-wide"
            style={{ color: "var(--text-muted)" }}>
            What People Love
          </span>
          <ul className="flex flex-col gap-1">
            {pros.map((pro, i) => (
              <li key={i} className="flex gap-2 text-sm" style={{ color: "var(--text-primary)" }}>
                <span className="mt-0.5 shrink-0">🌸</span>
                <span>{pro}</span>
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* ── Cons ────────────────────────────────────────────────────────── */}
      {cons && cons.length > 0 && (
        <div className="flex flex-col gap-2">
          <span className="text-xs font-semibold uppercase tracking-wide"
            style={{ color: "var(--text-muted)" }}>
            Watch Out For
          </span>
          <ul className="flex flex-col gap-1">
            {cons.map((con, i) => (
              <li key={i} className="flex gap-2 text-sm" style={{ color: "var(--text-primary)" }}>
                <span className="mt-0.5 shrink-0">💧</span>
                <span>{con}</span>
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* ── Verdict ─────────────────────────────────────────────────────── */}
      {verdict && (
        <div
          className="rounded-xl p-4 mt-auto"
          style={{ background: "var(--gradient-dreamy)" }}
        >
          <span className="text-xs font-semibold uppercase tracking-wide block mb-1"
            style={{ color: "var(--text-muted)" }}>
            Verdict
          </span>
          <p className="text-sm italic" style={{ color: "var(--text-primary)" }}>
            "{verdict}"
          </p>
        </div>
      )}

    </div>
  );
}