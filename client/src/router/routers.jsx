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

export default function MyRouter() {
    // const { user } = useSelector(state => state.user)
    const router = createBrowserRouter([
        {
            path: "/",
            element: <CheckProtectedRouter><Dashboard /></CheckProtectedRouter>,
            errorElement: <ErrorPage />,
        },
        {
            path: "/seller",
            element: <ProtectedRouter><Dashboard /></ProtectedRouter>,
            errorElement: <ErrorPage />,
            children: [
                {
                    path: "home",
                    element: <ProtectedRouter><SellerHome /></ProtectedRouter>,
                    // loader: async () => await getStatistics()
                },
            ]
        },
        {
            path: "/buyer",
            element: <ClientHomePage />,
            // element: <ProtectedRouter><ClientHomePage /></ProtectedRouter>,
            errorElement: <ErrorPage />,
            // children: [
            //     {
            //         path: "products",
            //         element: <ProtectedRouter><Home /></ProtectedRouter>,
            //     },
            //     {
            //         path: "profile",
            //         element: <ProtectedRouter><StatisticBoard /></ProtectedRouter>,
            //     },
            // ]
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
