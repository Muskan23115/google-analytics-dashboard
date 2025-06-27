document.addEventListener("DOMContentLoaded", async () => {
  const ctx = document.getElementById("devicesChart").getContext("2d");

  let labels = [], data = [];
  try {
    const res = await fetch("/api/devices");
    const json = await res.json();
    labels = json.labels;
    data = json.data;
  } catch (err) {
    console.error("Error fetching device data:", err);
    labels = ['Mobile', 'Desktop', 'Tablet'];
    data = [68, 24, 8]; // fallback
  }

  const isDark = document.body.classList.contains('dark-mode');
  const textColor = isDark ? '#cbd5e1' : '#1e293b';

  new Chart(ctx, {
    type: 'pie',
    data: {
      labels,
      datasets: [{
        label: 'Device Distribution',
        data,
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

fetch("/api/device-metrics")
  .then(res => res.json())
  .then(data => {
    document.getElementById("mobilePercent").textContent = `${data.mobile || 0}%`;
    document.getElementById("desktopPercent").textContent = `${data.desktop || 0}%`;
    document.getElementById("tabletPercent").textContent = `${data.tablet || 0}%`;

    document.getElementById("mobileBar").style.width = `${data.mobile || 0}%`;
    document.getElementById("desktopBar").style.width = `${data.desktop || 0}%`;
    document.getElementById("tabletBar").style.width = `${data.tablet || 0}%`;
  })
  .catch(err => {
    console.error("Failed to fetch device stats:", err);
  });
