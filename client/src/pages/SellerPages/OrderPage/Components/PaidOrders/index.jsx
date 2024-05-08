import './index.less'
import EmptyBox from '@/assets/pic/EmptyBox.png'
import OrderCard from '../OrderCard';
import { useStateContext } from '@/pages/ClientHomePage/context';
const PaidOrders = () => {
    const { paidOrders } = useStateContext()
    console.log("unpaidOrders", paidOrders);
    return <div className={`UnpaidContainer`}>
        <div className='UnpaidContainer-left'>
            {paidOrders.length === 0 && <div className='UnpaidContainer-left-empty'>
                <div className='emptyContent'>
                    <img src={EmptyBox} alt="" />
                    <div className='emptyContent-textContainer'>
                        <div style={{ fontSize: 18, fontWeight: 'bold' }}>There is no paid order right now</div>
                        {/* <div style={{ color: "#747474" }}>Add your favorite items in it.</div> */}
                    </div>
                </div>
            </div>}
            {paidOrders.length !== 0 && <div className='UnpaidContainer-left-content'>
                {paidOrders.map((item) => {
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

export default PaidOrders