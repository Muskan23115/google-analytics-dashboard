// static/js/devices.js
document.addEventListener('DOMContentLoaded', async () => {
  try {
    const response = await fetch('/analytics/devices');
    const result = await response.json();

    const ctx = document.getElementById('devicesChart').getContext('2d');
    new Chart(ctx, {
      type: 'bar', // Change to 'pie' if you prefer
      data: {
        labels: result.labels,
        datasets: [{
          label: 'Users by Device',
          data: result.data,
          backgroundColor: ['#00bcd4', '#3f51b5', '#8bc34a'],
          borderWidth: 1
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
  } catch (err) {
    console.error("Error fetching device data:", err);
  }
});
