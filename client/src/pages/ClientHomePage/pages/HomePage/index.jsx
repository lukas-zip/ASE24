import './index.less'
import { useSelector } from 'react-redux';
import CardVertical from '../../../../Components/Card/CardVertical';
import { Input, message } from 'antd';
import { EnvironmentTwoTone } from '@ant-design/icons';
import COLORS from '../../../../constants/COLORS';
import { useEffect, useState } from 'react';
import { getAllProductsByShopId } from '../../../../api/user.api';
import CONSTANTS from '../../../../constants';
import Product_Categories_PIC from '../../../../assets/pic/product-categories';
const { Search } = Input
export default function UserHomePage() {
    const { user } = useSelector(state => state.user)
    const onSearch = async () => {

    }
    const [firstProducts, setFirstProducts] = useState([])
    useEffect(() => {
        const getFirstProducts = async () => {
            await getAllProductsByShopId("99b725e9-1565-4e33-85e8-ef8a0e241abe").then(res => {
                if (res.status) {
                    setFirstProducts(res.value)
                } else {
                    message.error(res.message)
                }
            }).catch(err => {
                message.error("Error")
            })
        }
        getFirstProducts()
    }, [])
    return (
        <div className={`productPage`} style={{}}>
            {/* <div className={"overflowAuto"} style={{ flex: 1, display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 20 }}> */}
            <div className={`productPage-header`}>
                <div className={`productPage-header-searchBox`}>
                    <Search placeholder='Search product Here' style={{ width: 360 }} size="large" allowClear onSearch={onSearch} />
                </div>
                <div className={`productPage-header-address`}>
                    <EnvironmentTwoTone twoToneColor="#3d3d3d" style={{ fontSize: 18 }} />
                    <div style={{ marginLeft: 6, }} >
                        <div style={{ fontSize: 12, color: COLORS.commentText, userSelect: 'none' }}>Deliver to</div>
                        <div style={{ fontSize: 14, cursor: 'pointer' }}>your address</div>
                    </div>
                </div>
            </div>
            <div className='productPage-categories'>
                <div className='productPage-categories-title'>
                    <div>{"Categories".toUpperCase()}</div>
                </div>
                <div className='productPage-categories-box'>
                    {CONSTANTS.CATEGORIES.map((item, key) =>
                        <div className={`productPage-categories-box-item`} key={key}>
                            <img style={{ width: 100, height: 100, borderRadius: "50%", objectFit: "cover" }} src={Product_Categories_PIC[item]}></img>
                            <div className='productPage-categories-box-item-title'>{item}</div>
                        </div>)}
                </div>
            </div>
            <div className='productPage-container'>
                <div className='productPage-container-box'>
                    {firstProducts.map((item, key) => <CardVertical product={item} key={key} />)}
                </div>
            </div>
        </div >
    )
}
