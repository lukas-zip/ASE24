import React, { Suspense, useEffect } from 'react';
import "./index.less"
import { Layout, Menu, theme, } from 'antd';
import { Outlet, useLocation, useNavigate } from 'react-router-dom'
import MyLayoutHeader from './header';
import { useDispatch, useSelector } from 'react-redux';
import { setCollapsed } from '@/store/configuration.store'
import { DatabaseOutlined, HomeOutlined, MoneyCollectFilled, MoneyCollectOutlined, SettingOutlined, WalletOutlined } from '@ant-design/icons';

const { Content, Sider } = Layout;

const Dashboard = () => {
  const getItem = (label, router, icon, children) => {
    return { key: router, icon, children, label }
  }
  const mySidebarOptions = [
    getItem("Home", '/home', <HomeOutlined />),
    getItem("Statistic", '/statistic', <DatabaseOutlined />),
    getItem("Loan", '/loan', <MoneyCollectOutlined />),
    getItem("Savings", '/savings', <MoneyCollectFilled />),
    getItem("Budget", '/budget', <WalletOutlined />),
    getItem("Settings", '/settings', <SettingOutlined />),
  ]

  const { pathname } = useLocation()
  const collapsed = useSelector(state => state.configuration.collapsed)
  const dispatch = useDispatch()
  const { token: { colorBgContainer } } = theme.useToken()
  const navigateTo = useNavigate()
  const menuClick = (e) => navigateTo(e.key)
  useEffect(() => {
    pathname === '/' && navigateTo('/home')
  }, [pathname])
  return (
    <Layout className="layout-page" style={{ minHeight: '100vh' }}>
      <MyLayoutHeader />
      <Layout hasSider>
        <Sider style={{ background: colorBgContainer }} collapsible collapsed={collapsed} onCollapse={(value) => dispatch(setCollapsed(value))}>
          <Menu defaultSelectedKeys={['/home']} selectedKeys={[pathname]} mode="inline" items={mySidebarOptions} onClick={menuClick} />
        </Sider>
        <Content className='layout-page-content'>
          <Suspense fallback={null}>
            <Outlet />
          </Suspense>
        </Content>
      </Layout>
    </Layout >
  )
}
export default Dashboard;
