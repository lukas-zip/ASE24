import { useState } from "react";
import { formatDateToMalaysia } from "../../../utils/convertDate";
import { useSelector } from "react-redux";
import {
  Col,
  Modal,
  Row,
  Space,
  Button,
  InputNumber,
  DatePicker,
  Form,
  Input,
  message,
  Card,
  Select,
} from "antd";
import {
  DownOutlined,
  FileOutlined,
  UpOutlined,
  UploadOutlined,
} from "@ant-design/icons";
import COLORS from "../../../constants/COLORS";
import OneExpenseCard from "./OneExpenseCard";
import { createExpense } from "../../../api/expense.api";

const AllExpensesRecords = ({ getAllData, allExpenses, allCategories }) => {
  const { user } = useSelector((state) => state.user);
  const [collapsed, setCollapsed] = useState(false);
  const [createOpen, setCreateOpen] = useState(false);

  const onFinishCreate = async (values) => {
    const date = formatDateToMalaysia(new Date(values.expense_date));

    const newExpense = {
      comments: values.comments,
      expense_val: values.expense_val,
      dateString: date,
      user_id: user.id,
      category_id: allCategories.find(
        (item) => item.category_name === values.category
      ).id,
    };

    await createExpense(newExpense).then((res) => {
      if (res && res.status !== false) {
        message.success("Expense create successfully");
        setCreateOpen(false);
        getAllData();
      } else {
        console.error(res);
      }
    });
  };

  return (
    <>
      <Row>
        <Col span={24}>
          <Card
            bordered={true}
            bodyStyle={{
              width: "100%",
              padding: 0,
              borderRadius: 10,
            }}
          >
            <div
              style={{
                width: "100%",
                display: "flex",
                padding: "10px 10px 15px",
                borderBottom: "1px solid #F0F0F0",
                justifyContent: "space-between",
                alignItems: "center",
              }}
            >
              <div style={{ fontWeight: "bold", fontSize: 18 }}>
                <FileOutlined /> Total {allExpenses.length} Expenses{" "}
                {collapsed ? (
                  <span
                    className="hoverButton"
                    style={{
                      fontSize: 14,
                      fontWeight: "normal",
                      marginLeft: 8,
                    }}
                    onClick={() => setCollapsed(!collapsed)}
                  >
                    Collapsed <UpOutlined />
                  </span>
                ) : (
                  <span
                    className="hoverButton"
                    style={{
                      fontSize: 14,
                      fontWeight: "normal",
                      marginLeft: 8,
                    }}
                    onClick={() => setCollapsed(!collapsed)}
                  >
                    Expand <DownOutlined />
                  </span>
                )}
              </div>
              <div
                className="hoverButton"
                onClick={() => setCreateOpen(true)}
                style={{
                  userSelect: "none",
                  borderRadius: 10,
                  padding: 10,
                  backgroundColor: COLORS.primary,
                  color: "white",
                }}
              >
                Create Expense <UploadOutlined />
              </div>
            </div>
            {!collapsed && (
              <div style={{ maxHeight: 300, overflowY: "auto", padding: 10 }}>
                <Space
                  direction="vertical"
                  size="small"
                  style={{
                    display: "flex",
                  }}
                >
                  {allExpenses.map((item, index) => (
                    <OneExpenseCard
                      Title={"Expense"}
                      allCategories={allCategories}
                      getAllData={getAllData}
                      expense={item}
                      key={index}
                    />
                  ))}
                </Space>
              </div>
            )}
          </Card>
        </Col>
      </Row>
      <Modal
        open={createOpen}
        onCancel={() => setCreateOpen(false)}
        onOk={() => setCreateOpen(false)}
        title={"Create Expense"}
        footer={null}
      >
        <Form
          onFinish={onFinishCreate}
          labelCol={{ span: 8 }}
          wrapperCol={{ span: 16 }}
          style={{ maxWidth: 600 }}
          autoComplete="off"
        >
          <Form.Item
            label="Comments"
            name="comments"
            rules={[
              { required: true, message: "Please input expense comment!" },
            ]}
          >
            <Input />
          </Form.Item>
          <Form.Item
            label="Category"
            name={"category"}
            rules={[{ required: true, message: "Please select a category!" }]}
          >
            <Select>
              {allCategories.map((item, index) => (
                <Select.Option value={item.category_name} key={index}>
                  {item.category_name}
                </Select.Option>
              ))}
            </Select>
          </Form.Item>
          <Form.Item
            label="Date"
            name={"expense_date"}
            rules={[{ required: true, message: "Please input date!" }]}
          >
            <DatePicker format={"DD/MM/YYYY"} />
          </Form.Item>
          <Form.Item
            label="Amount"
            name={"expense_val"}
            rules={[{ required: true, message: "Please input amount!" }]}
          >
            <InputNumber step={0.01} min={0} />
          </Form.Item>
          <Form.Item wrapperCol={{ offset: 8, span: 16 }}>
            <Button type="primary" htmlType="submit">
              Create
            </Button>
          </Form.Item>
        </Form>
      </Modal>
    </>
  );
};

export default AllExpensesRecords;
