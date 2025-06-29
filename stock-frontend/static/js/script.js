document.addEventListener("DOMContentLoaded", async function () {
    const response = await fetch("/api/aapl-data");
    const data = await response.json();
  
    const dates = data.map(item => item.date);
    const prices = data.map(item => item.close);
  
    new Chart(document.getElementById("stockChart"), {
      type: "line",
      data: {
        labels: dates,
        datasets: [{
          label: "AAPL Closing Price",
          data: prices,
          fill: false,
          borderColor: "rgb(75, 192, 192)",
          tension: 0.1
        }]
      },
      options: {
        responsive: true,
        scales: {
          x: { display: true, title: { display: true, text: "Date" } },
          y: { display: true, title: { display: true, text: "Price (USD)" } }
        }
      }
    });
  });
  