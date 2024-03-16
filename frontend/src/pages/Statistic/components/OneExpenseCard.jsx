import { useState } from "react";
import { formatDateToMalaysia } from "../../../utils/convertDate";
import {
  Card,
  Col,
  Modal,
  Row,
  Button,
  InputNumber,
  DatePicker,
  Form,
  Input,
  message,
  Select,
  Popconfirm,
} from "antd";
import { DeleteOutlined, EditOutlined } from "@ant-design/icons";
import dayjs from "dayjs";
import { deleteExpense, updateExpense } from "../../../api/expense.api";

const OneExpenseCard = ({ Title, expense, getAllData, allCategories }) => {
  const [editOpen, setEditOpen] = useState(false);
  const onFinish = async (values) => {
    const date = formatDateToMalaysia(new Date(values.expenseDate));
    const updatedExpense = {
      expense_id: expense.id,
      dateString: date,
      comments: values.comments,
      expense_val: values.expense_val,
      category_id: allCategories.find(
        (item) => item.category_name === values.category
      ).id,
      user_id: expense.user.id,
    };

    await updateExpense(updatedExpense).then((res) => {
      if (res && res.status !== false) {
        message.success("Expense updated successfully");
        setEditOpen(false);
        getAllData();
      }
    });
  };

  const handleDeleteExpense = async () => {
    await deleteExpense(expense.id).then((res) => {
      if (res && res?.status !== false) {
        if (Title === "Expense") {
          window.location.reload();
        }
        message.success("Expense deleted successfully");
        getAllData();
      }
    });
  };

  return (
    <Row key={expense}>
      <Col span={24}>
        <Card
          title={`${Title}: 「${expense ? expense?.comments : "--"}」`}
          bordered={true}
          hoverable={true}
          headStyle={{ padding: 10, fontSize: 18, fontWeight: "bold" }}
          bodyStyle={{ padding: 10 }}
          extra={
            <div style={{ display: "flex", gap: 10 }}>
              <Popconfirm
                title="Delete the Expense"
                description="Are you sure to delete this expense?"
                onConfirm={handleDeleteExpense}
                okText="Yes"
                cancelText="No"
              >
                <Button danger size="small">
                  <DeleteOutlined /> Delete
                </Button>
              </Popconfirm>
              <Button size="small" onClick={() => setEditOpen(true)}>
                <EditOutlined /> Update
              </Button>
            </div>
          }
        >
          <div style={{ display: "flex", alignItems: "baseline", gap: 10 }}>
            <div style={{ fontSize: 18 }}>Expense Amount:</div>
            <span style={{ fontSize: 24, fontWeight: "bold" }}>
              {expense
                ? `$${parseFloat(expense?.expense_val).toFixed(2)}`
                : "--"}
            </span>
          </div>
          <div style={{ fontSize: 18 }}>
            Category: {expense ? expense?.category.category_name : "--"}
          </div>
          {/* <div style={{ fontSize: 18 }}>
            Comment: {expense ? expense?.comments : "--"}
          </div> */}
          <div style={{ display: "flex", gap: 30, justifyContent: "end" }}>
            <div style={{ fontSize: 16 }}>
              Date:{" "}
              {expense
                ? expense?.expenseDate &&
                  formatDateToMalaysia(new Date(expense?.expenseDate))
                : "--"}
            </div>
          </div>
        </Card>
      </Col>
      <Modal
        open={editOpen}
        onCancel={() => setEditOpen(false)}
        onOk={() => setEditOpen(false)}
        title={"Edit Expense"}
        footer={null}
      >
        <Form
          onFinish={onFinish}
          labelCol={{ span: 8 }}
          wrapperCol={{ span: 16 }}
          style={{ maxWidth: 600 }}
          initialValues={{
            ...expense,
            expenseDate: expense?.expenseDate
              ? dayjs(expense?.expenseDate, "YYYY-MM-DD")
              : null,
            category: expense?.category.category_name,
          }}
          autoComplete="off"
        >
          <Form.Item
            label="Comments"
            name="comments"
            rules={[{ required: true, message: "Please input expense name!" }]}
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
            name={"expenseDate"}
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
              Update
            </Button>
          </Form.Item>
        </Form>
      </Modal>
    </Row>
  );
};

export default OneExpenseCard;
