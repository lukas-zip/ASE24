import { createBrowserRouter, RouterProvider } from 'react-router-dom'
import Dashboard from "../pages/Dashboard"
import Login from '../pages/Login'
import ErrorPage from '../pages/ErrorPage'
import StatisticBoard from '../pages/Statistic'
import ProtectedRouter from './protectedRouter'
import Home from '../pages/Home'
import { useSelector } from 'react-redux'
import CheckProtectedRouter from './CheckProtectedRouter'

export default function MyRouter() {
    // const { user } = useSelector(state => state.user)
    const router = createBrowserRouter([
        {
            path: "/",
            element: <CheckProtectedRouter><Dashboard /></CheckProtectedRouter>,
            errorElement: <ErrorPage />,
            // children: [
            //     {
            //         path: "home",
            //         element: <ProtectedRouter><Home /></ProtectedRouter>,
            //     },
            // ]
        },
        {
            path: "/seller",
            element: <ProtectedRouter><Dashboard /></ProtectedRouter>,
            errorElement: <ErrorPage />,
            children: [
                {
                    path: "home",
                    element: <ProtectedRouter><Home /></ProtectedRouter>,
                    // loader: async () => await getStatistics()
                },
            ]
        },
        {
            path: "/buyer",
            element: <ProtectedRouter><Dashboard /></ProtectedRouter>,
            errorElement: <ErrorPage />,
            children: [
                {
                    path: "products",
                    element: <ProtectedRouter><Home /></ProtectedRouter>,
                    // loader: async () => await getStatistics()
                },
                {
                    path: "profile",
                    element: <ProtectedRouter><StatisticBoard /></ProtectedRouter>,
                    // loader: async () => await getStatistics()
                },
            ]
        },
        {
            path: "/login",
            element: <Login />
        },
    ])
    return (
        <RouterProvider router={router} />
    )
}
