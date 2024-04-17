import COLORS from '@/constants/COLORS'
import './index.less'
import { DeleteTwoTone, RightOutlined } from '@ant-design/icons'
import { Avatar, InputNumber, Popconfirm } from 'antd'
import { useNavigate } from 'react-router-dom'
import checked from '@/assets/pic/checked.png'
import unchecked from '@/assets/pic/unchecked.svg'
import { useState } from 'react'

export default function OrderCard({ }) {
    const navigateTo = useNavigate()
    const order = {
        order_id: 1,
        order_status: "PENDING",
        quantity: 1,
    }
    const { quantity } = order
    const product = {
        product_assemblies: [],
        product_name: "Product_name",
        product_description: "Product_description",
        product_bom: [],
        product_price: 100.00,
        product_price_reduction: 10
    }
    const {
        product_assemblies,
        product_name,
        product_description,
        product_bom,
        product_picture = ["https://cdn.corporatefinanceinstitute.com/assets/products-and-services.jpeg"],
        product_search_attributes,
        product_price,
        product_owner,
        product_price_reduction,
        product_id,
    } = product
    const handleAddOperation = async () => {
    }
    const confirm = (e) => {
        console.log(e);
    };
    const cancel = (e) => {
        console.log(e);
    };
    const [selected, setSelected] = useState(false)
    return (
        <div className={`OrderItemCard`} onClick={() => { }} >
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', }}>
                {/* <img src={unchecked} style={{ width: 36, height: 36, marginRight: 10 }}></img> */}
                <img src={selected ? checked : unchecked} onClick={() => setSelected(!selected)} style={{ width: 30, height: 30, cursor: 'pointer', marginRight: 10 }}></img>
            </div>
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
                }}
            >
                <img style={{ maxHeight: '100%', width: 'auto', height: 'auto', objectFit: 'cover' }} src={product_picture[0]} />
            </div>
            <div className='OrderItemCard-desc'>
                <span className='OrderItemCard-desc-productName'>
                    <span style={{ userSelect: 'none' }}>
                        {product_name}
                    </span>
                </span>
                <div className='OrderItemCard-desc-title' style={{ color: COLORS.commentText, fontSize: 12 }}>
                    <span style={{ userSelect: 'none', cursor: 'pointer' }}>
                        By <Avatar size={18} /> shop_name <RightOutlined size={12} />
                    </span>
                </div>
                <div>
                    <div style={{ display: 'flex', marginTop: 20, justifyContent: 'space-between' }}>
                        <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
                            <div style={{ fontWeight: 'bold' }}>Quantity: </div>
                            <div><InputNumber min={1} max={6} defaultValue={quantity} onChange={(num) => {
                                // setQuantity(num)
                            }} /></div>
                        </div>
                        <div style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
                            <div style={{ display: 'flex', alignItems: 'baseline', fontSize: 16, gap: 2, fontWeight: 'bold', color: '#4790ff' }}>
                                <div>CHF</div>
                                <div style={{ fontSize: 26 }}>{(product_price * (100 - product_price_reduction) / 100).toPrecision(2)}</div>
                            </div>
                            {(100 - product_price_reduction) != 0 && <><div style={{ color: '#4790ff', fontSize: 14, borderRadius: 6, padding: "0 6px", border: "1px solid #4790ff" }}>-{product_price_reduction}%</div>
                                <div style={{ color: 'rgb(170, 170, 170)', fontSize: 14, textDecoration: 'line-through' }}>{product_price}</div>
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
