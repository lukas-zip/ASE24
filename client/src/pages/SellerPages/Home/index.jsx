import React, { useEffect, useState } from 'react'
import './index.less'
import { Button, Card, Divider, Empty, Flex, Modal, Popconfirm, Space, Tabs, message } from 'antd'
import Meta from 'antd/es/card/Meta'
import { DeleteOutlined, EditOutlined, SettingOutlined, UploadOutlined } from '@ant-design/icons'
import { deleteProductFromCompany, getAllProductsByShopId } from '../../../api/user.api'
import { useSelector } from 'react-redux'
import UploadProductModal from '../../../Components/uploadTutorial'
import EditProductModal from '../../../Components/editTutorial'
import Overview from './components/overview'

const cardWidth = 230
const cardHeight = 220
function index() {
    const { user: { shop_id } } = useSelector(state => state.user)
    const [allProducts, setAllProducts] = useState([])
    const getAllProducts = async () => {
        await getAllProductsByShopId(shop_id).then(res => {
            if (res.status) {
                setAllProducts(res.value)
            } else {
                message.error(res.message)
            }
        }).catch(err => {
            message.error("Error")
        })
    }
    useEffect(() => {
        getAllProducts()
    }, [])
    const handleDeleteProduct = async (productId) => {
        await deleteProductFromCompany(productId).then(res => {
            if (res.status) {
                message.success("Product deleted successfully")
                getAllProducts()
            } else {
                message.error(res.message)
            }
        })
    }


    const [selectedProduct_id, setSelectedProductId] = useState("")
    const [updateProductModalVisible, setUpdateProductModalVisible] = useState(false)
    const updateProduct = async (product_id) => {

    }

    //tabs
    const initialItems = [{ label: 'Home', key: 'home', closable: false }]
    const [activeKey, setActiveKey] = useState(initialItems[0].key);
    const [items, setItems] = useState(initialItems);
    const addUploadTab = () => {
        const newActiveKey = 'upload';
        const alreadyHave = items.find(tab => tab.key === newActiveKey)
        if (!alreadyHave) {
            const newPanes = [...items];
            newPanes.push({
                label: 'Add Product',
                key: newActiveKey,
                children: <UploadProductModal getData={getAllProducts} removeTab={remove} />
            });
            setItems(newPanes);
            setActiveKey(newActiveKey);
        } else {
            setActiveKey(newActiveKey);
        }
    };
    const addEditTab = (product) => {
        const newActiveKey = `edit${product.product_id}`;
        const newPanes = [...items];
        const alreadyHave = items.find(tab => tab.key === newActiveKey)
        if (!alreadyHave) {
            newPanes.push({
                label: `Edit '${product.product_name}'`,
                children: <EditProductModal getData={getAllProducts} selectedProduct={product} removeTab={remove} />,
                key: newActiveKey,
            });
            setItems(newPanes);
            setActiveKey(newActiveKey);
        } else {
            setActiveKey(newActiveKey);
        }
    };
    const remove = (targetKey) => {
        let newActiveKey = activeKey;
        let lastIndex = -1;
        items.forEach((item, i) => {
            if (item.key === targetKey) {
                lastIndex = i - 1;
            }
        });
        const newPanes = items.filter((item) => item.key !== targetKey);
        if (newPanes.length && newActiveKey === targetKey) {
            if (lastIndex >= 0) {
                newActiveKey = newPanes[lastIndex].key;
            } else {
                newActiveKey = newPanes[0].key;
            }
        }
        setItems(newPanes);
        setActiveKey(newActiveKey);
    };
    const onEdit = (targetKey, action) => {
        if (action === 'add') {
            add();
        } else {
            remove(targetKey);
        }
    };
    const onChange = (newActiveKey) => {
        setActiveKey(newActiveKey);
    };
    return (
        <div style={{ backgroundColor: "#fff", margin: 10, borderRadius: 10, }}>
            <Tabs type="editable-card" hideAdd items={items} onChange={onChange} activeKey={activeKey} onEdit={onEdit} />
            {/* header */}
            {activeKey === "home" && <>
                <Overview products={allProducts} />
                <Divider />
                <div style={{ display: 'flex', alignItems: 'center', justifyContent: "space-between", marginBottom: 10 }}>
                    <div>
                    </div>
                    {allProducts.length !== 0 && <Button type='primary' onClick={addUploadTab}><UploadOutlined />Add New Product</Button>}
                </div>
                <div>
                    {allProducts.length === 0 && <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', height: 320 }}>
                        <Empty description={"No product right now"} >
                            <Button onClick={addUploadTab} type="primary"><UploadOutlined />Create Now</Button>
                        </Empty>
                    </div>}
                    <Space wrap size={'middle'}>

                        {allProducts.map((item, key) =>
                            <Card
                                key={key}
                                hoverable
                                style={{ width: cardWidth }}
                                cover={
                                    <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                                        <img style={{ maxWidth: cardWidth, height: cardHeight, width: 'auto', objectFit: 'cover' }} alt="example" src={item.product_picture[0]} />
                                    </div>
                                }
                                actions={[
                                    <Popconfirm
                                        title="Delete the product"
                                        description="Are you sure to delete this product?"
                                        onConfirm={() => handleDeleteProduct(item.product_id)}
                                        okText="Yes"
                                        cancelText="No"
                                    >
                                        <DeleteOutlined key="delete" />
                                    </Popconfirm>,
                                    <div onClick={() => {
                                        addEditTab(item)
                                    }}>
                                        <EditOutlined key="edit" />
                                    </div>,
                                ]}
                            >
                                <Meta title={item.product_name} description={item.product_description} />
                            </Card>
                        )}
                    </Space>
                </div>
            </>
            }
            {/* <Product /> */}
            <Modal
                open={updateProductModalVisible}
                title="Update Product"
                onOk={() => setUpdateProductModalVisible(false)}
                onCancel={() => setUpdateProductModalVisible(false)}
                footer={null}
            >

            </Modal>
        </div >
    )
}

export default index