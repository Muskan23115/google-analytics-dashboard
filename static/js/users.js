document.addEventListener("DOMContentLoaded", async () => {
  const response = await fetch('/api/users');
  const data = await response.json();

  const ctx = document.getElementById('userChart').getContext('2d');
  new Chart(ctx, {
    type: 'line',
    data: {
      labels: data.labels,
      datasets: [{
        label: 'Users',
        data: data.data,
        backgroundColor: 'rgba(0, 188, 212, 0.2)',
        borderColor: 'rgba(0, 188, 212, 1)',
        borderWidth: 2,
        fill: true,
        tension: 0.4
      }]
    },
    options: {
      responsive: true,
      scales: {
        y: {
          beginAtZero: true
        }
      }
    }
  });
});
