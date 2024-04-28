import { useEffect, useState } from 'react';
import Sidebar from './components/sidebar'
import { useSelector } from 'react-redux'
import { useNavigate, Outlet, useLocation } from 'react-router-dom'
import './index.less';
import { Badge } from 'antd';
import { ShoppingFilled } from '@ant-design/icons';
import { useStateContext } from './context';

const ClientHomePage = () => {
    const { orderNumber } = useStateContext()
    const { user } = useSelector((state) => state.user)
    const navigateTo = useNavigate()
    useEffect(() => {
        !user && navigateTo('/login')
    }, [])
    const location = useLocation()
    const [shoppingChartDisplay, setShoppingChartDisplay] = useState(true)
    useEffect(() => {
        setShoppingChartDisplay(location.pathname.split('/')[2] !== "cart");
    }, [location])
    return (
        <div className={`App App-light`}>
            <div className={`myDashboard myDashboard-light`}>
                <Sidebar />
                <Outlet />
            </div>
            {shoppingChartDisplay && <div className='shoppingCartBtn' onClick={() => navigateTo("/user/cart")}>
                <Badge count={orderNumber}>
                    <ShoppingFilled style={{ fontSize: 22, color: "white" }} />
                </Badge>
            </div>}
        </div>
    );
}
export default ClientHomePage




