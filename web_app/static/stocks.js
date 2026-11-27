const data = JSON.parse(document.getElementById("price-data").textContent);
const canvas = document.getElementById("price-chart");
const currency = canvas.dataset.currency;
const price = new Intl.NumberFormat("en-US", currency
  ? { style: "currency", currency }
  : { minimumFractionDigits: 2, maximumFractionDigits: 2 });

new Chart(canvas, {
  type: "line",
  data: {
    labels: data.map((point) => point.date),
    datasets: [{
      label: "Price",
      data: data.map((point) => point.close),
      borderColor: "#14695d",
      backgroundColor: "rgba(20, 105, 93, 0.12)",
      fill: true,
      pointRadius: 0,
      pointHoverRadius: 5,
      borderWidth: 2,
    }],
  },
  options: {
    maintainAspectRatio: false,
    interaction: { mode: "index", intersect: false },
    plugins: {
      legend: { display: false },
      tooltip: { callbacks: { label: (item) => price.format(item.parsed.y) } },
    },
    scales: {
      x: { grid: { display: false }, ticks: { maxTicksLimit: 6, maxRotation: 0 } },
      y: { ticks: { callback: (value) => price.format(value) } },
    },
  },
});
