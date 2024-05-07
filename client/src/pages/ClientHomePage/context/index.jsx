import { getOrderByShopId, getOrderByUserId, getSellerPaidOrders, getSellerUnpaidOrders, getUserPaidOrders, getUserUnpaidOrders } from '@/api/user.api';
import { message } from 'antd';
import React, { useEffect, useState } from 'react'
import { useSelector } from 'react-redux';

const StateContext = React.createContext();

const StateContextProvider = ({ children }) => {
    const { user } = useSelector(state => state.user)
    console.log(user);
    const [orders, setOrders] = useState([]);

    const [unpaidOrders, setUnpaidOrders] = useState([])
    const [paidOrders, setPaidOrders] = useState([])

    const getOrders = async () => {
        if (user?.type === "Shop") {
            user?.shop_id && await getOrderByShopId(user.shop_id).then(res => {
                console.log("serhop de", res);
                if (res.status) {
                    setOrders(res.value.Items)
                }
            })
            user?.shop_id && await getSellerUnpaidOrders(user.shop_id).then(res => {
                if (res.status) {
                    const resObj = res.value
                    setUnpaidOrders(resObj.Items)
                }
            })
            user?.shop_id && await getSellerPaidOrders(user.shop_id).then(res => {
                if (res.status) {
                    const resObj = res.value
                    setPaidOrders(resObj.Items)
                }
            })
        } else if (user?.type === "User") {
            user?.user_id && await getOrderByUserId(user.user_id).then(res => {
                if (res.status) {
                    console.log("whether", res);
                    setOrders(res.value.Items)
                }
            })
            user?.user_id && await getUserUnpaidOrders(user.user_id).then(res => {
                if (res.status) {
                    const resObj = res.value
                    console.log("un", res);
                    setUnpaidOrders(resObj.Items)
                }
            })
            user?.user_id && await getUserPaidOrders(user.user_id).then(res => {
                if (res.status) {
                    const resObj = res.value
                    setPaidOrders(resObj.Items)
                }
            })
        }
    }
    useEffect(() => {
        getOrders();
    }, [])
    return (
        <StateContext.Provider value={{
            orders,
            unpaidOrders,
            paidOrders,
            getOrders,
            setOrders,
            orderNumber: orders[0]?.orders_fe?.length
        }}>
            {children}
        </StateContext.Provider>
    )
}

export default StateContextProvider

export const useStateContext = () => React.useContext(StateContext)