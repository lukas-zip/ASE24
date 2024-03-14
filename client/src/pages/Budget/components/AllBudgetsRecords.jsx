import React, { useState } from 'react'
import { createNewBudget, } from '../../../api/budget.api'
import { formatDateToMalaysia } from '../../../utils/convertDate'
import { useSelector } from 'react-redux'
import { Col, Modal, Row, Space, Button, InputNumber, DatePicker, Form, Input, message, Card } from 'antd';
import { DownOutlined, FileOutlined, UpOutlined, UploadOutlined } from '@ant-design/icons';
import COLORS from '../../../constants/COLORS';
import OneBudgetCard from './OneBudgetCard';
const { TextArea } = Input;

const AllBudgetsRecords = ({ getAllData, allBudgets }) => {
    const { user } = useSelector(state => state.user)
    const [collapsed, setCollapsed] = useState(false);
    const [createOpen, setCreateOpen] = useState(false)
    const onFinishCreate = async (values) => {
        const startDate = formatDateToMalaysia(new Date(values.startDate))
        const endDate = formatDateToMalaysia(new Date(values.endDate))
        const updatedBudget = { ...values, startDate, endDate, userId: user.id }
        await createNewBudget(updatedBudget).then(res => {
            if (res && res.status !== false) {
                message.success('Budget create successfully')
                setCreateOpen(false)
                getAllData()
            } else {
                console.log(res);
            }
        })
    };
    return (
        <>
            <Row>
                <Col span={24}>
                    <Card bodyStyle={{ width: "100%", padding: 10, borderRadius: 10, }}>
                        <div style={{ width: "100%", display: 'flex', justifyContent: 'space-between', alignItems: 'center', }}>
                            <div style={{ fontWeight: 'bold', fontSize: 18 }}>
                                <FileOutlined /> Total {allBudgets.length} Budgets {collapsed ? <span className='hoverButton' style={{ fontSize: 14, fontWeight: 'normal', marginLeft: 8 }} onClick={() => setCollapsed(!collapsed)}>Collapsed <UpOutlined /></span> : <span className='hoverButton' style={{ fontSize: 14, fontWeight: 'normal', marginLeft: 8 }} onClick={() => setCollapsed(!collapsed)}>Expand <DownOutlined /></span>}
                            </div>
                            <div className='hoverButton' onClick={() => setCreateOpen(true)} style={{ userSelect: 'none', borderRadius: 10, padding: 10, backgroundColor: COLORS.primary, color: 'white' }}>Create Budget <UploadOutlined /></div>
                        </div>
                        {!collapsed && <Space
                            direction="vertical"
                            size="small"
                            style={{
                                display: 'flex',
                            }}
                        >
                            {allBudgets.map((item, index) => <OneBudgetCard Title={"Budget"} getAllData={getAllData} budget={item} key={index} />)}
                        </Space>}
                    </Card>
                </Col>
            </Row>
            <Modal
                open={createOpen}
                onCancel={() => setCreateOpen(false)}
                onOk={() => setCreateOpen(false)}
                title={"Create Budget"}
                footer={null}
            >
                <Form
                    onFinish={onFinishCreate}
                    labelCol={{ span: 8, }}
                    wrapperCol={{ span: 16, }}
                    style={{ maxWidth: 600, }}
                    autoComplete="off"
                >
                    <Form.Item label="name" name="name"
                        rules={[{ required: true, message: 'Please input budget name!', }]}
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
                    <Form.Item wrapperCol={{ offset: 8, span: 16, }}>
                        <Button type="primary" htmlType="submit">
                            Update
                        </Button>
                    </Form.Item>
                </Form>
            </Modal>
        </>
    )
}

export default AllBudgetsRecords
