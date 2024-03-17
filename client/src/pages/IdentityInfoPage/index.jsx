import React from 'react'
import { Avatar, Button, Modal, DatePicker, Form, Input, InputNumber, Radio, Select, message, Upload } from 'antd'
import { UserOutlined, EditOutlined, UploadOutlined, ArrowRightOutlined, RightOutlined } from '@ant-design/icons';
const { TextArea } = Input;
import dayjs from 'dayjs';
import CONSTANTS from '../../constants';
import COLORS from '../../constants/COLORS';

const normFile = (e) => {
    if (Array.isArray(e)) {
        return e;
    }
    return e?.fileList;
};

function IdentityInfoPage() {
    return (
        <div className={`Login_mainBox`}>
            <div className='box'>
                <div className='inner-box'>
                    <div style={{ fontSize: 36, color: COLORS.commentText, marginBottom: 10 }}>
                        Welcome to Clarie~
                    </div>
                    <Form variant="filled" labelCol={{ span: 8, }} wrapperCol={{ span: 10, }} layout="horizontal" style={{}} onFinish={{}} onFinishFailed={{}}>
                        <Form.Item name="gender" label={'Your Identity'}>
                            <Radio.Group>
                                <Radio value="Male">Seller</Radio>
                                <Radio value="Female">Buyer</Radio>
                            </Radio.Group>
                        </Form.Item>
                        <Form.Item label={'Avatar'} valuePropName="fileList" getValueFromEvent={normFile}>
                            {/* <Upload name="image" listType="picture" customRequest={submitImageToFirebase} maxCount={1} {...propsImage}> */}
                            <Upload name="image" listType="picture" customRequest={{}} maxCount={1} >
                                <Button icon={<UploadOutlined />}>Upload Avatar</Button>
                            </Upload>
                        </Form.Item>
                        <Form.Item name="name" label={"userName"}>
                            <Input />
                        </Form.Item>
                        <Form.Item name="personalStatus" label={'bio'}>
                            <TextArea rows={2} />
                        </Form.Item>
                        <Form.Item name="hpNum" label={'app.prf.label.hpNum'}>
                            <Input />
                        </Form.Item>
                        <Form.Item name="birthday" label={'app.prf.label.birthday'}>
                            <DatePicker />
                        </Form.Item>
                        <Button style={{ marginLeft: 400 }} size='large' type="primary" htmlType="submit">
                            Enter Clarie <RightOutlined />
                        </Button>
                    </Form>
                </div >
            </div >
        </div >
    )
}

export default IdentityInfoPage