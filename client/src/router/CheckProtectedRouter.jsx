import React from 'react'
import { useSelector } from 'react-redux'
import { Navigate } from 'react-router-dom'
import CONSTANTS from '../constants'

export default function CheckProtectedRouter({ children }) {
    const { user } = useSelector(state => state.user)
    if (!user) {
        return <Navigate to={'/login'} />
    } else {
        if (user.type === CONSTANTS.USER_TYPE.SHOP) {
            return <Navigate to={'/shop'} />
        } else if (user.type === CONSTANTS.USER_TYPE.USER) {
            return <Navigate to={'/user'} />
        }
    }
}
