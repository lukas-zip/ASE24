import { Card, Col, Row } from "antd";

const OverallStatistics = ({ overallStats }) => {
  return (
    <Row gutter={[10, 10]}>
      <Col span={8}>
        <Card
          title="Overall Spent"
          bordered={false}
          hoverable={true}
          headStyle={{ padding: 10, fontSize: 18, fontWeight: "bold" }}
          bodyStyle={{ fontSize: 24, fontWeight: "bold", padding: 20 }}
        >
          {overallStats
            ? `$${parseFloat(overallStats.overallSpent).toFixed(2)}`
            : "--"}
        </Card>
      </Col>
      <Col span={8}>
        <Card
          title="This Year"
          bordered={false}
          hoverable={true}
          headStyle={{ padding: 10, fontSize: 18, fontWeight: "bold" }}
          bodyStyle={{ fontSize: 24, fontWeight: "bold", padding: 20 }}
        >
          {overallStats
            ? `$${parseFloat(overallStats.yearlySpent).toFixed(2)}`
            : "--"}
        </Card>
      </Col>
      <Col span={8}>
        <Card
          title="This Month"
          bordered={false}
          hoverable={true}
          headStyle={{ padding: 10, fontSize: 18, fontWeight: "bold" }}
          bodyStyle={{ fontSize: 24, fontWeight: "bold", padding: 20 }}
        >
          {overallStats
            ? `$${parseFloat(overallStats.monthlySpent).toFixed(2)}`
            : "--"}
        </Card>
      </Col>

      <Col span={8}>
        <Card
          title="This Week"
          bordered={false}
          hoverable={true}
          headStyle={{ padding: 10, fontSize: 18, fontWeight: "bold" }}
          bodyStyle={{ fontSize: 24, fontWeight: "bold", padding: 20 }}
        >
          {overallStats
            ? `$${parseFloat(overallStats.weeklySpent).toFixed(2)}`
            : "--"}
        </Card>
      </Col>
      <Col span={8}>
        <Card
          title="Today"
          bordered={false}
          hoverable={true}
          headStyle={{ padding: 10, fontSize: 18, fontWeight: "bold" }}
          bodyStyle={{ fontSize: 24, fontWeight: "bold", padding: 20 }}
        >
          {overallStats
            ? `$${parseFloat(overallStats.todaySpent).toFixed(2)}`
            : "--"}
        </Card>
      </Col>
      <Col span={8}>
        <Card
          title="Most Spent On"
          bordered={false}
          hoverable={true}
          headStyle={{ padding: 10, fontSize: 18, fontWeight: "bold" }}
          bodyStyle={{ fontSize: 24, fontWeight: "bold", padding: 20 }}
        >
          {overallStats ? overallStats?.mostSpentOn : "--"}
        </Card>
      </Col>
    </Row>
  );
};

export default OverallStatistics;
