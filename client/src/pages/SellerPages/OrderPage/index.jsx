import COLORS from '@/constants/COLORS';
import './index.less'
import { Divider, Tabs } from 'antd';
import { useState } from 'react';
import { useSelector } from 'react-redux';
import EmptyBox from '@/assets/pic/EmptyBox.png'
import { useNavigate } from 'react-router-dom';
import OrderCard from './Components/Order';
import { CarOutlined, ClockCircleOutlined, WalletOutlined } from '@ant-design/icons';
import ProccessedOrders from './Components/ProccessedOrders';

const tabsKey = {
    PROCESSED: "Processed",
    DELIVERED: "Delivered",
    SHIPPED: "Shipped"
}
export default function OrderPage() {
    const navigateTo = useNavigate()
    const [activeTab, setActiveTab] = useState(tabsKey.PROCESSED)
    return (
        <div className='containerWrapper' style={{ margin: 10 }}>
            <div className='ShoppingCartPage-header'>
                <div className='ShoppingCartPage-header-title'>All Orders</div>
                <Tabs
                    defaultActiveKey={activeTab}
                    onChange={(e) => setActiveTab(e)}
                    items={[
                        { key: tabsKey.PROCESSED, label: tabsKey.PROCESSED, icon: <WalletOutlined /> },
                        { key: tabsKey.DELIVERED, label: tabsKey.DELIVERED, icon: <ClockCircleOutlined /> },
                        { key: tabsKey.SHIPPED, label: tabsKey.SHIPPED, icon: <CarOutlined /> }
                    ]}
                />
            </div>
            {activeTab === tabsKey.PROCESSED && <ProccessedOrders />}
            {activeTab === tabsKey.DELIVERED && <ProccessedOrders />}
            {activeTab === tabsKey.SHIPPED && <ProccessedOrders />}
        </div >
    )
}

