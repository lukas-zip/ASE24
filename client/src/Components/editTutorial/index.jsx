import { Button, Form, Input, InputNumber, Radio, Select, Switch, Upload, message } from 'antd'
import { UploadOutlined } from '@ant-design/icons';
import CardTitle from '../CardTitle';
// import { ref, uploadBytesResumable, getDownloadURL } from "firebase/storage";
// import { storage } from '../../firebase'
import { useRef, useState } from 'react';
import CONSTANTS from '../../constants';
import { useSelector } from 'react-redux';
import { updateProductForCompany, uploadProductPicture } from '../../api/user.api';

export default function EditProductModal({ getData, selectedProduct, removeTab }) {
    const { user: { shop_id } } = useSelector(state => state.user)
    const [uploading, setUploading] = useState(false)
    const editFormRef = useRef(null);
    const originCover = selectedProduct.product_picture.map((item, key) => ({
        uid: key,
        name: 'Product Picture ' + key,
        status: 'done',
        url: item,
        thumbUrl: item,
    }))
    const [productImages, setProductImages] = useState(originCover)
    const propsCover = {
        onRemove: (file) => {
            const index = productImages.indexOf(file);
            const newFileList = productImages.slice();
            newFileList.splice(index, 1);
            setProductImages(newFileList);
        },
        beforeUpload: (file) => {
            const isImage = file.type?.startsWith('image')
            if (isImage) {
                const isSupportedImageType = ['image/jpeg', 'image/png', 'image/gif', 'image/webp'].includes(file.type);
                if (!isSupportedImageType) {
                    message.error('Unsupported file format. Please upload a JPEG, PNG, GIF, or WEBP image.');
                    return false; // 阻止上传
                } else {
                    productImages.push({ ...file, name: file.name })
                    setProductImages(productImages)
                }
            } else {
                message.error('u only can upload picture here')
                return false
            }
        },
        fileList: productImages,
    };
    const submitCoverToFirebase = async ({ file }) => {
        setUploading(true)
        if (file) {
            const formData = new FormData();
            formData.append('image', file);
            await uploadProductPicture(formData).then(res => {
                if (res.status) {
                    message.success('Uploaded successfully')
                    const handledProductImages = productImages.map(item => {
                        if (item.uid === file.uid) {
                            return { ...file, status: 'done', url: res.value, thumbUrl: res.value, name: file.name }
                        }
                        return item
                    })
                    console.log(productImages);
                    setProductImages(handledProductImages)
                    setUploading(false)
                } else {
                    message.err('Upload failure')
                    const handledProductImages = productImages.map(item => {
                        if (item.uid === file.uid) {
                            return { ...file, status: 'error' }
                        }
                        return item
                    })
                    setProductImages(handledProductImages)
                    setUploading(false)
                }
            })
        } else {
            message.err('Some error happens')
            const handledProductImages = productImages.map(item => {
                if (item.uid === file.uid) {
                    return { ...file, status: 'error' }
                }
                return item
            })
            setProductImages(handledProductImages)
            setUploading(false)
        }
    }
    const onFinish = async (items) => {
        const imgUrl = productImages.map(item => item.url)
        const reqData = {
            ...items, product_owner: shop_id, product_sale: items.product_sale || true, product_picture: imgUrl,
        }
        console.log('req', reqData);

        try {
            await updateProductForCompany(selectedProduct.product_id, reqData).then(res => {
                if (res.status) {
                    message.success('Update successfully')
                    removeTab(`edit${selectedProduct.product_id}`)
                    getData()
                } else {
                    message.error(res.message)
                }
            })
        } catch (error) {
            console.log(error);
            message.error('error')
        }
    };
    const onFinishFailed = (errorInfo) => {
        message.error('Failed:', errorInfo)
    };
    const normFile = (e) => {
        if (Array.isArray(e)) {
            return e;
        }
        return e?.fileList;
    };
    const options = [];
    return (
        <div>
            <CardTitle title={`Edit Product: ${selectedProduct.product_name}`} />
            <Form name="basic" ref={editFormRef} labelCol={{ span: 14, }} wrapperCol={{ span: 16, }} style={{ maxWidth: 600, }} initialValues={selectedProduct} onFinish={onFinish} onFinishFailed={onFinishFailed} autoComplete="off">
                <Form.Item label="Category" name="product_category" rules={[{ required: true, message: 'Please select category!', }]}>
                    <Select mode="multiple" allowClear>
                        {Object.values(CONSTANTS.CATEGORIES).map((item, index) => <Select.Option key={index} value={item}>{item}</Select.Option>)}
                    </Select>
                </Form.Item>
                {/* <Form.Item label="BOM" name="product_bom" rules={[{ required: true, message: 'Please select bom!', }]}>
                    <Select mode="multiple" allowClear>
                        {Object.values(CONSTANTS.CATEGORIES).map((item, index) => <Select.Option key={index} value={item}>{item}</Select.Option>)}
                    </Select>
                </Form.Item> */}
                <Form.Item label="Assembly" name="product_assemblies" rules={[{ required: true, message: 'Please select assembly!', }]}>
                    <Radio.Group>
                        <Radio value="Final"> Final </Radio>
                        <Radio value="Secondary"> Secondary </Radio>
                    </Radio.Group>
                </Form.Item>
                <Form.Item label="Sale" name="product_sale">
                    <Switch />
                </Form.Item>
                <Form.Item label="Search Attributes" name="product_search_attributes" rules={[{ required: true, message: 'Please select attributes!', }]}>
                    <Select mode="tags" allowClear options={options}>
                        {Object.values(CONSTANTS.CATEGORIES).map((item, index) => <Select.Option key={index} value={item}>{item}</Select.Option>)}
                    </Select>
                </Form.Item>
                <Form.Item label="name" name="product_name" rules={[{ required: true }]}>
                    <Input />
                </Form.Item>
                <Form.Item label="description" name="product_description" rules={[{ required: true, message: 'Please input product description!', }]}>
                    <Input />
                </Form.Item>
                <Form.Item label="Current stock" name="product_current_stock" rules={[{ required: true, message: 'Please input product_current_stock!', }]}>
                    <InputNumber min={0} />
                </Form.Item>
                <Form.Item label="Should stock" name="product_should_stock" rules={[{ required: true, message: 'Please input product_should_stock!', }]}>
                    <InputNumber min={0} />
                </Form.Item>
                <Form.Item label="Price(CHF)" name="product_price" rules={[{ required: true, message: 'Please input product_price!', }]}>
                    <InputNumber min={0} step="0.01" />
                </Form.Item>
                <Form.Item label="Reduction(%)" name="product_price_reduction" rules={[{ required: true, message: 'Please input product_price_reduction!', }]}>
                    <InputNumber min={0} />
                </Form.Item>
                <Form.Item label="Cover" rules={[{ required: false, message: 'Please input cover!', }]} getValueFromEvent={normFile}>
                    <Upload listType="picture" customRequest={submitCoverToFirebase} maxCount={1} {...propsCover}>
                        <Button icon={<UploadOutlined />}>Click to upload</Button>
                    </Upload>
                </Form.Item>
                <Form.Item wrapperCol={{ offset: 8, span: 16 }}>
                    <Button type="primary" htmlType="submit" disabled={uploading ? true : false}>Upload</Button>
                </Form.Item>
            </Form>
        </div >
    )
}
