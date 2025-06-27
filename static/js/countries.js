document.addEventListener("DOMContentLoaded", async () => {
  const ctx = document.getElementById("countriesChart").getContext("2d");

  let labels = [], data = [], tableData = [];

  try {
    const res = await fetch("/api/countries");
    const json = await res.json();
    labels = json.labels;
    data = json.data;
    tableData = json.table;
  } catch (err) {
    console.error("Error fetching countries data:", err);
    labels = ["India", "USA", "UK"];
    data = [40, 30, 20];
    tableData = [];
  }

  const isDark = document.body.classList.contains('dark-mode');
  const textColor = isDark ? '#cbd5e1' : '#1e293b';

  new Chart(ctx, {
    type: 'bar',
    data: {
      labels,
      datasets: [{
        label: 'Active Users by Country',
        data,
        backgroundColor: '#6366f1',
        borderRadius: 6
      }]
    },
    options: {
      responsive: true,
      plugins: { legend: { display: false } },
      scales: {
        x: { ticks: { color: textColor } },
        y: { beginAtZero: true, ticks: { color: textColor } }
      }
    }
  });

  // ✅ Populate table
  const tbody = document.querySelector(".country-table tbody");
  tbody.innerHTML = "";
  tableData.forEach(row => {
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td>${row.country}</td>
      <td>${row.users}</td>
      <td>${row.sessions}</td>
      <td>${row.bounceRate}</td>
      <td>${row.avgSession}</td>
    `;
    tbody.appendChild(tr);
  });
});
