document.addEventListener("DOMContentLoaded", () => {
  const ctx = document.getElementById("devicesChart").getContext("2d");

  const isDark = document.body.classList.contains('dark-mode');
  const textColor = isDark ? '#cbd5e1' : '#1e293b';

  new Chart(ctx, {
    type: 'pie',
    data: {
      labels: ['Mobile', 'Desktop', 'Tablet'],
      datasets: [{
        label: 'Device Distribution',
        data: [68, 24, 8],
        backgroundColor: ['#3b82f6', '#8b5cf6', '#10b981'],
        borderWidth: 1
      }]
    },
    options: {
      responsive: true,
      plugins: {
        legend: {
          labels: {
            color: textColor
          }
        }
      }
    }
  });
});
