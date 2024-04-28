import { getOrderByUserId } from '@/api/user.api';
import React, { useEffect, useState } from 'react'
import { useSelector } from 'react-redux';

const StateContext = React.createContext();

const StateContextProvider = ({ children }) => {
    const { user } = useSelector(state => state.user)
    const [orders, setOrders] = useState([]);
    const getOrders = async () => {
        user?.user_id && await getOrderByUserId(user.user_id).then(res => {
            console.log("here", res);
            setOrders(res.Items)
        })
    }
    useEffect(() => {
        user?.user_id && getOrders();
    }, [])
    return (
        <StateContext.Provider value={{
            orders,
            getOrders,
            setOrders,
            orderNumber: orders.length
        }}>
            {children}
        </StateContext.Provider>
    )
}

export default StateContextProvider

export const useStateContext = () => React.useContext(StateContext)