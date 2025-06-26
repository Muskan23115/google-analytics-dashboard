document.addEventListener("DOMContentLoaded", () => {
  const ctx = document.getElementById("usersChart").getContext("2d");

  const chart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
      datasets: [{
        label: "Active Users",
        data: [120, 200, 180, 220, 250, 300, 280],
        fill: false,
        borderColor: "#efe8e8",
        tension: 0.4,
        pointBackgroundColor: "#6366f1"
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          display: false
        }
      },
      scales: {
        x: {
          ticks: {
            color: '#efe8e8'
          },
          grid: {
            display: false
          }
        },
        y: {
          beginAtZero: true,
          ticks: {
            color: '#efe8e8' 
          },
          grid: {
            color: "#3b3b5e"
          }
        }
      }
    }
  });
});
