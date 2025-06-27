document.addEventListener("DOMContentLoaded", () => {
  fetch("/api/welcome-metrics")
    .then(res => res.json())
    .then(data => {
      document.getElementById("usersToday").textContent = data.usersToday;
      document.getElementById("newUsers").textContent = data.newUsers;
      document.getElementById("avgSession").textContent = data.avgSession;
    })
    .catch(err => {
      console.error("Failed to load welcome stats:", err);
    });
});
