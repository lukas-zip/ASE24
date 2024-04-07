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
const { TextArea } = Input;

const normFile = (e) => {
    if (Array.isArray(e)) {
        return e;
    }
    return e?.fileList;
};

export default function ProfileCard() {
    const { user } = useSelector((state) => state.user)
    const { profile_picture, phone, address } = user
    const username = user.type === CONSTANTS.USER_TYPE.USER ? user.username : user.shop_name
    const [isEditModalOpen, setIsEditModalOpen] = useState(false);
    const dispatch = useDispatch()
    const showEditModal = () => { setIsEditModalOpen(true); };
    const handleEditOk = () => { setIsEditModalOpen(false); };
    const handleCancel = () => { setIsEditModalOpen(false); };
    const [updatedAvator, setUpdatedAvator] = useState([{ uid: 0, name: 'avatar', status: 'done', url: profile_picture, thumbUrl: profile_picture }])
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
    const submitImageToFirebase = ({ file }) => {
        // if (file) {
        //     const storageRef = ref(storage, `${name}-avator-${parseInt((new Date().getTime() / 1000).toString())}`);
        //     const uploadTask = uploadBytesResumable(storageRef, file);
        //     uploadTask.on('state_changed', (snapshot) => {
        //         const progress = (snapshot.bytesTransferred / snapshot.totalBytes) * 100;
        //         const handledBlogImgs = updatedAvator.map(item => {
        //             if (item.uid === file.uid) {
        //                 return { ...file, status: 'uploading', percent: progress }
        //             }
        //             return item
        //         })
        //         setUpdatedAvator(handledBlogImgs)
        //         switch (snapshot.state) {
        //             case 'paused':
        //                 console.log('Upload is paused');
        //                 break;
        //             case 'running':
        //                 console.log('Upload is running', progress);
        //                 break;
        //         }
        //     },
        //         (error) => {
        //             message.err(intl.formatMessage({ id: 'error.errorHappens' }))
        //             updatedAvator.map(item => {
        //                 if (item.uid === file.uid) {
        //                     return { ...file, status: 'error' }
        //                 }
        //                 return item
        //             })
        //             setUpdatedAvator(updatedAvator)
        //         },
        //         () => {
        //             getDownloadURL(uploadTask.snapshot.ref).then((downloadURL) => {
        //                 const handledBlogImgs = updatedAvator.map(item => {
        //                     if (item.uid === file.uid) {
        //                         return { ...file, status: 'done', url: downloadURL, thumbUrl: downloadURL, name: file.name }
        //                     }
        //                     return item
        //                 })
        //                 setUpdatedAvator(handledBlogImgs)
        //             });
        //         }
        //     );
        // } else {
        //     message.err(intl.formatMessage({ id: 'error.errorHappens' }))
        //     updatedAvator.map(item => {
        //         if (item.uid === file.uid) {
        //             return item = { ...file, status: 'error' }
        //         }
        //         return item
        //     })
        //     setUpdatedAvator(updatedAvator)
        // }
    }
    const onFinish = async (items) => {
        // let handledItems = { ...items, avator: updatedAvator[0].url }
        // let updateInfo = Object.keys(handledItems)
        //     .filter((key) => handledItems[key] != null)
        //     .reduce((a, key) => ({ ...a, [key]: handledItems[key] }), {});
        // try {
        //     await updateuserinfo(user._id, updateInfo)
        //         .then((updatedUser) => {
        //             dispatch(loginSuccess(updatedUser))
        //             handleEditOk()
        //             message.success(intl.formatMessage({ id: 'app.prf.updated' }))
        //         })
        // } catch (error) {
        //     console.log(error);
        //     message.error(intl.formatMessage({ id: 'error.default' }))
        // }
    }
    const onFinishFailed = (errorInfo) => { message.error("Error: ", errorInfo) }
    return (
        <>
            <div style={{ marginTop: 60 }} className='profileCard'>
                <div style={{ display: 'flex' }}>
                    <div className='Card-Avatar'>
                        <Avatar size={80} icon={<UserOutlined />} src={user?.avator ? user.avator : ''} />
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
                        {/* <Form.Item name="gender" label={intl.formatMessage({ id: 'app.prf.label.gender' })}>
                        <Radio.Group defaultValue={gender}>
                            <Radio value="Male"> {intl.formatMessage({ id: 'app.prf.edit.gender.Male' })} </Radio>
                            <Radio value="Female"> {intl.formatMessage({ id: 'app.prf.edit.gender.Female' })} </Radio>
                        </Radio.Group>
                    </Form.Item> */}
                        <Form.Item name="name" label={"User Name"}>
                            <Input defaultValue={username} />
                        </Form.Item>
                        {/* <Form.Item name="age" label={intl.formatMessage({ id: 'app.prf.label.age' })} >
                        <InputNumber defaultValue={age} />
                    </Form.Item> */}
                        {/* <Form.Item name="personalStatus" label={intl.formatMessage({ id: 'app.prf.label.bio' })}>
                        <TextArea defaultValue={personalStatus} rows={2} />
                    </Form.Item> */}
                        {/* <Form.Item name="preferedTheme" label={intl.formatMessage({ id: 'app.prf.label.theme' })}>
                        <Select defaultValue={preferedTheme}>
                            <Select.Option value="dark">{intl.formatMessage({ id: 'app.prf.edit.theme.dark' })}</Select.Option>
                            <Select.Option value="light">{intl.formatMessage({ id: 'app.prf.edit.theme.light' })}</Select.Option>
                        </Select>
                    </Form.Item> */}
                        {/* <Form.Item name="preferedLanguage" label={intl.formatMessage({ id: 'app.prf.label.lang' })}> */}
                        {/* <Select defaultValue={preferedLanguage}> */}
                        {/* <Select.Option value="en_US">English</Select.Option> */}
                        {/* <Select.Option value="zh_CN">中文</Select.Option> */}
                        {/* </Select> */}
                        {/* </Form.Item> */}
                        <Form.Item name="hpNum" label={"Phone Number"}>
                            <Input defaultValue={phone} />
                        </Form.Item>
                        {/* <Form.Item name="birthday" label={intl.formatMessage({ id: 'app.prf.label.birthday' })}> */}
                        {/* {birthday ? <DatePicker defaultValue={dayjs(birthday, 'YYYY-MM-DD')} /> : <DatePicker />} */}
                        {/* </Form.Item> */}
                        <Form.Item label={"Avator"} valuePropName="fileList" getValueFromEvent={normFile}>
                            <Upload name="image" listType="picture" customRequest={submitImageToFirebase} maxCount={1} {...propsImage}>
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
                <Form labelCol={{ span: 10, }} wrapperCol={{ offset: 2, span: 14, }} variant="filled" layout="horizontal" style={{ width: 600 }} onFinish={onFinish} onFinishFailed={onFinishFailed}>
                    <Form.Item name="name" label={"User Name"}>
                        <Input defaultValue={username} />
                    </Form.Item>
                    <Form.Item name="Address" label={'Address'}>
                        <TextArea defaultValue={address} rows={2} />
                    </Form.Item>
                    <Form.Item name="hpNum" label={"Phone Number"}>
                        <Input defaultValue={phone} />
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
