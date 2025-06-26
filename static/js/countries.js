document.addEventListener("DOMContentLoaded", () => {
  const ctx = document.getElementById("countryChart").getContext("2d");

  new Chart(ctx, {
    type: 'bar',
    data: {
      labels: ["USA", "India", "UK", "Germany", "Canada"],
      datasets: [{
        label: "Users",
        data: [1200, 950, 780, 640, 430],
        backgroundColor: ["#6366f1", "#10b981", "#f59e0b", "#3b82f6", "#ef4444"],
        borderRadius: 8
      }]
    },
    options: {
      responsive: true,
      plugins: {
        legend: {
          display: false
        }
      },
      scales: {
        x: {
          ticks: {
            color: "#ffffff"  // ⬅ Change this to any color you like
          },
          grid: {
            color: "#444" // Optional: grid line color
          }
        },
        y: {
          beginAtZero: true,
          ticks: {
            color: "#ffffff"  // ⬅ Change this to match your theme
          },
          grid: {
            color: "#444"
          }
        }
      }
    }
  });
});
