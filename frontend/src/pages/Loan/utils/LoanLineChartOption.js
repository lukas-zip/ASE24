import * as echarts from "echarts";
import COLORS from "../../../constants/COLORS";

const colors = [COLORS.red, COLORS.green, COLORS.primary]; // Add more colors if needed

const LoanLineChartOption = (xArr, yArrs, titles, title, boundaryColor) => {
  const series = yArrs.map((yArr, index) => {
    let yarr = yArr.map((element) => element || 0);
    return {
      data: yarr,
      type: "line",
      name: titles[index],
      color: colors[index], // Set the color of the line
      areaStyle: {
        normal: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 0.7, [
            {
              offset: 0,
              color: colors[index], // 0% 处的颜色
            },
            {
              offset: 1,
              color: boundaryColor ? boundaryColor : "#fff", // 100% 处的颜色
            },
          ]), //背景渐变色
        },
      },
      smooth: true,
    };
  });

  const selectedLegends = titles.reduce((acc, title, index) => {
    acc[title] = index < 2; // Only select the first two legends
    return acc;
  }, {});

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
        type: "cross",
        label: {
          backgroundColor: COLORS.primary,
        },
      },
    },
    legend: {
      data: titles,
      left: "center",
      bottom: "25",
      selected: selectedLegends,
    },
    toolbox: {
      feature: {
        saveAsImage: {
          type: "png", // 设置保存图片的类型，例如 'png', 'jpeg'
          name: titles.join(" / "), // 设置保存的图片名称
        },
      },
    },
    xAxis: {
      type: "category",
      data: xArr,
      show: true,
    },
    yAxis: {
      type: "value",
      show: true,
      splitLine: {
        show: true, // Do not show the split lines
      },
    },
    grid: {
      top: "50", // Give more room at the top
      right: "50",
      bottom: "50", // Provide space for rotated labels
      left: "8%",
      containLabel: true,
    },
    series: series,
    backgroundColor: "",
  };
};
export default LoanLineChartOption;
