import COLORS from '@/constants/COLORS';
import './index.less'
import { Button, Divider, Modal, message, Input } from 'antd';
const { TextArea } = Input
import EmptyBox from '@/assets/pic/EmptyBox.png'
import OrderCard from '../Order';
import { useNavigate } from 'react-router-dom';
import { useStateContext } from '@/pages/ClientHomePage/context';
import { loadStripe } from '@stripe/stripe-js';
import { useEffect, useState } from 'react';
import { createPaymentIntent, updateUser } from '@/api/user.api';
import { useDispatch, useSelector } from 'react-redux';
import { Elements } from '@stripe/react-stripe-js';
import CheckoutForm from './CheckoutForm';
import { EnvironmentOutlined } from '@ant-design/icons';
import { setUser } from '@/store/user.store';

const stripePromise = loadStripe("pk_test_51P3x1RL2VoulaBDdTZCgMoiGawfZWU3PyyMlhvjhwOKneaA7Ui480S5c52HMqL8RZ8e3EIrQHGIyr4LPwxV6MU5800HxUrmS6y");

const UnpaidOrders = () => {
    const { user } = useSelector(state => state.user)
    const { orders } = useStateContext()
    console.log(orders);
    const navigateTo = useNavigate()
    const [clientSecret, setClientSecret] = useState("");

    const PaymentIntent = async () => {
        if (orders[0]?.order_id) {
            const reqBody = { user_id: user.user_id, order_id: orders[0].order_id, total_price: Number(orders[0].total_price) }
            await createPaymentIntent(reqBody).then(res => {
                setClientSecret(res.clientSecret)
            })
        }
    }
    useEffect(() => {
        PaymentIntent()
    }, [orders[0]?.order_id]);

    const appearance = {
        theme: 'stripe',
    };
    const options = {
        clientSecret,
        appearance,
    };

    const dispatch = useDispatch()
    const [updateAddressLoading, setUpdatedAddressLoading] = useState(false)
    const [addressModalOpen, setAddressModalOpen] = useState(false)
    const [updatedAddress, setUpdatedAddress] = useState(user.address)
    const updateAddress = async () => {
        try {
            if (updatedAddress === user.address) {
                message.error("Address not changed")
                return
            } else if (!updatedAddress) {
                message.error("Nothing to update")
                return
            }
            setUpdatedAddressLoading(true)
            let handledItems = { ...user, address: updatedAddress, action: 'update' }
            await updateUser(user.user_id, handledItems)
                .then((res) => {
                    setUpdatedAddressLoading(false)
                    if (res.status) {
                        dispatch(setUser(res.value))
                        setAddressModalOpen(false)
                        message.success("Update successfully")
                    } else {
                        message.error(res.message)
                    }
                }).catch(err => {
                    console.log(err);
                    setUpdatedAddressLoading(false)
                })
        } catch (error) {
            console.log(error);
            message.error("Error")
        }
    }

    const [paymentModalOpen, setPaymentModalOpen] = useState(false)
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
                {orders.map((item) => {
                    const { order_id, orders_fe: orderItemsArray, totalprice } = item
                    return <div key={order_id}>
                        {orderItemsArray.map((specificProductInfo, key) => <OrderCard key={key} orderInfo={item} specificProductInfo={specificProductInfo} />)}
                    </div>
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
                    <div className='UnpaidContainer-right-body-item-price' style={{ textDecoration: 'line-through', color: "#747474" }}>CHF</div>
                </div>
                <div className='UnpaidContainer-right-body-item'>
                    <div className='UnpaidContainer-right-body-item-name'>Item Discount:</div>
                    <div className='UnpaidContainer-right-body-item-price' style={{ color: COLORS.primary, fontWeight: 'bold' }}>-CHF</div>
                </div>
            </div>
            <Divider />
            <div className='UnpaidContainer-right-footer'>
                <div className='UnpaidContainer-right-footer-price'>
                    <div>Total: ({(orders[0] && orders[0]?.orders_fe) ? orders[0].orders_fe.length : 0} items) </div>
                    <div>CHF {(orders[0] && orders[0]?.total_price) ? Number(orders[0].total_price).toFixed(2) : 0}</div>
                </div>
                <div style={{ display: 'flex', alignItems: 'center', marginTop: 10, }}>
                    <EnvironmentOutlined twoToneColor="#3d3d3d" style={{ fontSize: 18 }} />
                    <div style={{ marginLeft: 6, display: 'flex', alignItems: 'center', gap: 10 }}>
                        <div style={{ fontSize: 12, color: COLORS.commentText, userSelect: 'none' }}>Deliver to</div>
                        <div onClick={() => setAddressModalOpen(true)} style={{ fontSize: 14, cursor: 'pointer' }}>{user.address ? user.address : "Fill your address"}</div>
                    </div>
                </div>
                <div className='UnpaidContainer-right-footer-button' onClick={() => setPaymentModalOpen(true)}>
                    <div className='UnpaidContainer-right-footer-button-checkout'>Checkout</div>
                </div>
            </div>

            <Modal title="Payment" open={paymentModalOpen} width={1000} footer={null} onOk={() => { setPaymentModalOpen(false) }} onCancel={() => { setPaymentModalOpen(false) }}>
                <div style={{ width: "100%", height: 500, display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
                    {clientSecret && (
                        <Elements options={options} stripe={stripePromise}>
                            <CheckoutForm />
                        </Elements>
                    )}
                </div>
            </Modal>

            <Modal title="Address" open={addressModalOpen} footer={null} onCancel={() => setAddressModalOpen(false)} onOk={() => { setAddressModalOpen(false) }}>
                <div>
                    <TextArea onChange={(e) => setUpdatedAddress(e.target.value)} defaultValue={user.address} variant="filled" />
                </div>
                <div style={{ marginTop: 10, display: 'flex', justifyContent: 'flex-end' }}>
                    <Button loading={updateAddressLoading} onClick={updateAddress} type='primary'>Update</Button>
                </div>
            </Modal>
        </div>
    </div >
}

export default UnpaidOrders