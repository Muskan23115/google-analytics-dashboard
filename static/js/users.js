document.addEventListener("DOMContentLoaded", async () => {
  const ctx = document.getElementById("usersChart").getContext("2d");

  let labels = [], data = [];
  try {
    const res = await fetch("/api/active-users");
    const json = await res.json();
    labels = json.labels;
    data = json.data;
  } catch (err) {
    console.error("Error fetching active users:", err);
    labels = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"];
    data = [120, 200, 180, 220, 250, 300, 280];  // fallback
  }

  new Chart(ctx, {
    type: 'line',
    data: {
      labels,
      datasets: [{
        label: "Active Users",
        data,
        fill: false,
        borderColor: "#efe8e8",
        tension: 0.4,
        pointBackgroundColor: "#6366f1"
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { display: false } },
      scales: {
        x: {
          ticks: { color: '#efe8e8' },
          grid: { display: false }
        },
        y: {
          beginAtZero: true,
          ticks: { color: '#efe8e8' },
          grid: { color: "#3b3b5e" }
        }
      }
    }
  });
});

fetch("/api/user-metrics")
  .then(res => res.json())
  .then(data => {
    document.getElementById("totalUsers").textContent = data.totalUsers;
    document.getElementById("bounceRate").textContent = data.bounceRate;
    document.getElementById("newUsers").textContent = data.newUsers;
    document.getElementById("avgTime").textContent = data.avgTime;
  })
  .catch(err => {
    console.error("Failed to fetch user metrics:", err);
  });
