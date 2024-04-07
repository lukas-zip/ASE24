import { Button, Form, Input, InputNumber, Radio, Select, Switch, Upload, message } from 'antd'
import { UploadOutlined } from '@ant-design/icons';
import CardTitle from '../CardTitle';
// import { ref, uploadBytesResumable, getDownloadURL } from "firebase/storage";
// import { storage } from '../../firebase'
import { useRef, useState } from 'react';
import CONSTANTS from '../../constants';
import { addProductForCompany } from '../../api/user.api';
import { useSelector } from 'react-redux';

export default function UploadTutorialModal({ getData, removeTab }) {
    const { user: { shop_id } } = useSelector(state => state.user)
    const [uploading, setUploading] = useState(false)
    const formRef = useRef(null);
    const [cover, setCover] = useState([])
    const [imageFile, setImageFile] = useState()
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
                setImageFile(file)
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
        const formData = new FormData();
        formData.append('image', imageFile);
        formData.append('product_owner', shop_id);
        formData.append('product_bom', [""]);

        for (const key in items) {
            formData.append(key, items[key]);
        }
        console.log('formData', formData);
        // const handledItems = { ...items, image: formData }
        // console.log('gaiguode', handledItems);

        try {
            await addProductForCompany(formData).then(res => {
                if (res.status) {
                    getData()
                    removeTab('upload')
                    clear()
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
        console.log(errorInfo);
        message.error('Failed:', errorInfo)
    };
    const normFile = (e) => {
        console.log('Upload event:', e);
        if (Array.isArray(e)) {
            return e;
        }
        return e?.fileList;
    };
    const clear = () => {
        formRef.current?.resetFields();
        setCover([])
    };

    const addProduct = {
        // product_owner: "1324a686-c8b1-4c84-bbd6-17325209d78c6",
        // product_name: "exampleadditionProduct",
        // product_description: "exampleDescription",
        // product_current_stock: 0,
        // product_should_stock: 0,
        // product_price: 0.00,
        // product_price_reduction: 0.00,
        product_sale: false,
        // product_category: ["accessories"],
        // product_search_attributes: ["black", "curled"],
        // product_reviews: [],
        product_bom: [
            "1324a686-c8b1-4c84-bbd6-17325209d78c1",
            "1324a686-c8b1-4c84-bbd6-17325209d78c2"
        ],
        product_assemblies: "Final"
    }
    const options = [];
    const handleChange = (value) => {
        console.log(value);
    };
    return (
        <div>
            <CardTitle title={'Upload Product'} />
            <Form name="basic" ref={formRef} labelCol={{ span: 14, }} wrapperCol={{ span: 16, }} style={{ maxWidth: 600, }} initialValues={{ remember: true, }} onFinish={onFinish} onFinishFailed={onFinishFailed} autoComplete="off">
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
                <Form.Item label="Sale" name="product_sale" valuePropName='checked'>
                    <Switch />
                </Form.Item>
                <Form.Item label="Search Attributes" name="product_search_attributes" rules={[{ required: true, message: 'Please select attributes!', }]}>
                    <Select mode="tags" allowClear onChange={handleChange} options={options}>
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
                <Form.Item label="Cover" name="cover" rules={[{ required: true, message: 'Please input cover!', }]} getValueFromEvent={normFile}>
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
