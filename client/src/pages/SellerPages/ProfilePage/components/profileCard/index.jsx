import { Avatar, Button, Modal, DatePicker, Form, Input, InputNumber, Radio, Select, message, Upload } from 'antd'
import { UserOutlined, EditOutlined, UploadOutlined } from '@ant-design/icons';
import React, { useState } from 'react'
import './index.less'
// import { storage } from '../../../../firebase'
// import { ref, uploadBytesResumable, getDownloadURL } from "firebase/storage";
// import { loginSuccess } from '../../../../redux/userSlice'
import { useDispatch } from 'react-redux'
import { useSelector } from 'react-redux'
import COLORS from '@/constants/COLORS';
import CONSTANTS from '../../../../../constants';
import { postPictureForUserService_profile, updateShop } from '../../../../../api/user.api';
import { setUser } from '../../../../../store/user.store';
const { TextArea } = Input;

const normFile = (e) => {
    if (Array.isArray(e)) {
        return e;
    }
    return e?.fileList;
};
const updateUser = {
    address: "update 18, Bern",
    description: "I´m selling update goods.",
    email: "update@example.com",
    phone: "324314332414",
    profile_picture: "NONE",
    shop_id: "2c1f74e3-33f0-47a2-97e5-ad4cc5953ed3",
    shop_name: "update Hydro",
    type: "Shop"
}

export default function ProfileCard() {
    const formref = React.useRef();
    const { user } = useSelector((state) => state.user)
    const { profile_picture, phone, address, email } = user
    const username = user.type === CONSTANTS.USER_TYPE.USER ? user.username : user.shop_name
    const [isEditModalOpen, setIsEditModalOpen] = useState(false);
    const dispatch = useDispatch()
    const showEditModal = () => { setIsEditModalOpen(true); };
    const handleEditOk = () => { setIsEditModalOpen(false); };
    const handleCancel = () => { setIsEditModalOpen(false); };
    const [updatedAvator, setUpdatedAvator] = useState(profile_picture ? [{ uid: 0, name: 'avatar', status: 'done', url: profile_picture, thumbUrl: profile_picture }] : [])
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
        let handledItems = { ...items, profile_picture: updatedAvator[0]?.url }
        let updateInfo = Object.keys(handledItems)
            .filter((key) => handledItems[key] != null)
            .reduce((a, key) => ({ ...a, [key]: handledItems[key] }), {});
        try {
            await updateShop(user.shop_id, { ...user, ...updateInfo })
                .then((res) => {
                    if (res.status) {
                        dispatch(setUser(res.value))
                        formref.current.setFieldsValue(res.value);
                        handleEditOk()
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
                    <Button onClick={showEditModal}><EditOutlined />&nbsp;&nbsp;{"Edit Profile"}</Button>
                </div>

                <Modal title={"Profile"} open={isEditModalOpen} onOk={handleEditOk} onCancel={handleCancel} okText="Update" cancelText="Cancel" footer={null} width={600}>
                    <Form labelCol={{ span: 6, }} wrapperCol={{ span: 14, }} layout="horizontal" style={{ width: 600 }} onFinish={onFinish} onFinishFailed={onFinishFailed}>
                        <Form.Item name="shop_name" label={"Shop Name"}>
                            <Input defaultValue={username} />
                        </Form.Item>
                        <Form.Item name="phone" label={"Phone"}>
                            <Input defaultValue={phone} />
                        </Form.Item>
                        <Form.Item name="address" label={'Address'}>
                            <TextArea defaultValue={address} rows={2} />
                        </Form.Item>
                        <Form.Item name="description" label={'Description'}>
                            <TextArea defaultValue={user.description} rows={2} />
                        </Form.Item>
                        <Form.Item label={"profile_picture"} valuePropName="fileList" getValueFromEvent={normFile}>
                            <Upload name="profile_picture" listType="picture" customRequest={submitImageToFirebase} maxCount={1} {...propsImage}>
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
                <Form ref={formref} labelCol={{ span: 10, }} wrapperCol={{ offset: 2, span: 14, }} initialValues={user} variant="filled" layout="horizontal" style={{ width: 600 }} onFinish={onFinish} onFinishFailed={onFinishFailed}>
                    <Form.Item name="shop_name" label={"Username"}>
                        <Input defaultValue={username} />
                    </Form.Item>
                    <Form.Item name="address" label={'Address'}>
                        <TextArea defaultValue={address} rows={2} />
                    </Form.Item>
                    <Form.Item name="description" label={'Description'}>
                        <TextArea defaultValue={user.description} rows={2} />
                    </Form.Item>
                    <Form.Item name="phone" label={"Phone"}>
                        <Input defaultValue={phone} />
                    </Form.Item>
                    <Form.Item name="email" label={"email"}>
                        <Input defaultValue={email} />
                    </Form.Item>
                    {/* <Form.Item name="birthday" label={intl.formatMessage({ id: 'app.prf.label.birthday' })}> */}
                    {/* {birthday ? <DatePicker defaultValue={dayjs(birthday, 'YYYY-MM-DD')} /> : <DatePicker />} */}
                    {/* </Form.Item> */}
                    {/* <Form.Item label={"Avator"} valuePropName="fileList" getValueFromEvent={normFile}>
                        <Upload name="image" listType="picture" customRequest={submitImageToFirebase} maxCount={1} {...propsImage}>
                            <Button icon={<UploadOutlined />}>Upload Avatar</Button>
                        </Upload>
                    </Form.Item> */}
                </Form>
            </div>
        </>
    )
}
