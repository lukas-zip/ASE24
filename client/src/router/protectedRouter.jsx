import React from 'react'
import { useSelector } from 'react-redux'
import { Navigate } from 'react-router-dom'

export default function ProtectedRouter({ children }) {
    let { user } = useSelector(state => state.user)
    user = {
        name: "张三",
    }
    if (!user) {
        return <Navigate to={'/login'} />
    } else {
        return children
    }
}
