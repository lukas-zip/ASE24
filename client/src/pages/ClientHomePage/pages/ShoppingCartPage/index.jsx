import './index.less'
import { Tabs } from 'antd';
import { useState } from 'react';
import { ClockCircleOutlined, WalletOutlined } from '@ant-design/icons';
import UnpaidOrders from './Components/UnpaidOrders';
import PaidOrders from './Components/PaidOrders';
import { useStateContext } from '../../context';

const tabsKey = {
    UNPAID: "Unpaid",
    PAID: "Paid",
}
export default function ShoppingCartPage() {
    const { unpaidOrders, paidOrders } = useStateContext()
    const [activeTab, setActiveTab] = useState(tabsKey.UNPAID)
    return (
        <div className='containerWrapper'>
            <div className='ShoppingCartPage-header'>
                <div className='ShoppingCartPage-header-title'>Shopping Cart</div>
                <Tabs
                    defaultActiveKey={activeTab}
                    onChange={(e) => setActiveTab(e)}
                    items={[
                        { key: tabsKey.UNPAID, label: `${tabsKey.UNPAID} (${unpaidOrders?.length ? unpaidOrders?.length : 0})`, icon: <ClockCircleOutlined /> },
                        { key: tabsKey.PAID, label: `${tabsKey.PAID} (${paidOrders?.length ? paidOrders?.length : 0})`, icon: <WalletOutlined /> },
                    ]}
                />
            </div>
            {activeTab === tabsKey.UNPAID && <UnpaidOrders />}
            {activeTab === tabsKey.PAID && <PaidOrders />}
        </div >
    )
}

