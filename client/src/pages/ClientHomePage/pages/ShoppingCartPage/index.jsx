import COLORS from '@/constants/COLORS';
import './index.less'
import { Tabs } from 'antd';
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { ClockCircleOutlined, WalletOutlined } from '@ant-design/icons';
import UnpaidOrders from './Components/UnpaidOrders';
import PaidOrders from './Components/PaidOrders';

const tabsKey = {
    UNPAID: "unpaid",
    PAID: "paid",
}
export default function ShoppingCartPage() {
    const navigateTo = useNavigate()
    const [activeTab, setActiveTab] = useState(tabsKey.UNPAID)
    return (
        <div className='containerWrapper'>
            <div className='ShoppingCartPage-header'>
                <div className='ShoppingCartPage-header-title'>Shopping Cart</div>
                <Tabs
                    defaultActiveKey={activeTab}
                    onChange={(e) => setActiveTab(e)}
                    items={[
                        { key: tabsKey.UNPAID, label: `Unpaid`, icon: <ClockCircleOutlined /> },
                        { key: tabsKey.PAID, label: `Paid`, icon: <WalletOutlined /> },
                    ]}
                />
            </div>
            {activeTab === tabsKey.UNPAID && <UnpaidOrders />}
            {activeTab === tabsKey.PAID && <PaidOrders />}
        </div >
    )
}

