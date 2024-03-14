import React, { useState, useRef } from "react";
import { createNewLoan } from "../../../api/loan.api";
import { useSelector } from "react-redux";
import { Select, Col, Modal, Row, Space, Button, InputNumber, DatePicker, Form, Input, message, Card } from "antd";
import { DownOutlined, FileOutlined, UpOutlined, UploadOutlined } from "@ant-design/icons";
import COLORS from "../../../constants/COLORS";
import OneLoanCard from "./OneLoanCard";
import dayjs from "dayjs";
const { TextArea } = Input;

const AllLoanRecords = ({ getAllData, allLoans, setLoanUpdated }) => {
  const { user } = useSelector((state) => state.user);
  const [collapsed, setCollapsed] = useState(false);
  const [createOpen, setCreateOpen] = useState(false);
  const formRef = useRef(null);
  const onFinishCreate = async (values) => {
    const date = dayjs(values.date).format("DD-MM-YYYY");
    const updatedLoan = {
      dateString: date,
      loan_type: values.loan_type,
      status: values.status,
      user_id: user.id,
      amount: values.amount,
      person: values.person,
      reason: values.reason,
    };
    await createNewLoan(updatedLoan).then((res) => {
      if (res && res.status !== false) {
        message.success("Loan create successfully");
        setCreateOpen(false);
        getAllData(user.id);
        formRef.current.resetFields();
        setLoanUpdated(true);
      } else {
        console.log(res);
      }
    });
  };
  return (
    <>
      <Row>
        <Col span={24}>
          <Card bodyStyle={{ width: "100%", padding: 10, borderRadius: 10 }}>
            <div style={{ width: "100%", display: "flex", justifyContent: "space-between", alignItems: "center" }}>
              <div style={{ fontWeight: "bold", fontSize: 18 }}>
                <FileOutlined /> Total {allLoans.length} Loans{" "}
                {collapsed ? (
                  <span className="hoverButton" style={{ fontSize: 14, fontWeight: "normal", marginLeft: 8 }} onClick={() => setCollapsed(!collapsed)}>
                    Collapsed <UpOutlined />
                  </span>
                ) : (
                  <span className="hoverButton" style={{ fontSize: 14, fontWeight: "normal", marginLeft: 8 }} onClick={() => setCollapsed(!collapsed)}>
                    Expand <DownOutlined />
                  </span>
                )}
              </div>
              <div
                className="hoverButton"
                onClick={() => setCreateOpen(true)}
                style={{ userSelect: "none", borderRadius: 10, padding: 10, backgroundColor: COLORS.primary, color: "white" }}
              >
                Create Loan <UploadOutlined />
              </div>
            </div>
            {!collapsed && (
              <Space
                direction="vertical"
                size="small"
                style={{
                  display: "flex",
                }}
              >
                {allLoans.map((item, index) => (
                  <OneLoanCard Title={"Loan"} getAllData={getAllData} loan={item} key={index} setLoanUpdated={setLoanUpdated} />
                ))}
              </Space>
            )}
          </Card>
        </Col>
      </Row>
      <Modal
        open={createOpen}
        onCancel={() => {
          setCreateOpen(false);
          formRef.current.resetFields();
        }}
        onOk={() => setCreateOpen(false)}
        title={"Create Loan"}
        footer={null}
      >
        <Form ref={formRef} onFinish={onFinishCreate} labelCol={{ span: 8 }} wrapperCol={{ span: 16 }} style={{ maxWidth: 600 }} autoComplete="off">
          <Form.Item label="Person" name="person" rules={[{ required: true, message: "Please input person name!" }]}>
            <Input />
          </Form.Item>

          <Form.Item label="Date" name={"date"} rules={[{ required: true, message: "Please select a date!" }]}>
            <DatePicker format={"DD/MM/YYYY"} />
          </Form.Item>

          <Form.Item label="Amount" name={"amount"} rules={[{ required: true, message: "Please input the loan amount!" }]}>
            <InputNumber step={0.01} min={0} />
          </Form.Item>

          <Form.Item label="Loan Type" name={"loan_type"} rules={[{ required: true, message: "Please select a loan type!" }]}>
            <Select>
              <Select.Option value="GIVEN">Given</Select.Option>
              <Select.Option value="TAKEN">Taken</Select.Option>
            </Select>
          </Form.Item>

          <Form.Item label="Status" name={"status"} rules={[{ required: true, message: "Please select a status!" }]}>
            <Select>
              <Select.Option value="PENDING">Pending</Select.Option>
              <Select.Option value="SETTLED">Settled</Select.Option>
            </Select>
          </Form.Item>

          <Form.Item label="Reason" name={"reason"} rules={[{ required: true, message: "Please input a reason!" }]}>
            <TextArea rows={4} />
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

export default AllLoanRecords;
