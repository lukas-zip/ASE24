import './index.less'
import { Tabs } from 'antd';
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { ClockCircleOutlined, WalletOutlined } from '@ant-design/icons';
import UnpaidOrders from './Components/UnpaidOrders';
import PaidOrders from './Components/PaidOrders';
import { useStateContext } from '@/pages/ClientHomePage/context';

const tabsKey = {
    UNPAID: "Unpaid",
    PAID: "Paid"
}
export default function OrderPage() {
    const { unpaidOrders, paidOrders } = useStateContext()
    const navigateTo = useNavigate()
    const [activeTab, setActiveTab] = useState(tabsKey.PAID)
    return (
        <div className='containerWrapper' style={{ margin: 10 }}>
            <div className='ShoppingCartPage-header'>
                <div className='ShoppingCartPage-header-title'>All Orders</div>
                <Tabs
                    defaultActiveKey={activeTab}
                    onChange={(e) => setActiveTab(e)}
                    items={[
                        { key: tabsKey.PAID, label: `${tabsKey.PAID} (${paidOrders?.length ? paidOrders?.length : 0})`, icon: <WalletOutlined /> },
                        { key: tabsKey.UNPAID, label: `${tabsKey.UNPAID} (${unpaidOrders?.length ? unpaidOrders?.length : 0})`, icon: <ClockCircleOutlined /> },
                    ]}
                />
            </div>
            {activeTab === tabsKey.UNPAID && <UnpaidOrders />}
            {activeTab === tabsKey.PAID && <PaidOrders />}
        </div >
    )
}

