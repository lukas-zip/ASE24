import COLORS from "../constants/COLORS";

export const SimpleBarChartOption = (xArr, yArr, title) => {
  return {
      title: {
        text: title, // Main title text
        left: "center", // Position the title in the center
        textStyle: {
          color: COLORS.primary, // Title color
          fontWeight: "bold", // Make the title font bold
          fontSize: 24, // Set the font size for the title
        },
      },
    tooltip: {
      trigger: "axis",
      axisPointer: {
        type: "shadow",
      },
    },
    grid: {
      left: "3%",
      right: "4%",
      bottom: "3%",
      containLabel: true,
    },
    xAxis: [
      {
        type: "category",
        data: xArr,
        axisTick: {
          alignWithLabel: true,
        },
      },
    ],
    yAxis: [
      {
        type: "value",
      },
    ],
    series: [
      {
        name: "Direct",
        type: "bar",
        barWidth: "60%",
        data: yArr,
      },
    ],
  };
};