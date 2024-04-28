import { getOrderByShopId, getOrderByUserId } from '@/api/user.api';
import React, { useEffect, useState } from 'react'
import { useSelector } from 'react-redux';

const StateContext = React.createContext();

const StateContextProvider = ({ children }) => {
    const { user } = useSelector(state => state.user)
    console.log(user);
    const [orders, setOrders] = useState([]);
    const getOrders = async () => {
        if (user?.type === "Shop") {
            await getOrderByShopId(user.shop_id).then(res => {
                console.log("serhop de", res);
                if (res.status) {
                    setOrders(res.value.Items)
                }
            })
        }
        user?.user_id && await getOrderByUserId(user.user_id).then(res => {
            if (res.status) {
                setOrders(res.value.Items)
            }
        })
    }
    useEffect(() => {
        (user?.user_id || user?.type === "Shop") && getOrders();
    }, [])
    return (
        <StateContext.Provider value={{
            orders,
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