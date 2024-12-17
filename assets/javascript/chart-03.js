import ApexCharts from "apexcharts";

// ===== chartThree
const chart03 = () => {
  const chartThreeOptions = {
    series: [85, 14, 45, 12],
    chart: {
      type: "donut",
      width: 380,
    },
    colors: ["#3C50E0", "#6577F3", "#8FD0EF", "#0FADCF"],
    labels: ["Desktop", "Tablet", "Mobile", "Unknown"],
    legend: {
      show: false,
      position: "bottom",
    },

    plotOptions: {
      pie: {
        donut: {
          size: "55%",
          background: "transparent",
        },
      },
    },

    dataLabels: {
      enabled: false,
    },
    responsive: [
      {
        breakpoint: 640,
        options: {
          chart: {
            width: 200,
          },
        },
      },
    ],
  };

  const chartSelector = document.querySelectorAll("#chartThree");

  if (chartSelector.length) {
    const chartThree = new ApexCharts(
      document.querySelector("#chartThree"),
      chartThreeOptions
    );
    chartThree.render();
  }
};

export default chart03;
