import React, { useState } from "react";
import { useSelector } from "react-redux";
import { deleteLoan, updateLoan, getLoanTransactions, recordPayment, recordReception, editLoanTransaction, deleteLoanTransaction } from "../../../api/loan.api";
import { formatDateToMalaysia } from "../../../utils/convertDate";
import { Card, Col, Row, Button, InputNumber, DatePicker, Form, Input, message, Popconfirm, Modal, Select, Tag, List } from "antd";
import { DeleteOutlined, EditOutlined, ArrowRightOutlined, ArrowLeftOutlined, InfoCircleOutlined, DollarCircleOutlined } from "@ant-design/icons";
import dayjs from "dayjs";
const { TextArea } = Input;
import LoanDetailModal from "./LoanDetailModal";

const OneLoanCard = ({ Title, loan, getAllData, setLoanUpdated }) => {
  const { user } = useSelector((state) => state.user);
  const [editOpen, setEditOpen] = useState(false);
  const [detailOpen, setDetailOpen] = useState(false);
  const [loanTransactions, setLoanTransactions] = useState([]);
  const [form] = Form.useForm();
  const onFinish = async (values) => {
    const date = dayjs(values.date).format("DD-MM-YYYY");
    const updatedLoan = {
      dateString: date,
      loan_type: values.loan_type,
      status: values.status,
      user_id: user.id,
      amount: values.amount,
      person: values.person,
      reason: values.reason,
      loan_id: loan.id,
    };
    await updateLoan(updatedLoan).then((res) => {
      if (res && res.status !== false) {
        message.success("Loan updated successfully");
        setEditOpen(false);
        getAllData(user.id);
        setLoanUpdated(true);
      }
    });
  };
  const handleDeleteLoan = async () => {
    const params = {
      loan_id: loan.id,
    };
    await deleteLoan(params).then((res) => {
      if (res && res?.status !== false) {
        message.success("Loan deleted successfully");
        getAllData(user.id);
        setLoanUpdated(true);
      }
    });
  };
  const handleCancel = () => {
    form.resetFields();
    setEditOpen(false);
  };
  // Loan Transaction
  const handleViewDetails = async () => {
    const res = await getLoanTransactions(loan.id);
    if (res && res.status !== false) {
      setLoanTransactions(res);
      setDetailOpen(true);
    }
  };
  return (
    <Row key={loan}>
      <Col span={24}>
        <Card
          title={
            <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
              {`${Title}: 「${loan ? loan.person : "--"}」`}
              <Tag color={loan.status === "PENDING" ? "gold" : "green"}>
                {loan ? loan.status : "--"}
              </Tag>
              <Tag color={loan.loan_type === "GIVEN" ? "volcano" : "geekblue"}>
                <span>{loan ? loan.loan_type : "--"}</span>
                <span style={{ marginLeft: 5 }}>
                  {loan.loan_type === "GIVEN" ? (
                    <ArrowRightOutlined />
                  ) : (
                    <ArrowLeftOutlined />
                  )}
                </span>
              </Tag>
            </div>
          }
          bordered={false}
          hoverable={true}
          headStyle={{ padding: 10, fontSize: 18, fontWeight: "bold" }}
          bodyStyle={{ padding: 10 }}
          extra={
            <div style={{ display: "flex", gap: 10 }}>
              <Popconfirm
                title="Delete the Loan"
                description="Are you sure to delete this loan?"
                onConfirm={handleDeleteLoan}
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
              <Button size="small" onClick={handleViewDetails}>
                <InfoCircleOutlined /> View Details
              </Button>
            </div>
          }
        >
          <div style={{ fontSize: 18 }}>
            Person: {loan ? loan.person : "--"}
          </div>
          <div style={{ display: "flex", alignItems: "baseline", gap: 10 }}>
            <div style={{ fontSize: 18 }}>Loan Amount:</div>
            <span style={{ fontSize: 24, fontWeight: "bold" }}>
              {loan.amount  ? `$${parseFloat(loan.amount).toFixed(2)}` : "--"}
            </span>
          </div>
          <div style={{ fontSize: 18 }}>
            Reason: {loan ? loan.reason : "--"}
          </div>
          <div style={{ display: "flex", gap: 30, justifyContent: "end" }}>
            <div style={{ fontSize: 16 }}>
              Date:{" "}
              {loan
                ? loan.date && formatDateToMalaysia(new Date(loan.date))
                : "--"}
            </div>
          </div>
        </Card>
      </Col>
      <Modal
        open={editOpen}
        onCancel={handleCancel}
        onOk={handleCancel}
        title={"Edit Loan"}
        footer={null}
      >
        <Form
          form={form}
          onFinish={onFinish}
          labelCol={{ span: 8 }}
          wrapperCol={{ span: 16 }}
          style={{ maxWidth: 600 }}
          initialValues={{
            ...loan,
            date: loan?.date ? dayjs(loan?.date, "YYYY-MM-DD") : null, // Change the format here
          }}
          autoComplete="off"
        >
          <Form.Item
            label="Person"
            name="person"
            rules={[{ required: true, message: "Please input person name!" }]}
          >
            <Input />
          </Form.Item>

          <Form.Item
            label="Date"
            name={"date"}
            rules={[{ required: true, message: "Please select a date!" }]}
          >
            <DatePicker format={"DD/MM/YYYY"} />
          </Form.Item>

          <Form.Item
            label="Amount"
            name={"amount"}
            rules={[
              { required: true, message: "Please input the loan amount!" },
            ]}
          >
            <InputNumber step={0.01} min={0} />
          </Form.Item>

          <Form.Item
            label="Loan Type"
            name={"loan_type"}
            rules={[{ required: true, message: "Please select a loan type!" }]}
          >
            <Select>
              <Select.Option value="GIVEN">Given</Select.Option>
              <Select.Option value="TAKEN">Taken</Select.Option>
            </Select>
          </Form.Item>

          <Form.Item
            label="Status"
            name={"status"}
            rules={[{ required: true, message: "Please select a status!" }]}
          >
            <Select>
              <Select.Option value="PENDING">Pending</Select.Option>
              <Select.Option value="SETTLED">Settled</Select.Option>
            </Select>
          </Form.Item>

          <Form.Item
            label="Reason"
            name={"reason"}
            rules={[{ required: true, message: "Please input a reason!" }]}
          >
            <TextArea rows={4} />
          </Form.Item>

          <Form.Item wrapperCol={{ offset: 8, span: 16 }}>
            <Button type="primary" htmlType="submit">
              Update
            </Button>
          </Form.Item>
        </Form>
      </Modal>
      <LoanDetailModal
        detailOpen={detailOpen}
        setDetailOpen={setDetailOpen}
        loanTransactions={loanTransactions}
        handleViewDetails={handleViewDetails}
        setLoanUpdated={setLoanUpdated}
        loan={loan}
      />
    </Row>
  );
};

export default OneLoanCard;
