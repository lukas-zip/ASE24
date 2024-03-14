import React, { useState } from 'react'
import { deleteBudget, updateBudget } from '../../../api/budget.api'
import { formatDateToMalaysia } from '../../../utils/convertDate'
import { Card, Col, Modal, Row, Button, InputNumber, DatePicker, Form, Input, message, Popconfirm } from 'antd';
import { DeleteOutlined, EditOutlined, } from '@ant-design/icons';
import dayjs from 'dayjs';
const { TextArea } = Input;

const OneBudgetCard = ({ Title, budget, getAllData }) => {
    const [editOpen, setEditOpen] = useState(false)
    const onFinish = async (values) => {
        const startDate = formatDateToMalaysia(new Date(values.startDate))
        const endDate = formatDateToMalaysia(new Date(values.endDate))
        const updatedBudget = { ...values, startDate, endDate, budgetId: budget.id }
        await updateBudget(updatedBudget).then(res => {
            if (res && res.status !== false) {
                message.success('Budget updated successfully')
                setEditOpen(false)
                getAllData()
            }
        })
    };
    const handleDeleteBudget = async () => {
        const params = {
            budgetId: budget.id
        }
        await deleteBudget(params).then(res => {
            if (res && res?.status !== false) {
                if (Title === "Current Budget") {
                    window.location.reload()
                }
                message.success('Budget deleted successfully')
                getAllData()
            }
        })
    }
    return (
      <Row key={budget}>
        <Col span={24}>
          <Card
            title={`${Title}: 「${budget ? budget?.name : "--"}」`}
            bordered={false}
            hoverable={true}
            headStyle={{ padding: 10, fontSize: 18, fontWeight: "bold" }}
            bodyStyle={{ padding: 10 }}
            extra={
              <div style={{ display: "flex", gap: 10 }}>
                <Popconfirm
                  title="Delete the Budget"
                  description="Are you sure to delete this budget?"
                  onConfirm={handleDeleteBudget}
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
              <div style={{ fontSize: 18 }}>Budget Amount:</div>{" "}
              <span style={{ fontSize: 24, fontWeight: "bold" }}>
                {budget.budgetAmount  ? `$${parseFloat(budget.budgetAmount).toFixed(2)}` : "--"}
              </span>
            </div>
            <div style={{ fontSize: 18 }}>
              Comment: {budget ? budget?.comments : "--"}
            </div>
            <div style={{ display: "flex", gap: 30, justifyContent: "end" }}>
              <div style={{ fontSize: 16 }}>
                Start Date:{" "}
                {budget
                  ? budget?.startDate &&
                    formatDateToMalaysia(new Date(budget?.startDate))
                  : "--"}
              </div>
              <div style={{ fontSize: 16 }}>
                End date:{" "}
                {budget
                  ? budget?.endDate &&
                    formatDateToMalaysia(new Date(budget?.endDate))
                  : "--"}
              </div>
            </div>
          </Card>
        </Col>
        <Modal
          open={editOpen}
          onCancel={() => setEditOpen(false)}
          onOk={() => setEditOpen(false)}
          title={"Edit Budget"}
          footer={null}
        >
          <Form
            onFinish={onFinish}
            labelCol={{ span: 8 }}
            wrapperCol={{ span: 16 }}
            style={{ maxWidth: 600 }}
            initialValues={{
              ...budget,
              startDate: budget?.startDate
                ? dayjs(
                    formatDateToMalaysia(new Date(budget?.startDate)),
                    "DD/MM/YYYY"
                  )
                : null,
              endDate: budget?.endDate
                ? dayjs(
                    formatDateToMalaysia(new Date(budget?.endDate)),
                    "DD/MM/YYYY"
                  )
                : null,
            }}
            autoComplete="off"
          >
            <Form.Item
              label="name"
              name="name"
              rules={[{ required: true, message: "Please input budget name!" }]}
            >
              <Input />
            </Form.Item>

            <Form.Item label="Start Date" name={"startDate"}>
              <DatePicker format={"DD/MM/YYYY"} />
            </Form.Item>
            <Form.Item label="End Date" name={"endDate"}>
              <DatePicker format={"DD/MM/YYYY"} />
            </Form.Item>
            <Form.Item label="Budegt Amount" name={"budgetAmount"}>
              <InputNumber step={0.01} min={0} />
            </Form.Item>
            <Form.Item label="comments" name={"comments"}>
              <TextArea rows={4} />
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
}

export default OneBudgetCard