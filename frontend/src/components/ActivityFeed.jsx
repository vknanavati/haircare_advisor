export default function ActivityFeed({ activities }) {
  if (activities.length === 0) return null;

  return (
    <div style={{
      position: "fixed",
      bottom: "20px",
      right: "20px",
      width: "300px",
      backgroundColor: "rgba(0, 0, 0, 0.75)",
      backdropFilter: "blur(20px)",
      WebkitBackdropFilter: "blur(20px)",
      borderRadius: "12px",
      border: "1px solid rgba(255, 255, 255, 0.15)",
      padding: "16px",
      zIndex: 1000,
      boxShadow: "0 8px 32px rgba(0, 0, 0, 0.4)",
    }}>
      <div style={{
        fontSize: "0.7rem",
        fontWeight: 600,
        color: "rgba(255,255,255,0.6)",
        marginBottom: "12px",
        textTransform: "uppercase",
        letterSpacing: "0.08em",
      }}>
        Pipeline Status
      </div>

      <div style={{ display: "flex", flexDirection: "column", gap: "8px" }}>
        {activities.map((activity, index) => (
          <div key={index} style={{ display: "flex", alignItems: "flex-start", gap: "10px" }}>
            <div style={{ minWidth: "16px", marginTop: "2px", fontSize: "0.8rem" }}>
              {activity.status === "in_progress" && <span style={{ color: "#38bdf8" }}>●</span>}
              {activity.status === "completed" && <span style={{ color: "#4ade80" }}>✓</span>}
              {activity.status === "failed" && <span style={{ color: "#f87171" }}>✗</span>}
            </div>
            <div>
              <div style={{ fontSize: "0.8rem", fontWeight: 500, color: "white" }}>{activity.step}</div>
              <div style={{ fontSize: "0.72rem", color: "rgba(255,255,255,0.5)", marginTop: "1px" }}>{activity.detail}</div>
            </div>
          </div>
        ))}
      </div>

      <style>{`
        @keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.3; } }
      `}</style>
    </div>
  );
}
