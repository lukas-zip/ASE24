import { Avatar, Button, Modal, Form, Input, message, Upload } from 'antd'
import { UserOutlined, EditOutlined, UploadOutlined } from '@ant-design/icons';
import React, { useRef, useState } from 'react'
import './index.less'
import { useDispatch } from 'react-redux'
import { useSelector } from 'react-redux'
import COLORS from '@/constants/COLORS';
import { postPictureForUserService_profile, updateUser } from '@/api/user.api';
import { setUser } from '@/store/user.store';
const { TextArea } = Input;

const normFile = (e) => {
    if (Array.isArray(e)) {
        return e;
    }
    return e?.fileList;
};

export default function ProfileCard() {
    const formref = useRef(null);
    const { user } = useSelector((state) => state.user)
    const { user_id, username, profile_picture, phone, address } = user
    const [isEditModalOpen, setIsEditModalOpen] = useState(false);
    const dispatch = useDispatch()
    const [updatedAvator, setUpdatedAvator] = useState(profile_picture ? [{ uid: 0, name: 'avatar', status: 'done', url: profile_picture, thumbUrl: profile_picture }] : [])
    // const [updatedAvator, setUpdatedAvator] = useState([])
    const propsImage = {
        onRemove: (file) => {
            const index = updatedAvator.indexOf(file);
            const newFileList = updatedAvator.slice();
            newFileList.splice(index, 1);
            setUpdatedAvator(newFileList);
        },
        beforeUpload: (file) => {
            const isImage = file.type?.startsWith('image')
            if (isImage) {
                updatedAvator.push({ ...file, name: file.name })
                setUpdatedAvator(updatedAvator)
            } else {
                message.error("Should Be a Picture")
                return false
            }
        },
        fileList: updatedAvator,
    };
    const submitImageToFirebase = async ({ file }) => {
        if (file) {
            const formData = new FormData();
            formData.append('image', file);
            await postPictureForUserService_profile(formData).then(res => {
                if (res.status) {
                    message.success('Uploaded successfully')
                    setUpdatedAvator([{ ...file, status: 'done', url: res.value, thumbUrl: res.value, name: file.name }])
                } else {
                    message.error('Upload failure')
                    setUpdatedAvator([{ ...file, status: 'error' }])
                }
            })
        } else {
            message.error('Some error happens')
            setUpdatedAvator([{ ...file, status: 'error' }])
        }
    }
    const onFinish = async (items) => {
        let handledItems = { ...items, profile_picture: updatedAvator[0]?.url, action: 'update' }
        let updateInfo = Object.keys(handledItems)
            .filter((key) => handledItems[key] != null)
            .reduce((a, key) => ({ ...a, [key]: handledItems[key] }), {});
        try {
            await updateUser(user_id, { ...user, ...updateInfo })
                .then((res) => {
                    if (res.status) {
                        dispatch(setUser(res.value))
                        formref.current.setFieldsValue(res.value);
                        setIsEditModalOpen(false)
                        message.success("Update successfully")
                    } else {
                        message.error(res.message)
                    }
                })
        } catch (error) {
            console.log(error);
            message.error("Error")
        }
    }
    const onFinishFailed = (errorInfo) => { message.error("Error: ", errorInfo) }
    return (
        <>
            <div style={{ marginTop: 60 }} className='profileCard'>
                <div style={{ display: 'flex' }}>
                    <div className='Card-Avatar'>
                        <Avatar size={80} icon={<UserOutlined />} src={user?.profile_picture ? user.profile_picture : ''} />
                    </div>
                    <div className='Card-UserInfo'>
                        <div className='Card-Username'><h1 style={{ color: COLORS.primary }}>{username}</h1></div>
                    </div>
                </div>
                <div className='Card-Edit'>
                    <Button onClick={() => setIsEditModalOpen(true)}><EditOutlined />&nbsp;&nbsp;{"Edit Profile"}</Button>
                </div>

                <Modal title={"Profile"} open={isEditModalOpen} onOk={() => setIsEditModalOpen(false)} onCancel={() => setIsEditModalOpen(false)} okText="Update" cancelText="Cancel" footer={null} width={600}>
                    <Form labelCol={{ span: 6, }} wrapperCol={{ span: 14, }} layout="horizontal" style={{ width: 600 }} onFinish={onFinish} onFinishFailed={onFinishFailed}>
                        <Form.Item name="username" label={"User Name"}>
                            <Input defaultValue={username} />
                        </Form.Item>
                        <Form.Item name="phone" label={"Phone Number"}>
                            <Input defaultValue={phone} />
                        </Form.Item>
                        <Form.Item name="address" label={'Address'}>
                            <TextArea defaultValue={address} rows={2} />
                        </Form.Item>
                        <Form.Item label={"Avator"} valuePropName="fileList" getValueFromEvent={normFile}>
                            <Upload listType="picture" customRequest={submitImageToFirebase} maxCount={1} {...propsImage}>
                                <Button icon={<UploadOutlined />}>Upload Avatar</Button>
                            </Upload>
                        </Form.Item>
                        <Button style={{ marginLeft: 400 }} type="primary" htmlType="submit">
                            Update
                        </Button>
                    </Form>
                </Modal>
            </div >
            <div style={{ marginTop: 50, pointerEvents: "none" }}>
                <Form ref={formref} labelCol={{ span: 10, }} wrapperCol={{ offset: 2, span: 14, }} variant="filled" layout="horizontal" style={{ width: 600 }} onFinish={onFinish} onFinishFailed={onFinishFailed}>
                    <Form.Item name="username" label={"User Name"}>
                        <Input defaultValue={username} />
                    </Form.Item>
                    <Form.Item name="address" label={'Address'}>
                        <TextArea defaultValue={address} rows={2} />
                    </Form.Item>
                    <Form.Item name="phone" label={"Phone Number"}>
                        <Input defaultValue={phone} />
                    </Form.Item>
                </Form>
            </div>
        </>
    )
}
