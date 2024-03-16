import React, { useState } from 'react'
import { formatDateToMalaysia } from '../../../utils/convertDate'
import { useSelector } from 'react-redux'
import { Col, Modal, Row, Space, Button, InputNumber, DatePicker, Form, Input, message, Select, Card } from 'antd';
import { DownOutlined, FileOutlined, UpOutlined, UploadOutlined } from '@ant-design/icons';
import COLORS from '../../../constants/COLORS';
import OneSavingCard from './OneSavingCard';
import { createNewSaving } from '../../../api/saving.api';
const { TextArea } = Input;

const AllSavingsRecords = ({ getAllData, allSavings, allCategories }) => {
    const { user } = useSelector(state => state.user)
    const [collapsed, setCollapsed] = useState(false)
    const [createOpen, setCreateOpen] = useState(false)
    const onFinishCreate = async (values) => {
        const targetDate = formatDateToMalaysia(new Date(values.targetDate))
        const updatedSaving = { ...values, targetDate, user_id: user.id }
        await createNewSaving(updatedSaving).then(res => {
            if (res && res.status !== false) {
                message.success('Saving create successfully')
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
                    <Card bodyStyle={{ padding: 0 }} style={{ width: "100%", padding: 10, borderRadius: 10, }}>
                        <div style={{ width: "100%", display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 8, }}>
                            <div style={{ fontWeight: 'bold', fontSize: 18 }}>
                                <FileOutlined /> Total {allSavings.length} Savings {collapsed ? <span className='hoverButton' style={{ fontSize: 14, fontWeight: 'normal', marginLeft: 8 }} onClick={() => setCollapsed(!collapsed)}>Collapsed <UpOutlined /></span> : <span className='hoverButton' style={{ fontSize: 14, fontWeight: 'normal', marginLeft: 8 }} onClick={() => setCollapsed(!collapsed)}>Expand <DownOutlined /></span>}
                            </div>
                            <div className='hoverButton' onClick={() => setCreateOpen(true)} style={{ userSelect: 'none', borderRadius: 10, padding: 10, backgroundColor: COLORS.primary, color: 'white' }}>Create Saving <UploadOutlined /></div>
                        </div>
                        {!collapsed && <Space
                            direction="vertical"
                            size="small"
                            style={{
                                display: 'flex',
                            }}
                        >
                            {allSavings.map((item, index) => <OneSavingCard Title={"Saving"} getAllData={getAllData} saving={item} expenseCategory={item.category} allCategories={allCategories} key={index} />)}
                        </Space>}
                    </Card>
                </Col>
            </Row>
            <Modal
                open={createOpen}
                onCancel={() => setCreateOpen(false)}
                onOk={() => setCreateOpen(false)}
                title={"Create Saving"}
                footer={null}
            >
                <Form
                    onFinish={onFinishCreate}
                    labelCol={{ span: 8, }}
                    wrapperCol={{ span: 16, }}
                    style={{ maxWidth: 600, }}
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
        </>
    )
}

export default AllSavingsRecords
