// static/js/countries.js
document.addEventListener('DOMContentLoaded', async () => {
  try {
    const response = await fetch('/analytics/countries');
    const result = await response.json();

    const ctx = document.getElementById('countriesChart').getContext('2d');
    new Chart(ctx, {
      type: 'pie',
      data: {
        labels: result.labels,
        datasets: [{
          label: 'Users by Country',
          data: result.data,
          backgroundColor: [
            '#00bcd4', '#3f51b5', '#8bc34a',
            '#ff9800', '#9c27b0', '#e91e63', '#ff5722'
          ]
        }]
      },
      options: {
        responsive: true
      }
    });
  } catch (err) {
    console.error('Error fetching country data:', err);
  }
});
