import React from 'react'
import { useSelector } from 'react-redux'
import { Navigate } from 'react-router-dom'
import CONSTANTS from '../constants'

export default function CheckProtectedRouter({ children }) {
    let { user } = useSelector(state => state.user)
    user = {
        type: "seller",
        id: 1,
    }
    if (!user) {
        console.log("zhe");
        return <Navigate to={'/login'} />
    } else {
        console.log("zhe1");
        if (user.type === CONSTANTS.USER_TYPE.BUYER) {
            return <Navigate to={'/buyer'} />
        } else if (user.type === CONSTANTS.USER_TYPE.SELLER) {
            return <Navigate to={'/seller'} />
        }
    }
}
