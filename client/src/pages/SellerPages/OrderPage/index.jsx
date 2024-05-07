import COLORS from '@/constants/COLORS';
import './index.less'
import { Divider, Tabs } from 'antd';
import { useState } from 'react';
import { useSelector } from 'react-redux';
import EmptyBox from '@/assets/pic/EmptyBox.png'
import { useNavigate } from 'react-router-dom';
import OrderCard from './Components/OrderCard';
import { CarOutlined, ClockCircleOutlined, WalletOutlined } from '@ant-design/icons';
import UnpaidOrders from './Components/UnpaidOrders';

const tabsKey = {
    UNPAID: "Unpaid",
    PAID: "Paid"
}
export default function OrderPage() {
    const navigateTo = useNavigate()
    const [activeTab, setActiveTab] = useState(tabsKey.UNPAID)
    return (
        <div className='containerWrapper' style={{ margin: 10 }}>
            <div className='ShoppingCartPage-header'>
                <div className='ShoppingCartPage-header-title'>All Orders</div>
                <Tabs
                    defaultActiveKey={activeTab}
                    onChange={(e) => setActiveTab(e)}
                    items={[
                        { key: tabsKey.UNPAID, label: tabsKey.UNPAID, icon: <ClockCircleOutlined /> },
                        { key: tabsKey.PAID, label: tabsKey.PAID, icon: <WalletOutlined /> },
                    ]}
                />
            </div>
            {activeTab === tabsKey.UNPAID && <UnpaidOrders />}
            {activeTab === tabsKey.PAID && <UnpaidOrders />}
        </div >
    )
}

