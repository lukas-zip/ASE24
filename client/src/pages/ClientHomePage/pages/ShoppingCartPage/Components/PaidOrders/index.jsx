import './index.less'
import { Button, Divider, message, } from 'antd';
import EmptyBox from '@/assets/pic/EmptyBox.png'
import { useNavigate } from 'react-router-dom';
import { useStateContext } from '@/pages/ClientHomePage/context';
import PaidOrderCard from '../PaidOrderCard';
import { saveAs } from 'file-saver';
import { serviceBases } from '@/api/request';
import COLORS from '@/constants/COLORS';

const PaidOrders = () => {
    const { orders } = useStateContext()
    console.log(orders);
    const navigateTo = useNavigate()

    const SaveFile = async (orderId) => {
        await fetch(serviceBases.orders + `/invoice/${orderId}`).then(res => res.blob()).then(blob => {
            saveAs(blob)
        }).catch(err => {
            message.error("Failed to download invoice")
        })
    }
    return <div className={`UnpaidContainer`}>
        <div className='UnpaidContainer-left'>
            {orders.length === 0 && <div className='UnpaidContainer-left-empty'>
                <div className='emptyContent'>
                    <img src={EmptyBox} alt="" />
                    <div className='emptyContent-textContainer'>
                        <div style={{ fontSize: 18, fontWeight: 'bold' }}>Your shopping cart is empty</div>
                        <div style={{ color: "#747474" }}>Add your favorite items in it.</div>
                    </div>
                </div>
                <div className='startShopping' onClick={() => navigateTo('/')}>
                    Start shopping
                </div>
            </div>}
            {orders.length !== 0 && <div className='UnpaidContainer-left-content'>
                {orders.map((item, key) => {
                    const { order_id, orders_fe: orderItemsArray, totalprice } = item
                    console.log("he", item);
                    return <div key={order_id}>
                        <div style={{ padding: "0 20px 6px", display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                            <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
                                <p style={{ fontSize: 18, fontWeight: 600, }}>Order {key + 1}</p>
                                <p style={{ color: COLORS.black }}>Create time: {new Date(item.execution_time).toLocaleDateString()}</p>
                            </div>
                            <Button type='primary' onClick={() => SaveFile(order_id)}>Download Invoice</Button>
                        </div>
                        {orderItemsArray.map((specificProductInfo, key) => <PaidOrderCard key={key} orderInfo={item} specificProductInfo={specificProductInfo} />)}
                        <Divider />
                    </div>
                })}
            </div>}
        </div>
    </div>
}

export default PaidOrders