import React, { useEffect, useState } from "react";
import { recordPayment, recordReception, editLoanTransaction, deleteLoanTransaction } from "../../../api/loan.api";
import { List, Button, Modal, Form, InputNumber, message, Select, Checkbox, Tag } from "antd";
import { formatDateToMalaysia } from "../../../utils/convertDate";
import { DollarCircleOutlined } from "@ant-design/icons";
import { useSelector } from "react-redux";

const LoanDetailModal = ({ detailOpen, setDetailOpen, loanTransactions, loan, handleViewDetails, setLoanUpdated }) => {
  const { user } = useSelector((state) => state.user);
  const { Option } = Select;
  const [recordOpen, setRecordOpen] = useState(false);
  const [editTransactionOpen, setEditTransactionOpen] = useState(false);
  const [editTransactionForm] = Form.useForm();
  const [currentTransaction, setCurrentTransaction] = useState(null);
  const [recordForm] = Form.useForm();
  const [remainingLoanAmount, setRemainingLoanAmount] = useState(loan.amount);

  const handleRecordPayment = async (values) => {
    const params = {
      loan_id: loan.id,
      transaction_val: values.amount,
      user_id: user.id,
      transactionFrequency: values.transactionFrequency,
      isRecurring: values.isRecurring,
    };
    const res = await recordPayment(params);
    if (res && res.status !== false) {
      message.success("Payment recorded successfully");
      handleViewDetails(); // refresh the loan transactions
      setLoanUpdated(true);
      recordForm.resetFields(); // reset the form fields
      setRecordOpen(false); // close the record modal
    }
  };

  const handleRecordReception = async (values) => {
    const params = {
      loan_id: loan.id,
      transaction_val: values.amount,
      user_id: user.id,
      transactionFrequency: values.transactionFrequency,
      isRecurring: values.isRecurring,
    };
    const res = await recordReception(params);
    if (res && res.status !== false) {
      message.success("Reception recorded successfully");
      handleViewDetails(); // refresh the loan transactions
      setLoanUpdated(true);
      recordForm.resetFields(); // reset the form fields
      setRecordOpen(false); // close the record modal
    }
  };

  const handleEditLoanTransaction = async (transactionId, amount, isRecurring, transactionFrequency) => {
    const params = {
      transaction_id: transactionId,
      transaction_val: amount,
      loan_id: loan.id, // include the loan id
      user_id: user.id, // include the user id
      isRecurring: isRecurring,
      transactionFrequency: transactionFrequency,
    };
    const res = await editLoanTransaction(params);
    if (res && res.status !== false) {
      message.success("Loan transaction updated successfully");
      handleViewDetails(); // refresh the loan transactions
      setLoanUpdated(true);
    }
  };

  const handleDeleteLoanTransaction = async (transactionId) => {
    const params = {
      transaction_id: transactionId,
    };
    const res = await deleteLoanTransaction(params);
    if (res && res.status !== false) {
      message.success("Loan transaction deleted successfully");
      setLoanUpdated(true);
      handleViewDetails(); // refresh the loan transactions
    }
  };

  const handleOpenEditTransactionModal = (transaction) => {
    setCurrentTransaction(transaction);
    editTransactionForm.setFieldsValue({
      amount: transaction.amount,
      isRecurring: transaction.isRecurring,
      transactionFrequency: transaction.transactionFrequency,
    });
    setEditTransactionOpen(true);
  };

  const handleEditTransactionSubmit = async (values) => {
    await handleEditLoanTransaction(currentTransaction.id, values.amount, values.isRecurring, values.transactionFrequency);
    setEditTransactionOpen(false);
  };

  const handleOpenRecordModal = () => {
    setRecordOpen(true);
  };

  useEffect(() => {
    // calculate the remaining loan amount whenever the loan transactions are updated
    const totalTransactionAmount = loanTransactions.reduce((total, transaction) => total + transaction.amount, 0);
    setRemainingLoanAmount(loan.amount - totalTransactionAmount);
  }, [loanTransactions, loan.amount]);

  return (
    <Modal open={detailOpen} onCancel={() => setDetailOpen(false)} title={"Loan Details"} footer={null}>
      <h2>Remaining Loan Amount: {remainingLoanAmount}</h2>
      <List
        itemLayout="horizontal"
        dataSource={loanTransactions}
        renderItem={(item) => {
          return (
            <List.Item
              actions={[
                <Button onClick={() => handleOpenEditTransactionModal(item)}>Edit</Button>,
                <Button danger onClick={() => handleDeleteLoanTransaction(item.id)}>
                  Delete
                </Button>,
              ]}
            >
              <List.Item.Meta
                title={
                  <div style={{ display: "flex", alignItems: "center" }}>
                    <span style={{ fontWeight: "bold", fontSize: "18px" }}>Transaction ID: {item.id}</span>
                    {item.isRecurring && (
                      <Tag color="blue" style={{ marginLeft: "10px" }}>
                        {item.transactionFrequency}
                      </Tag>
                    )}
                  </div>
                }
                description={
                  <div>
                    <p>
                      <strong>Amount:</strong> {item.amount}
                    </p>
                    <p>
                      <strong>Date:</strong> {formatDateToMalaysia(new Date(item.date))}
                    </p>
                    <p>
                      <strong>Type:</strong> {item.transactionType}
                    </p>
                  </div>
                }
              />
            </List.Item>
          );
        }}
      />
      <Button type="primary" icon={<DollarCircleOutlined />} onClick={handleOpenRecordModal}>
        {loan.loan_type === "GIVEN" ? "Record Reception" : "Record Payment"}
      </Button>
      <Modal open={recordOpen} onCancel={() => setRecordOpen(false)} title={"Record Transaction"} footer={null}>
        <Form
          form={recordForm}
          onFinish={loan.loan_type === "GIVEN" ? handleRecordReception : handleRecordPayment}
          labelCol={{ span: 8 }}
          wrapperCol={{ span: 16 }}
          style={{ maxWidth: 600 }}
          autoComplete="off"
        >
          <Form.Item label="Amount" name={"amount"} rules={[{ required: true, message: "Please input the transaction amount!" }]}>
            <InputNumber step={0.01} min={0} />
          </Form.Item>
          <Form.Item label="Is Recurring" name={"isRecurring"} valuePropName="checked">
            <Checkbox />
          </Form.Item>
          <Form.Item shouldUpdate={(prevValues, currentValues) => prevValues.isRecurring !== currentValues.isRecurring}>
            {({ getFieldValue }) => {
              return getFieldValue("isRecurring") ? (
                <Form.Item labelCol={{ span: 12 }} wrapperCol={{ span: 16 }} label="Frequency" name={"transactionFrequency"}
                    rules={[
                      {
                          required: recordForm.getFieldValue("isRecurring"),
                          message: "Please select a frequency!",
                      },
                  ]}>
                  <Select>
                    <Option value="DAILY">Daily</Option>
                    <Option value="WEEKLY">Weekly</Option>
                    <Option value="MONTHLY">Monthly</Option>
                  </Select>
                </Form.Item>
              ) : null;
            }}
          </Form.Item>
          <Form.Item wrapperCol={{ offset: 8, span: 16 }}>
            <Button type="primary" htmlType="submit">
              Record
            </Button>
          </Form.Item>
        </Form>
      </Modal>
      <Modal title="Edit Transaction" open={editTransactionOpen} onCancel={() => setEditTransactionOpen(false)} footer={null}>
        <Form form={editTransactionForm} onFinish={handleEditTransactionSubmit} labelCol={{ span: 8 }} wrapperCol={{ span: 16 }} style={{ maxWidth: 600 }} autoComplete="off">
          <Form.Item label="Amount" name="amount" rules={[{ required: true, message: "Please input the transaction amount!" }]}>
            <InputNumber step={0.01} min={0} />
          </Form.Item>
          <Form.Item label="Is Recurring" name={"isRecurring"} valuePropName="checked">
            <Checkbox />
          </Form.Item>
        <Form.Item shouldUpdate={(prevValues, currentValues) => prevValues.isRecurring !== currentValues.isRecurring}>
            {({ getFieldValue }) => {
                return getFieldValue("isRecurring") ? (
                    <Form.Item
                        name="transactionFrequency"
                        rules={[
                            {
                                required: editTransactionForm.getFieldValue("isRecurring"),
                                message: "Please select a frequency!",
                            },
                        ]}
                        labelCol={{ span: 12 }} wrapperCol={{ span: 16 }} label="Frequency"
                    >
                        <Select>
                            <Option value="DAILY">Daily</Option>
                            <Option value="WEEKLY">Weekly</Option>
                            <Option value="MONTHLY">Monthly</Option>
                        </Select>
                    </Form.Item>
                ) : (
                    <div style={{ display: 'none' }}></div>
                );
            }}
        </Form.Item>
          <Form.Item wrapperCol={{ offset: 8, span: 16 }}>
            <Button type="primary" htmlType="submit">
              Update
            </Button>
          </Form.Item>
        </Form>
      </Modal>
    </Modal>
  );
};

export default LoanDetailModal;
