import COLORS from '@/constants/COLORS'
import './index.less'
import { Avatar, InputNumber, message } from 'antd'
import { useNavigate } from 'react-router-dom'
import { useEffect, useState } from 'react'
import { getProductById, getShopById, getUserById, removeProductFromOrder } from '@/api/user.api'
import { useStateContext } from '@/pages/ClientHomePage/context'
import { UserOutlined } from '@ant-design/icons'

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

    const { order_id, orders_fe: orderItemsArray, total_price, execution_time, user_id } = orderInfo
    const [userInfo, setUserInfo] = useState()
    console.log(orderInfo);
    const getUserInfo = async () => {
        await getUserById(user_id).then((res) => {
            if (res.status === true) {
                setUserInfo(res.value)
            }
        })
    }
    useEffect(() => {
        getProductInfo()
        getProductOwnerInfo()
        getUserInfo()
    }, [])
    const navigateTo = useNavigate()
    const handleAddOperation = async () => {
    }
    const { getOrders, orders } = useStateContext()
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
            <div className='OrderItemCard-desc' style={{ display: 'flex', justifyContent: 'space-between', paddingBottom: 10 }}>
                <div style={{ display: 'flex', flexDirection: 'column', gap: 6 }}>
                    <span className='OrderItemCard-desc-productName'>
                        <span style={{ userSelect: 'none', fontSize: 16, }}>Product Name: </span>
                        <span style={{ userSelect: 'none', fontSize: 18, fontWeight: 'bold' }}>
                            {product.product_name}
                        </span>
                    </span>
                    <span className='OrderItemCard-desc-productName'>
                        <span style={{ userSelect: 'none', fontSize: 16, }}>Quantity: </span>
                        <span style={{ userSelect: 'none', fontSize: 18, fontWeight: 'bold' }}>
                            {quantity}
                        </span>
                    </span>
                    <span className='OrderItemCard-desc-productName'>
                        <span style={{ userSelect: 'none', fontSize: 16, }}>Total Price: </span>
                        <span style={{ userSelect: 'none', fontSize: 18, fontWeight: 'bold', color: COLORS.primary }}>
                            {Number(total_price).toFixed(2)} CHF
                        </span>
                    </span>
                    <span className='OrderItemCard-desc-productName'>
                        <span style={{ userSelect: 'none', fontSize: 16 }}>Order Create Time: </span>
                        <span style={{ userSelect: 'none', }}>
                            {new Date(execution_time).toLocaleString()}
                        </span>
                    </span>
                </div>
                {/* <div>
                    <div style={{ display: 'flex', marginTop: 20, justifyContent: 'space-between' }}>
                        <div style={{ display: 'flex', alignItems: 'center', userSelect: 'none', gap: 10 }}>
                            <div style={{ fontWeight: 'bold' }}>Quantity: </div>
                            <div><InputNumber variant='borderless' disabled min={1} max={100} defaultValue={quantity} onChange={(num) => {
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
                </div> */}
                <div>
                    <div style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
                        <p style={{ userSelect: 'none', fontSize: 16 }}>Created By:</p>
                        <span style={{ padding: 6, borderRadius: 10, backgroundColor: COLORS.backgroundGray, }}><Avatar src={userInfo?.profile_picture} icon={<UserOutlined />} /> {userInfo?.username}</span>
                    </div>
                    <div style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
                        <p style={{ userSelect: 'none', fontSize: 16 }}>Address:</p>{userInfo?.address}
                    </div>
                </div>
            </div>
        </div >
    )
}
