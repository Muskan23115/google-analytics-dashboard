document.addEventListener("DOMContentLoaded", () => {
  console.log("✅ welcome.js loaded and DOM ready");

  const updateRealtime = () => {
    fetch("/api/realtime-users")
      .then(res => res.json())
      .then(data => {
        console.log("🎯 realtime (30min):", data);
        document.getElementById("activeUsersLast30Min").textContent = data.activeUsersLast30Min;
      })
      .catch(err => console.error("🛑 realtime error:", err));
  };

  const updateWelcomeMetrics = () => {
    fetch("/api/welcome-metrics")
      .then(res => res.json())
      .then(data => {
        console.log("📈 welcome-metrics:", data);
        document.getElementById("newUsers").textContent = data.newUsers;
        document.getElementById("avgSession").textContent = data.avgSession;
      })
      .catch(err => console.error("🛑 welcome-metrics error:", err));
  };

  updateRealtime();
  updateWelcomeMetrics();
  setInterval(updateRealtime, 15000);
});
