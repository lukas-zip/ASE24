import { Button, Form, Input, InputNumber, Radio, Select, Switch, Upload, message } from 'antd'
import { UploadOutlined } from '@ant-design/icons';
import CardTitle from '../CardTitle';
// import { ref, uploadBytesResumable, getDownloadURL } from "firebase/storage";
// import { storage } from '../../firebase'
import { useRef, useState } from 'react';
import CONSTANTS from '../../constants';
// import { createTutorial, updateTutorial } from '../../api/tutorial.api'
// import EXERCISETYPE from '../../constants/EXERCISETYPE';

const equipmentsOptions = [
    { value: 'yaling', label: 'yaling' },
    { value: '跳绳', label: '跳绳' },
]

export default function EditProductModal({ getData, selectedProduct, removeTab }) {
    const [uploading, setUploading] = useState(false)
    const editFormRef = useRef(null);
    const [cover, setCover] = useState([])
    const propsCover = {
        onRemove: (file) => {
            const index = cover.indexOf(file);
            const newFileList = cover.slice();
            newFileList.splice(index, 1);
            setCover(newFileList);
        },
        beforeUpload: (file) => {
            const isImage = file.type?.startsWith('image')
            if (isImage) {
                setCover([{ ...file, name: file.name }])
            } else {
                message.error('u only can upload picture here')
                return false
            }
        },
        fileList: cover,
    };
    const submitCoverToFirebase = ({ file }) => {
        // setUploading(true)
        // if (file) {
        //     const storageRef = ref(storage, `Tutorial-Cover-${parseInt((new Date().getTime() / 1000).toString())}`);
        //     const uploadTask = uploadBytesResumable(storageRef, file);
        //     uploadTask.on('state_changed',
        //         (snapshot) => {
        //             const progress = (snapshot.bytesTransferred / snapshot.totalBytes) * 100;
        //             setCover([{ ...file, status: 'uploading', percent: progress }])
        //             switch (snapshot.state) {
        //                 case 'paused':
        //                     console.log('Upload is paused');
        //                     break;
        //                 case 'running':
        //                     console.log('Upload is running');
        //                     break;
        //             }
        //         },
        //         (error) => {
        //             message.err('Some error happens')
        //             setCover([{ ...file, status: 'error' }])
        //             setUploading(false)
        //         },
        //         () => {
        //             // For instance, get the download URL: https://firebasestorage.googleapis.com/...
        //             getDownloadURL(uploadTask.snapshot.ref).then((downloadURL) => {
        //                 setCover([{ ...file, status: 'done', url: downloadURL, thumbUrl: downloadURL, name: file.name }])
        //             });
        //             setUploading(false)
        //         }
        //     );
        // } else {
        //     message.err('Some error happens')
        //     setCover([{ ...file, status: 'error' }])
        //     setUploading(false)
        // }
    }
    const onFinish = async (items) => {
        const handledItems = { ...items, cover: cover[0].url, video: video[0].url }
        try {
            const res = await updateTutorial(selectedProduct._id, handledItems)
            console.log(res);
            message.success('Update successfully')
            removeTab(`edit${selectedProduct._id}`)
            getData()
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
                <Form.Item label="Cover" name="cover" rules={[{ required: false, message: 'Please input cover!', }]} getValueFromEvent={normFile}>
                    <Upload name="cover" listType="picture" customRequest={submitCoverToFirebase} maxCount={1} {...propsCover}>
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
