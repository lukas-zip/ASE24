import { useEffect } from 'react';
import Sidebar from './components/sidebar'
import { useSelector } from 'react-redux'
import { useNavigate, Outlet } from 'react-router-dom'
import './index.less';

const ClientHomePage = () => {
    const { user, currentTheme } = useSelector((state) => state.user)
    const navigateTo = useNavigate()
    const lightAppClassname = currentTheme === 'light' ? 'App-light' : ''
    const lightDashboardClassname = currentTheme === 'light' ? 'myDashboard-light' : ''
    useEffect(() => {
        !user && navigateTo('/login')
    }, [])
    return (
        <div className={`App ${lightAppClassname}`}>
            <div className={`myDashboard ${lightDashboardClassname}`}>
                <Sidebar />
                <Outlet />
            </div>
        </div>
    );
}
export default ClientHomePage




