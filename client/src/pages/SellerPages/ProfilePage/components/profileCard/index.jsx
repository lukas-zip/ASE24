import { Avatar, Button, Modal, DatePicker, Form, Input, InputNumber, Radio, Select, message, Upload, Carousel } from 'antd'
import { UserOutlined, EditOutlined, UploadOutlined } from '@ant-design/icons';
import React, { useEffect, useState } from 'react'
import './index.less'
import { useDispatch } from 'react-redux'
import { useSelector } from 'react-redux'
import COLORS from '@/constants/COLORS';
import CONSTANTS from '../../../../../constants';
import { postPictureForUserService_profile, postPictureForUserService_shoppictures, updateShop } from '../../../../../api/user.api';
import { setUser } from '../../../../../store/user.store';
import MyCarouselDisplay from '@/Components/MyCarouselCard';
const { TextArea } = Input;

const normFile = (e) => {
    if (Array.isArray(e)) {
        return e;
    }
    return e?.fileList;
};

export default function ProfileCard() {
    const formref = React.useRef();
    const { user } = useSelector((state) => state.user)
    const { profile_picture, phone, address, email, description, shop_pictures } = user
    const username = user.type === CONSTANTS.USER_TYPE.USER ? user.username : user.shop_name
    const [isEditModalOpen, setIsEditModalOpen] = useState(false);
    const dispatch = useDispatch()
    const [updatedAvator, setUpdatedAvator] = useState(profile_picture ? [{ uid: 0, name: 'avatar', status: 'done', url: profile_picture, thumbUrl: profile_picture }] : [])
    const items = shop_pictures.length !== 0 ? shop_pictures.map((item, key) => ({ uid: key, name: `Shop picture ${key}`, status: 'done', url: item, thumbUrl: item }))
        : []
    const [updatedShopPictures, setUpdatedShopPictures] = useState(items)
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
    const propsPictureImage = {
        onRemove: (file) => {
            const index = updatedShopPictures.indexOf(file);
            const newFileList = updatedShopPictures.slice();
            newFileList.splice(index, 1);
            setUpdatedShopPictures(newFileList);
        },
        beforeUpload: (file) => {
            const isImage = file.type?.startsWith('image')
            if (isImage) {
                const isSupportedImageType = ['image/jpeg', 'image/png', 'image/gif', 'image/webp'].includes(file.type);
                if (!isSupportedImageType) {
                    message.error('Unsupported file format. Please upload a JPEG, PNG, GIF, or WEBP image.');
                    return false; // 阻止上传
                } else {
                    updatedShopPictures.push({ ...file, name: file.name })
                    setUpdatedShopPictures(updatedShopPictures)
                }
            } else {
                message.error('u only can upload picture here')
                return false
            }
        },
        fileList: updatedShopPictures,
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
    const submitShopPictures = async ({ file }) => {
        if (file) {
            const formData = new FormData();
            formData.append('image', file);
            await postPictureForUserService_shoppictures(formData).then(res => {
                if (res.status) {
                    message.success('Uploaded successfully')
                    const handledShopPictures = updatedShopPictures.map(item => {
                        if (item.uid === file.uid) {
                            return { ...file, status: 'done', url: res.value, thumbUrl: res.value, name: file.name + Math.random(1000) }
                        }
                        return item
                    })
                    setUpdatedShopPictures(handledShopPictures)
                } else {
                    const handledShopPictures = updatedShopPictures.map(item => {
                        if (item.uid === file.uid) {
                            return { ...file, status: 'error' }
                        }
                        return item
                    })
                    message.error('Upload failure')
                    setUpdatedShopPictures(handledShopPictures)
                }
            })
        } else {
            const handledShopPictures = updatedShopPictures.map(item => {
                if (item.uid === file.uid) {
                    return { ...file, status: 'error' }
                }
                return item
            })
            message.error('Upload failure')
            setUpdatedShopPictures(handledShopPictures)
        }
    }
    const onFinish = async (items) => {
        let handledItems = { ...items, profile_picture: updatedAvator[0]?.url, shop_pictures: updatedShopPictures.map(item => item.url) }
        let updateInfo = Object.keys(handledItems)
            .filter((key) => handledItems[key] != null)
            .reduce((a, key) => ({ ...a, [key]: handledItems[key] }), {});
        console.log(updateInfo);
        try {
            await updateShop(user.shop_id, { ...user, ...updateInfo })
                .then((res) => {
                    if (res.status) {
                        dispatch(setUser(res.value))
                        formref.current.setFieldsValue(res.value);
                        setIsEditModalOpen(false);
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
            <div style={{}} className='profileCard'>
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
                            <TextArea defaultValue={description} rows={2} />
                        </Form.Item>
                        <Form.Item label={"Profile Picture"} key={"Profile Picture"} getValueFromEvent={normFile}>
                            <Upload listType="picture" customRequest={submitImageToFirebase} maxCount={1} {...propsImage}>
                                <Button icon={<UploadOutlined />}>Upload Avatar</Button>
                            </Upload>
                        </Form.Item>
                        <Form.Item label={"Shop Pictures"} key={"Shop pictures"} getValueFromEvent={normFile}>
                            <Upload listType="picture" customRequest={submitShopPictures} maxCount={10} {...propsPictureImage}>
                                <Button icon={<UploadOutlined />}>Upload Shop Pictures</Button>
                            </Upload>
                        </Form.Item>
                        <Button style={{ marginLeft: 400 }} type="primary" htmlType="submit">
                            Update
                        </Button>
                    </Form>
                </Modal>
            </div >
            <div style={{}}>
                <div style={{ pointerEvents: "none", margin: "20px 0" }}>
                    <Form ref={formref} labelCol={{ span: 10, }} wrapperCol={{ offset: 2, span: 14, }} initialValues={user} variant="filled" layout="horizontal" style={{ width: 600 }} onFinish={onFinish} onFinishFailed={onFinishFailed}>
                        <Form.Item name="shop_name" label={"Username"}>
                            <Input defaultValue={username} />
                        </Form.Item>
                        <Form.Item name="address" label={'Address'}>
                            <TextArea defaultValue={address} rows={2} />
                        </Form.Item>
                        <Form.Item name="description" label={'Description'}>
                            <TextArea defaultValue={description} rows={2} />
                        </Form.Item>
                        <Form.Item name="phone" label={"Phone"}>
                            <Input defaultValue={phone} />
                        </Form.Item>
                        <Form.Item name="email" label={"email"}>
                            <Input defaultValue={email} />
                        </Form.Item>
                    </Form>
                </div>
                {shop_pictures.length !== 0 && <MyCarouselDisplay pictures={shop_pictures} />}
            </div>
        </>
    )
}
