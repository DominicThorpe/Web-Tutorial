function create_chart(rainfallMm) {
  const labels = Object.keys(rainfallMm);
  const ctx = document.getElementById("fieldChart");

  new Chart(ctx, {
    type: "bar",
    data: {
      labels,
      datasets: [
        {
          label: "Rainfall (mm/day)",
          data: Object.values(rainfallMm),
          yAxisID: "yRain",
          borderWidth: 1
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { position: "bottom" },
        tooltip: { mode: "index", intersect: false }
      },
      interaction: { mode: "index", intersect: false },
      scales: {
        yRain: {
          beginAtZero: true,
          title: { display: true, text: "Rainfall (mm)" }
        }
      }
    }
  });
}

function get_rainfall() {
  return new Promise((resolve, reject) => {
    const today = new Date().getDate();
    const fourteenDaysAgo = new Date();
    fourteenDaysAgo.setDate(today - 14);

    const url = `https://environment.data.gov.uk/flood-monitoring/id/stations/296705/readings?since=${fourteenDaysAgo.toISOString()}&_limit=2000`;
    try {
        const response = fetch(url)
          .then(response => {
            if (!response.ok) {
                  throw new Error(`Response status: ${response.status}`);
              }

              return response.json();
          })
          .then (result => {
            resolve(result.items)
          })
          .catch(error => {
            reject(error)
          })
    } catch (error) {
        console.error(error.message);
    }
  })
};

function process_rainfall(readings) {
  const grouped = {};
  for (const record of readings) {
    const day = record.dateTime.slice(0, 10); // "YYYY-MM-DD"
    if (!grouped[day]) {
      grouped[day] = [];
    }

    grouped[day].push(record);
  }

  const processed = {}
  for (const day in grouped) {
    processed[day] = grouped[day].reduce((acc, r) => acc + r.value, 0);
  }

  return processed
}

get_rainfall()
  .then(readings => create_chart(process_rainfall(readings)))
  .catch(err => console.error(err));
