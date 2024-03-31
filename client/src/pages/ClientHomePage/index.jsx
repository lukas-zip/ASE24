import { useEffect } from 'react';
import Sidebar from './components/sidebar'
import { useSelector } from 'react-redux'
import { useNavigate, Outlet } from 'react-router-dom'
import './index.less';

const ClientHomePage = () => {
    const { user } = useSelector((state) => state.user)
    const navigateTo = useNavigate()
    useEffect(() => {
        !user && navigateTo('/login')
    }, [])
    return (
        <div className={`App App-light`}>
            <div className={`myDashboard myDashboard-light`}>
                <Sidebar />
                <Outlet />
            </div>
        </div>
    );
}
export default ClientHomePage




