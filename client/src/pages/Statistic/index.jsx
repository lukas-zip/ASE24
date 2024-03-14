import { useEffect, useState } from "react";
import "./index.less";
import OverallStatistics from "./components/OverallStatistics";
import CalendarForm from "./components/CalendarForm";
import { useSelector } from "react-redux";
import {
  getOverallSummary,
  getCategorySummary,
  getMonthlySummary,
  getCategorySummaryByDay,
  getCategorySummaryByMonth,
  getExpensesByMonth,
} from "../../api/statistics.api";
import {
  getAllExpensesByMonth,
  getAllExpensesByDay,
} from "../../api/expense.api";
import { getAllExpenseCategory } from "../../api/setting.api";
import ReactEcharts from "echarts-for-react";
import { SimplePieChartOption } from "../../utils/SimplePieChartOption";
import { SimpleBarChartOption } from "../../utils/SimpleBarChartOption";
import SimpleLineChartOption from "../../utils/SimpleLineChartOption";
import { Space, Empty, Card, Tabs, DatePicker } from "antd";
import useUserTheme from "../../hooks/useUserTheme";
import dayjs from "dayjs";
import AllExpensesRecords from "./components/AllExpensesRecords";

export default function StatisticBoard() {
  const { user } = useSelector((state) => state.user);
  const theme = useUserTheme();
  const { TabPane } = Tabs;

  const [overallStats, setOverallStats] = useState();
  const [allCategories, setAllCategories] = useState([]);

  //overall tab
  const [categorySummary, setCategorySummary] = useState();
  const [categorySummaryYear, setCategorySummaryYear] = useState("2024");
  const [monthlySummary, setMonthlySummary] = useState();
  const [monthlySummaryYear, setMonthlySummaryYear] = useState("2024");

  //monthly tab
  const [monthlySelectedDate, setMonthlySelectedDate] = useState(dayjs());
  const [categorySummaryByMonth, setCategorySummaryByMonth] = useState();
  const [monthlyTotalSpent, setMonthlyTotalSpent] = useState(0);
  const [expensesByMonth, setExpensesByMonth] = useState();
  const [monthlyExpenses, setMonthlyExpenses] = useState([]);

  //daily tab
  const [dailySelectedDate, setDailySelectedDate] = useState(dayjs());
  const [categorySummaryByDay, setCategorySummaryByDay] = useState();
  const [dailyTotalSpent, setDailyTotalSpent] = useState(0);
  const [dailyExpenses, setDailyExpenses] = useState([]);

  const getOverall = async (userId) => {
    await getOverallSummary(userId, {
      year: dayjs().year(),
    }).then((res) => {
      if (res && res.status !== false) {
        setOverallStats(res);
      }
    });
  };

  const getCategory = async (userId) => {
    await getCategorySummary(userId, {
      year: parseInt(categorySummaryYear),
    }).then((res) => {
      if (res && res.status !== false) {
        setCategorySummary(
          Object.entries(res).map(([name, value]) => ({
            value,
            name,
          }))
        );
      }
    });
  };

  const getAllCategory = async () => {
    await getAllExpenseCategory(user.id).then((res) => {
      if (res && res.status !== false) {
        setAllCategories(res);
      }
    });
  };

  const getMonthly = async (userId) => {
    await getMonthlySummary(userId, {
      year: parseInt(monthlySummaryYear),
    }).then((res) => {
      if (res && res.status !== false) {
        setMonthlySummary(res);
      }
    });
  };

  const getMonthlyExpenses = async (userId) => {
    await getAllExpensesByMonth(userId, {
      date: monthlySelectedDate.format("DD-MM-YYYY"),
    }).then((res) => {
      if (res && res.status !== false) {
        setMonthlyExpenses(res);
      }
    });
  };

  const getDailyExpenses = async (userId) => {
    await getAllExpensesByDay(userId, {
      date: dailySelectedDate.format("DD-MM-YYYY"),
    }).then((res) => {
      if (res && res.status !== false) {
        setDailyExpenses(res);
      }
    });
  };

  const getCategoryByDay = async (userId) => {
    await getCategorySummaryByDay(userId, {
      date: dailySelectedDate.format("DD-MM-YYYY"),
    }).then((res) => {
      if (res && res.status !== false) {
        setCategorySummaryByDay(
          Object.entries(res).map(([name, value]) => ({
            value,
            name,
          }))
        );

        setDailyTotalSpent(
          Object.values(res).reduce((accumulator, value) => {
            return accumulator + value;
          }, 0)
        );
      }
    });
  };

  const getCategoryByMonth = async (userId) => {
    await getCategorySummaryByMonth(userId, {
      date: monthlySelectedDate.format("DD-MM-YYYY"),
    }).then((res) => {
      if (res && res.status !== false) {
        setCategorySummaryByMonth(
          Object.entries(res).map(([name, value]) => ({
            value,
            name,
          }))
        );

        setMonthlyTotalSpent(
          Object.values(res).reduce((accumulator, value) => {
            return accumulator + value;
          }, 0)
        );
      }
    });
  };

  const getByMonth = async (userId) => {
    await getExpensesByMonth(userId, {
      date: monthlySelectedDate.format("DD-MM-YYYY"),
    }).then((res) => {
      if (res && res.status !== false) {
        const resArray = Object.entries(res).map(([key, value]) => ({
          key,
          value,
        }));

        const newObj = resArray.map(({ key, value }) => ({
          [key.slice(0, 2)]: value,
        }));

        setExpensesByMonth(newObj);
      }
    });
  };

  const generateChartOptions = (title, categorySummaryData) => {
    const baseOptions = SimplePieChartOption(title, categorySummaryData);
    return {
      ...baseOptions,
      title: {
        ...baseOptions.title,
        left: "center",
      },
      legend: {
        left: "center",
        bottom: "20",
      },
      series: [
        {
          ...baseOptions.series[0],
          emphasis: {
            label: {
              ...baseOptions.series[0].label,
              show: false,
            },
          },
        },
      ],
    };
  };

  const generateLineChartOptions = (keys, value, title) => {
    const baseOptions = SimpleLineChartOption(keys, value, title);
    return {
      ...baseOptions,
      grid: {
        left: "3%",
        right: "4%",
        bottom: "3%",
        containLabel: true,
      },
    };
  };
  const getAllData = async () => {
    const userId = user.id;
    await getOverall(userId);
    await getCategory(userId);
    await getMonthly(userId);
    await getCategoryByDay(userId);
    await getCategoryByMonth(userId);
    await getByMonth(userId);
    await getAllCategory(userId);
    await getMonthlyExpenses(userId);
    await getDailyExpenses(userId);
  };

  useEffect(() => {
    getAllData();
  }, []);

  //overall
  useEffect(() => {
    getCategory(user.id);
  }, [categorySummaryYear]);

  useEffect(() => {
    getMonthly(user.id);
  }, [monthlySummaryYear]);

  //monthly
  const handleMonthlyDateSelection = (date) => {
    setMonthlySelectedDate(date);
  };

  useEffect(() => {
    //refetch
    getCategoryByMonth(user.id);
    getByMonth(user.id);
    getMonthlyExpenses(user.id);
  }, [monthlySelectedDate]);

  //daily
  const handleDailyDateSelection = (date) => {
    setDailySelectedDate(date);
  };

  useEffect(() => {
    //refetch
    getCategoryByDay(user.id);
    getDailyExpenses(user.id);
  }, [dailySelectedDate]);

  const onPieChartChange = (_date, dateString) => {
    setCategorySummaryYear(dateString);
  };

  const onBarChartChange = (_date, dateString) => {
    setMonthlySummaryYear(dateString);
  };

  return (
    <div>
      <Space
        direction="vertical"
        size="small"
        style={{
          display: "flex",
        }}
      >
        <OverallStatistics overallStats={overallStats} />
        {/* charts */}
        <Tabs defaultActiveKey="1">
          <TabPane tab="Overall" key="1">
            <div
              style={{
                display: "flex",
                flexDirection: "column", // Set to column direction
                justifyContent: "space-between",
                gap: "2rem",
              }}
            >
              <Card
                style={{
                  width: "100%",
                  padding: "10px",
                  height: "100%",
                  borderRadius: 10,
                  ...(categorySummary
                    ? {}
                    : {
                        display: "flex",
                        alignItems: "center",
                        justifyContent: "center",
                      }),
                }}
              >
                <DatePicker
                  style={{ float: "right" }}
                  onChange={onPieChartChange}
                  defaultValue={dayjs()}
                  picker="year"
                />

                {categorySummary ? (
                  <ReactEcharts
                    style={{
                      marginTop: "3rem",
                    }}
                    option={generateChartOptions(
                      "Total Expense For Each Category",
                      categorySummary
                    )}
                    theme={theme}
                  />
                ) : (
                  <Empty
                    description={
                      "No category summary available, try creating an expense"
                    }
                  />
                )}
              </Card>
              <Card
                style={{
                  width: "100%",
                  padding: "10px",
                  height: "100%",
                  borderRadius: 10,
                  ...(monthlySummary
                    ? {}
                    : {
                        display: "flex",
                        alignItems: "center",
                        justifyContent: "center",
                      }),
                }}
              >
                <DatePicker
                  style={{ float: "right" }}
                  onChange={onBarChartChange}
                  defaultValue={dayjs()}
                  picker="year"
                />
                {monthlySummary ? (
                  <ReactEcharts
                    style={{
                      marginTop: "3rem",
                    }}
                    option={SimpleBarChartOption(
                      Object.keys(monthlySummary),
                      Object.values(monthlySummary),
                      "Monthly Expense"
                    )}
                    theme={theme}
                  />
                ) : (
                  <Empty description={"No data available to show"} />
                )}
              </Card>
            </div>
          </TabPane>
          <TabPane tab="Monthly" key="2">
            <div className="statistic-overview">
              <Card className="statistic-overview-left">
                <Card
                  title={`Total Spent (${monthlySelectedDate.format("MMM")})`}
                  bordered={true}
                  headStyle={{ padding: 10, fontSize: 18, fontWeight: "bold" }}
                  bodyStyle={{ fontSize: 24, fontWeight: "bold", padding: 20 }}
                  style={{
                    width: "100%",
                    marginBottom: 10,
                  }}
                >
                  {monthlyTotalSpent !== 0
                    ? `$${parseFloat(monthlyTotalSpent).toFixed(2)}`
                    : "--"}
                </Card>
                <CalendarForm
                  handleDateChange={handleMonthlyDateSelection}
                  mode="year"
                />
              </Card>
              <div
                style={{
                  width: "100%",
                  height: "100%",
                  borderRadius: 10,
                  gap: "1rem",
                  display: "flex",
                  flexDirection: "column",
                }}
              >
                <Card
                  style={{
                    width: "100%",
                    padding: "20px 10%",
                    height: "100%",
                    borderRadius: 10,
                    ...(categorySummaryByMonth
                      ? {}
                      : {
                          display: "flex",
                          alignItems: "center",
                          justifyContent: "center",
                        }),
                  }}
                >
                  {categorySummaryByMonth &&
                  categorySummaryByMonth.length > 0 ? (
                    <ReactEcharts
                      option={generateChartOptions(
                        "Category By Month",
                        categorySummaryByMonth
                      )}
                      theme={theme}
                    />
                  ) : (
                    <Empty
                      description={
                        "No category summary available, try creating an expense"
                      }
                    />
                  )}
                </Card>
                <Card
                  style={{
                    width: "100%",
                    padding: "20px 10%",
                    height: "100%",
                    borderRadius: 10,
                    ...(expensesByMonth
                      ? {}
                      : {
                          display: "flex",
                          alignItems: "center",
                          justifyContent: "center",
                        }),
                  }}
                >
                  {expensesByMonth ? (
                    <ReactEcharts
                      option={generateLineChartOptions(
                        expensesByMonth.flatMap((obj) => Object.keys(obj)),
                        expensesByMonth.flatMap((obj) => Object.values(obj)),
                        "Monthly Expense"
                      )}
                      theme={theme}
                    />
                  ) : (
                    <Empty description={"No data available to show"} />
                  )}
                </Card>
                <AllExpensesRecords
                  allExpenses={monthlyExpenses}
                  allCategories={allCategories}
                  getAllData={getAllData}
                />
              </div>
            </div>
          </TabPane>
          <TabPane tab="Daily" key="3">
            <div className="statistic-overview">
              <Card className="statistic-overview-left">
                <Card
                  title="Total Spent"
                  bordered={true}
                  headStyle={{ padding: 10, fontSize: 18, fontWeight: "bold" }}
                  bodyStyle={{ fontSize: 24, fontWeight: "bold", padding: 20 }}
                  style={{
                    width: "100%",
                    marginBottom: 10,
                  }}
                >
                  {dailyTotalSpent !== 0
                    ? `$${parseFloat(dailyTotalSpent).toFixed(2)}`
                    : "--"}
                </Card>
                <CalendarForm handleDateChange={handleDailyDateSelection} />
              </Card>
              <div
                style={{
                  width: "100%",
                  height: "100%",
                  borderRadius: 10,
                  gap: "1rem",
                  display: "flex",
                  flexDirection: "column",
                }}
              >
                <Card
                  style={{
                    width: "100%",
                    padding: "20px 10%",
                    height: "100%",
                    borderRadius: 10,
                    ...(categorySummaryByDay
                      ? {}
                      : {
                          display: "flex",
                          alignItems: "center",
                          justifyContent: "center",
                        }),
                  }}
                >
                  {categorySummaryByDay && categorySummaryByDay.length > 0 ? (
                    <ReactEcharts
                      option={generateChartOptions(
                        "Category By Day",
                        categorySummaryByDay
                      )}
                      theme={theme}
                    />
                  ) : (
                    <Empty
                      description={
                        "No category summary available, try creating an expense"
                      }
                    />
                  )}
                </Card>
                <AllExpensesRecords
                  allExpenses={dailyExpenses}
                  allCategories={allCategories}
                  getAllData={getAllData}
                />
              </div>
            </div>
          </TabPane>
        </Tabs>
      </Space>
    </div>
  );
}
