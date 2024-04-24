import COLORS from '@/constants/COLORS';
import './index.less'
import { Divider, } from 'antd';
import { useState } from 'react';
import EmptyBox from '@/assets/pic/EmptyBox.png'
import OrderCard from '../Order';
import { useNavigate } from 'react-router-dom';
const UnpaidOrders = () => {
    const [orders, setOrders] = useState([{}, {}])
    const navigateTo = useNavigate()
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
                {orders.map((item, index) => {
                    return <OrderCard key={index} />
                })}
            </div>}
        </div>
        <div className='UnpaidContainer-right'>
            <div className='UnpaidContainer-right-header'>
                Order Summary
            </div>
            <div className='UnpaidContainer-right-body'>
                <div className='UnpaidContainer-right-body-item'>
                    <div className='UnpaidContainer-right-body-item-name'>Item Total:</div>
                    <div className='UnpaidContainer-right-body-item-price' style={{ textDecoration: 'line-through', color: "#747474" }}>CHF2.9</div>
                </div>
                <div className='UnpaidContainer-right-body-item'>
                    <div className='UnpaidContainer-right-body-item-name'>Item Discount:</div>
                    <div className='UnpaidContainer-right-body-item-price' style={{ color: COLORS.primary, fontWeight: 'bold' }}>-CHF2.9</div>
                </div>
            </div>
            <Divider />
            <div className='UnpaidContainer-right-footer'>
                <div className='UnpaidContainer-right-footer-price'>
                    <div>Total: ({orders.length} items) </div>
                    <div>CHF 1000.10</div>
                </div>
                <div className='UnpaidContainer-right-footer-button'>
                    <div className='UnpaidContainer-right-footer-button-checkout'>Checkout</div>
                </div>
            </div>
        </div>
    </div>
}

export default UnpaidOrders