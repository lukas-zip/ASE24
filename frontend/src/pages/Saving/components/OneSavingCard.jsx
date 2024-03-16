import React, { useState } from 'react'
import { formatDateToMalaysia } from '../../../utils/convertDate'
import { Card, Col, Modal, Row, Button, InputNumber, DatePicker, Form, Input, message, Popconfirm, Select, Badge } from 'antd';
import { DeleteOutlined, EditOutlined, PlusOutlined, } from '@ant-design/icons';
import dayjs from 'dayjs';
import { addMoreSaving, deleteSaving, updateSaving } from '../../../api/saving.api';
import { useSelector } from 'react-redux';
const { TextArea } = Input;

const OneSavingCard = ({ Title, saving, expenseCategory, allCategories, getAllData }) => {
    const { user } = useSelector(state => state.user)
    const [editOpen, setEditOpen] = useState(false)
    const [addMoreSavingOpen, setAddMoreSavingOpen] = useState(false)

    const onFinish = async (values) => {
        const targetDate = formatDateToMalaysia(new Date(values.targetDate))
        const updatedSaving = { ...values, targetDate, user_id: user.id }
        await updateSaving(updatedSaving, saving.id).then(res => {
            if (res && res.status !== false) {
                message.success('Saving updated successfully')
                setEditOpen(false)
                getAllData()
            }
        })
    };

    const onAddSavingFinish = async (values) => {
        const updatedSaving = { ...values }
        await addMoreSaving(updatedSaving, saving.id).then(res => {
            if (res && res.status !== false) {
                message.success('Saving updated successfully')
                setAddMoreSavingOpen(false)
                getAllData()
            } 
        })
    };

    const handleDeleteSaving = async () => {
        await deleteSaving(saving.id).then(res => {
            if (res && res?.status !== false) {
                message.success('Saving deleted successfully')
                getAllData()
            }
        })
    }
    
    return (
        <Row key={saving}>
            <Col span={24}>
                <Badge.Ribbon text={ saving ? (saving?.is_achieved ? 'Achieved' : 'Not Achieved') : 'Not Achieved'} color={ saving ? (saving?.is_achieved ? 'green' : 'red') : 'red'}>
                    <Card
                        title={`Target Date: ${saving ? (saving?.targetDate && formatDateToMalaysia(new Date(saving?.targetDate))) : "--"} (${saving?.goal_val - saving?.saving_val} more to save)`}
                        bordered={false}
                        hoverable={true}
                        headStyle={{ padding: 10, fontSize: 18, fontWeight: 'bold' }}
                        bodyStyle={{ padding: 10 }}
                    >
                        <div style={{ fontSize: 18 }}>
                            Category: 
                            <span style={{ marginLeft: 10, fontWeight: 'bold' }}>
                                {expenseCategory.category_name ? expenseCategory?.category_name : "--"}
                            </span>
                        </div>

                        <div style={{ fontSize: 18 }}>
                            Goal Amount:
                            <span style={{ marginLeft: 10, fontWeight: 'bold' }}>
                                {saving ? saving?.goal_val : "--"}
                            </span>
                        </div>

                        <div style={{ fontSize: 18 }}>
                            Saving Amount:
                            <span style={{ marginLeft: 10, fontWeight: 'bold' }}>
                                {saving ? saving?.saving_val : "--"}
                            </span>
                        </div>
                            
                        <div style={{ fontSize: 18 }}>
                            Comment: {saving.comments ? saving.comments : "--"}
                        </div>
                        <div style={{ display: 'flex', gap: 10, justifyContent: 'end' }}>
                            <Popconfirm
                                title="Delete the Saving"
                                description="Are you sure to delete this saving?"
                                onConfirm={handleDeleteSaving}
                                okText="Yes"
                                cancelText="No"
                            >
                                <Button danger size='small'><DeleteOutlined /> Delete</Button>
                            </Popconfirm>
                            <Button size='small' onClick={() => setEditOpen(true)}><EditOutlined /> Update
                            </Button>
                            <Button size='small' onClick={() => setAddMoreSavingOpen(true)}><PlusOutlined /> Add More Saving
                            </Button>
                        </div>
                    </Card>
                </Badge.Ribbon>
            </Col>
            <Modal
                open={editOpen}
                onCancel={() => setEditOpen(false)}
                onOk={() => setEditOpen(false)}
                title={"Edit Saving"}
                footer={null}
            >
                <Form
                    onFinish={onFinish}
                    labelCol={{ span: 8, }}
                    wrapperCol={{ span: 16, }}
                    style={{ maxWidth: 600, }}
                    initialValues={{
                        ...saving,
                        targetDate: saving?.targetDate ? dayjs(formatDateToMalaysia(new Date(saving?.targetDate)), 'DD/MM/YYYY') : null,
                        category_id: expenseCategory.id,
                    }}
                    autoComplete="off"
                >
                    <Form.Item label="Target Date" name={"targetDate"}
                        rules={[{ required: true, message: 'Please input target date!', }]} >
                        <DatePicker format={"DD/MM/YYYY"} />
                    </Form.Item>
                    <Form.Item label="Goal Amount" name={"goal_val"}
                        rules={[{ required: true, message: 'Please input goal amount!', }]} >
                        <InputNumber step={0.01} min={0} />
                    </Form.Item>
                    <Form.Item label="Saving Amount" name={"saving_val"}
                        rules={[{ required: true, message: 'Please input saving amount!', }]} >
                        <InputNumber step={0.01} min={0} />
                    </Form.Item>
                    <Form.Item label="Saving For" name={"category_id"} 
                        rules={[{ required: true, message: 'Please select category for saving!', }]} >
                        <Select>
                            {allCategories.map(category => (
                                <Select.Option key={category.id} value={category.id}>
                                    {category.category_name}
                                </Select.Option>
                            ))}
                        </Select>
                    </Form.Item>
                    <Form.Item label="Comments" name={"comments"}>
                        <TextArea rows={4} />
                    </Form.Item>
                    <Form.Item wrapperCol={{ offset: 8, span: 16, }}>
                        <Button type="primary" htmlType="submit">
                            Save
                        </Button>
                    </Form.Item>
                </Form>
            </Modal>

            <Modal
                open={addMoreSavingOpen}
                onCancel={() => setAddMoreSavingOpen(false)}
                onOk={() => setAddMoreSavingOpen(false)}
                title={"Add More Saving"}
                footer={null}
            >
                <Form
                    onFinish={onAddSavingFinish}
                    labelCol={{ span: 10, }}
                    wrapperCol={{ span: 14, }}
                    style={{ maxWidth: 600, }}
                    autoComplete="off"
                >
                    <Form.Item label="Added Saving Amount" name={"saving_val"}
                        rules={[{ required: true, message: 'Please input added saving amount!', }]} >
                        <InputNumber step={0.01} min={0} />
                    </Form.Item>
                    <Form.Item wrapperCol={{ offset: 10, span: 14, }}>
                        <Button type="primary" htmlType="submit">
                            Save
                        </Button>
                    </Form.Item>
                </Form>
            </Modal>
        </Row >
    )
}

export default OneSavingCard