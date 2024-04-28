import COLORS from '@/constants/COLORS'
import './index.less'
import { DeleteTwoTone, RightOutlined } from '@ant-design/icons'
import { Avatar, InputNumber, Popconfirm, message } from 'antd'
import { useNavigate } from 'react-router-dom'
import checked from '@/assets/pic/checked.png'
import unchecked from '@/assets/pic/unchecked.svg'
import { useEffect, useState } from 'react'
import { getProductById, getShopById, removeProductFromOrder } from '@/api/user.api'
import { useStateContext } from '@/pages/ClientHomePage/context'

export default function OrderCard({ orderInfo, specificProductInfo }) {
    const { product_id, quantity, product_owner } = specificProductInfo
    const [product, setProduct] = useState({
        product_assemblies: [],
        product_name: "",
        product_picture: ["https://cdn.corporatefinanceinstitute.com/assets/products-and-services.jpeg"],
        product_price: 0,
        product_price_reduction: 0,
    })
    const getProductInfo = async () => {
        await getProductById(product_id).then((res) => {
            if (res.status === true) {
                setProduct(res.value)
            }
        })
    }

    // get Shop info
    const [ShopInfo, setShopInfo] = useState({ shop_name: "", profile_picture: "", shop_description: "" })
    const getProductOwnerInfo = async () => {
        await getShopById(product_owner).then((res) => {
            if (res.status === true) {
                setShopInfo(res.value)
            }
        })
    }
    useEffect(() => {
        getProductInfo()
        getProductOwnerInfo()
    }, [])

    const { order_id, orders_fe: orderItemsArray, totalprice } = orderInfo

    const navigateTo = useNavigate()
    const handleAddOperation = async () => {
    }
    const { getOrders, orders } = useStateContext()
    console.log(orders);
    const confirm = async (e) => {
        const reqData = {
            quantity: -quantity,
            product_id
        }
        await removeProductFromOrder(order_id, reqData).then(res => {
            if (res.status) {
                getOrders()
            } else {
                message.error("Error, please try again")
            }
        }).catch(err => {
            console.log(err);
            message.error("Error, please try again")
        })
    };
    const cancel = (e) => {
        console.log(e);
    };
    const [selected, setSelected] = useState(true)
    return (
        <div className={`OrderItemCard`} onClick={() => { }} >
            <div
                className='OrderItemCard-img'
                style={{
                    flexShrink: 0,
                    flexBasis: 100,
                    height: 100,
                    width: 100,
                    borderRadius: 10,
                    display: "flex",
                    justifyContent: "center",
                    alignItems: "center",
                    overflow: "hidden",
                    marginRight: 10
                }
                }
            >
                <img style={{ maxHeight: '100%', width: 'auto', height: 'auto', objectFit: 'cover' }} src={product.product_picture[0]} />
            </div >
            <div className='OrderItemCard-desc'>
                <span className='OrderItemCard-desc-productName'>
                    <span style={{ userSelect: 'none', fontSize: 18, fontWeight: 'bold' }}>
                        {product.product_name}
                    </span>
                </span>
                <div className='OrderItemCard-desc-title' style={{ color: COLORS.commentText, fontSize: 12 }}>
                    {/* <span
                        onClick={() => navigateTo(`/user/home/shop/${product_owner}`)}
                        style={{ userSelect: 'none', cursor: 'pointer' }}>
                        By <Avatar size={18} src={ShopInfo.profile_picture} /> {ShopInfo.shop_name} <RightOutlined size={12} />
                    </span> */}
                </div>
                <div>
                    <div style={{ display: 'flex', marginTop: 20, justifyContent: 'space-between' }}>
                        <div style={{ display: 'flex', alignItems: 'center', userSelect: 'none', gap: 10 }}>
                            <div style={{ fontWeight: 'bold' }}>Quantity: </div>
                            <div><InputNumber variant='borderless' disabled min={1} max={100} defaultValue={quantity} onChange={(num) => {
                                // setQuantity(num)
                            }} /></div>
                        </div>
                        <div style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
                            <div style={{ display: 'flex', alignItems: 'baseline', fontSize: 16, gap: 2, fontWeight: 'bold', color: '#4790ff' }}>
                                <div>CHF</div>
                                <div style={{ fontSize: 26 }}>{(quantity * product.product_price * (100 - product.product_price_reduction) / 100).toFixed(2)}</div>
                            </div>
                            {(100 - product.product_price_reduction) != 0 && <><div style={{ color: '#4790ff', fontSize: 14, borderRadius: 6, padding: "0 6px", border: "1px solid #4790ff" }}>-{product.product_price_reduction}%</div>
                                <div style={{ color: 'rgb(170, 170, 170)', fontSize: 14, textDecoration: 'line-through' }}>{product.product_price}</div>
                            </>}
                        </div>
                    </div>
                </div>
            </div>
            <div>
                <span style={{ userSelect: 'none', cursor: 'pointer' }}>
                    <Popconfirm
                        title="Delete the order"
                        description="Are you sure to delete this order?"
                        onConfirm={confirm}
                        onCancel={cancel}
                        okText="Yes"
                        cancelText="No"
                    >
                        <DeleteTwoTone twoToneColor={COLORS.commentText} />
                    </Popconfirm>
                </span>
            </div>
        </div >
    )
}
