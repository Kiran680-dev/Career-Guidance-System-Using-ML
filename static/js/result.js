document.addEventListener("DOMContentLoaded", function () {
  const confidence = parseFloat(confidenceValue) || 0;
  const spinner = document.getElementById("spinner");

  if (spinner) {
    spinner.style.display = "none";
  }


  const centerTextPlugin = {
    id: "centerText",

    beforeDraw(chart) {
      const width = chart.width;
      const height = chart.height;
      const ctx = chart.ctx;
      ctx.restore();
      const fontSize = (height / 6).toFixed(2);
      ctx.font = "bold " + fontSize + "px Poppins";
      ctx.textBaseline = "middle";
      ctx.fillStyle = "#6c63ff";
      const text = confidence + "%";
      const textX = Math.round((width - ctx.measureText(text).width) / 2);
      const textY = height / 2;
      ctx.fillText(text, textX, textY);
      ctx.save();
    },
  };

  const ctx = document.getElementById("confidenceChart").getContext("2d");
  new Chart(ctx, {
    type: "doughnut",

    data: {
      labels: ["Confidence", "Others"],

      datasets: [
        {
          data: [confidence, 100 - confidence],
          backgroundColor: ["#6c63ff", "#d32f2f"],
          borderWidth: 0,
        },
      ],
    },

    options: {
      cutout: "75%",

      animation: {
        duration: 1100, // animation fast
      },

      plugins: {
        legend: {
          position: "bottom",
        },
      },
    },

    plugins: [centerTextPlugin],
  });
});
