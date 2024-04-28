import COLORS from '@/constants/COLORS';
import './index.less'
import { Divider, Tabs } from 'antd';
import { useState } from 'react';
import { useSelector } from 'react-redux';
import EmptyBox from '@/assets/pic/EmptyBox.png'
import { useNavigate } from 'react-router-dom';
import OrderCard from './Components/Order';
import { CarOutlined, ClockCircleOutlined, WalletOutlined } from '@ant-design/icons';
import UnpaidOrders from './Components/UnpaidOrders';

const tabsKey = {
    UNPAID: "unpaid",
    UNDELIVERED: "undelivered",
    RECEIVED: "received"
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
                        { key: tabsKey.UNPAID, label: `Unpaid`, icon: <WalletOutlined /> },
                        { key: tabsKey.UNDELIVERED, label: `Undelivered`, icon: <ClockCircleOutlined /> },
                        { key: tabsKey.RECEIVED, label: `Received`, icon: <CarOutlined /> }
                    ]}
                />
            </div>
            {activeTab === tabsKey.UNPAID && <UnpaidOrders />}
        </div >
    )
}

