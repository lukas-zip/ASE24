import { useEffect, useState } from "react";
import { Space, Empty, Card, DatePicker } from "antd";
import AllExpensesRecords from "./components/AllExpensesRecords";
import { useSelector } from "react-redux";
import OverallStatistics from "./components/OverallStatistics";
import { SimpleBarChartOption } from "../../utils/SimpleBarChartOption";
import ReactEcharts from "echarts-for-react";
import dayjs from "dayjs";
import useUserTheme from "../../hooks/useUserTheme";

function Home() {
  const { user } = useSelector((state) => state.user);
  const theme = useUserTheme();

  return (
    <Space
      direction="vertical"
      size="small"
      style={{
        display: "flex",
      }}
    >
      nihao
    </Space>
  );
}

export default Home;
