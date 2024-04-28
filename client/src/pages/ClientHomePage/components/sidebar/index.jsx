import React, { useState, useRef, useEffect } from 'react'
import { HomeTwoTone, IdcardTwoTone, UserOutlined, FileTextTwoTone, ShoppingTwoTone } from '@ant-design/icons';
import { Avatar, Popover, Button, message, Popconfirm } from 'antd';
import './index.less'
import { useSelector, useDispatch } from 'react-redux'
import { useLocation, useNavigate } from 'react-router-dom';
import APPTHEME from '@/constants/COLORS/APPTHEME';
import LOGO from '@/assets/pic/swan_logo.png'
import PROJECT_VARIABLE from '@/constants/ProjectNameVariable';
import { setUser } from '../../../../store/user.store';

export default function Sidebar() {
    const THEME = APPTHEME["light"]
    const { user } = useSelector((state) => state.user)
    const dispatch = useDispatch()
    const [clicked, setClicked] = useState(false);
    const [navShrink, setNavShrink] = useState()
    const navigateTo = useNavigate()
    useEffect(() => {
        handleResize()
        window.addEventListener('resize', handleResize);
        return () => window.removeEventListener('resize', handleResize);
    }, [])
    const navRef = useRef(null);
    const handleResize = () => { navRef.current && setNavShrink(navRef.current.offsetWidth < 90) }
    const handleClickChange = (open) => {
        setClicked(open);
    };
    const Logout = () => {
        dispatch(setUser(null))
        navigateTo('/login')
        message.success('Logout successfully!');
    }
    const location = useLocation()
    const [selecetedNavItem, setSelectedNavItem] = useState(location.pathname.split('/')[2])
    useEffect(() => {
        setSelectedNavItem(location.pathname.split('/')[2])
    }, [location])
    const navObjs = [
        { value: 'home', icon: () => <HomeTwoTone className={navShrink ? 'navigationCenteredItem' : 'navigationItem'} twoToneColor={selecetedNavItem === 'home' ? '#4e8df5' : "#3d3d3d"} style={{ fontSize: 18 }} /> },
        { value: 'cart', icon: () => <ShoppingTwoTone className={navShrink ? 'navigationCenteredItem' : 'navigationItem'} twoToneColor={selecetedNavItem === 'cart' ? '#4e8df5' : "#3d3d3d"} style={{ fontSize: 18 }} /> },
        { value: 'profile', icon: () => <IdcardTwoTone className={navShrink ? 'navigationCenteredItem' : 'navigationItem'} twoToneColor={selecetedNavItem === 'profile' ? '#4e8df5' : "#3d3d3d"} style={{ fontSize: 18 }} /> },
    ]
    const navigationItem = (value, Icon) => {
        return <div key={value} className={`navigation navigation-light`} ref={navRef} onClick={() => navigateTo(`${value}`)}>
            <Icon />
        </div>
    }
    return (
        <div className={`sidebar`} style={{ backgroundColor: THEME.contentColor }}>
            <div className='content'>
                <div className='logo' style={{ cursor: 'pointer' }} onClick={() => navigateTo('/')}>
                    <div className='logoPic' style={{ marginBottom: 10, width: 40, height: 40 }}>
                        <img style={{ maxHeight: '100%', width: 'auto', height: 'auto', objectFit: 'cover' }} src={LOGO} />
                    </div>
                    {PROJECT_VARIABLE.PROJECT_NAME}
                </div>
                <div className='navigationBar'>
                    {navObjs.map(nav => navigationItem(nav.value, nav.icon))}
                </div >
                <div className='avator'>
                    <Popover
                        content={
                            <div>
                                <Popconfirm
                                    title={'Confirm Logout?'}
                                    onConfirm={Logout}
                                    okText={'Yes'}
                                    cancelText={'No'}
                                >
                                    <Button style={{ marginTop: 5 }} type="primary" danger>
                                        {'Logout'}
                                    </Button>
                                </Popconfirm>
                            </div>
                        }
                        placement="rightBottom"
                        trigger="click"
                        open={clicked}
                        onOpenChange={handleClickChange}
                    >
                        <Avatar
                            src={user.profile_picture}
                            size={{
                                xs: 36,
                                sm: 36,
                                md: 36,
                                lg: 50,
                                xl: 54,
                                xxl: 70,
                            }}
                            icon={<UserOutlined />}
                        />
                    </Popover>
                </div>
            </div >
        </div >
    )
}
