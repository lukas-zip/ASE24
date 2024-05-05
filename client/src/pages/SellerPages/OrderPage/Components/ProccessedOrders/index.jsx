import './index.less'
import EmptyBox from '@/assets/pic/EmptyBox.png'
import OrderCard from '../Order';
import { useStateContext } from '@/pages/ClientHomePage/context';
const ProccessedOrders = () => {
    const { orders } = useStateContext()
    console.log(orders);
    return <div className={`UnpaidContainer`}>
        <div className='UnpaidContainer-left'>
            {orders.length === 0 && <div className='UnpaidContainer-left-empty'>
                <div className='emptyContent'>
                    <img src={EmptyBox} alt="" />
                    <div className='emptyContent-textContainer'>
                        <div style={{ fontSize: 18, fontWeight: 'bold' }}>There is no order right now</div>
                        {/* <div style={{ color: "#747474" }}>Add your favorite items in it.</div> */}
                    </div>
                </div>
            </div>}
            {orders.length !== 0 && <div className='UnpaidContainer-left-content'>
                {orders.map((item) => {
                    const { order_id, orders_fe: orderItemsArray } = item
                    return <div key={order_id}>
                        {orderItemsArray.map((specificProductInfo, key) => {
                            if (specificProductInfo.quantity !== 0) {
                                return <OrderCard key={key} orderInfo={item} specificProductInfo={specificProductInfo} />
                            }
                        })}
                    </div>
                })}
            </div>}
        </div>
    </div>
}

export default ProccessedOrders