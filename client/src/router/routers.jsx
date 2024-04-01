import { createBrowserRouter, RouterProvider } from 'react-router-dom'
import Dashboard from "../pages/Dashboard"
import Login from '../pages/Login'
import ErrorPage from '../pages/ErrorPage'
import ProtectedRouter from './protectedRouter'
import SellerHome from '../pages/SellerPages/Home'
import { useSelector } from 'react-redux'
import CheckProtectedRouter from './CheckProtectedRouter'
import ClientHomePage from '../pages/ClientHomePage'
import IdentityInfoPage from '../pages/IdentityInfoPage'
import SettingPage from '../pages/ClientHomePage/pages/settingPage'
import ShoppingCartPage from '../pages/ClientHomePage/pages/ShoppingCartPage'
import StatisticPage from '../pages/ClientHomePage/pages/StatisticPage'
import UserHomePage from '../pages/ClientHomePage/pages/HomePage'

export default function MyRouter() {
    const { user } = useSelector(state => state.user)
    const router = createBrowserRouter([
        {
            path: "/",
            element: <CheckProtectedRouter><Dashboard /></CheckProtectedRouter>,
            errorElement: <ErrorPage />,
        },
        {
            path: "/shop",
            element: <ProtectedRouter><Dashboard /></ProtectedRouter>,
            errorElement: <ErrorPage />,
            children: [
                {
                    path: "home",
                    element: <ProtectedRouter><SellerHome /></ProtectedRouter>,
                    // loader: async () => await getStatistics()
                },
                {
                    path: "statistic",
                    element: <ProtectedRouter><SellerHome /></ProtectedRouter>,
                    // loader: async () => await getStatistics()
                },
                {
                    path: "settings",
                    element: <ProtectedRouter><SellerHome /></ProtectedRouter>,
                    // loader: async () => await getStatistics()
                },
            ]
        },
        {
            path: "/user",
            element: <ProtectedRouter><ClientHomePage /></ProtectedRouter>,
            // element: <ProtectedRouter><ClientHomePage /></ProtectedRouter>,
            errorElement: <ErrorPage />,
            children: [
                {
                    path: "home",
                    element: <ProtectedRouter><UserHomePage /></ProtectedRouter>,
                },
                {
                    path: "cart",
                    element: <ProtectedRouter><ShoppingCartPage /></ProtectedRouter>,
                },
                {
                    path: "statistics",
                    element: <ProtectedRouter><StatisticPage /></ProtectedRouter>,
                },
                {
                    path: "profile",
                    element: <ProtectedRouter><SettingPage /></ProtectedRouter>,
                },
            ]
        },
        {
            path: "/info",
            element: <IdentityInfoPage />
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
