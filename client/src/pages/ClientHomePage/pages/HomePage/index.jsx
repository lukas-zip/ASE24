import './index.less'
import { useSelector } from 'react-redux';
import CardVertical from '@/Components/Card/CardVertical';
import { Button, Empty, Input, message } from 'antd';
import { EnvironmentTwoTone, RightOutlined } from '@ant-design/icons';
import COLORS from '@/constants/COLORS';
import { useEffect, useState } from 'react';
import { getAllProductsByShopId, getProductByCategory, searchProducts } from '@/api/user.api';
import CONSTANTS from '@/constants';
import Product_Categories_PIC from '@/assets/pic/product-categories';
import { useNavigate } from 'react-router-dom';
const { Search } = Input
export default function UserHomePage() {
    const { user } = useSelector(state => state.user)
    const onSearch = async (searchTerm) => {
        await searchProducts(searchTerm).then(res => {
            if (res.status) {
                navigateTo(`category/${searchTerm}`, { state: { allProducts: res.value } })
            } else {
                message.error(res.message)
            }
        }).catch(err => {
            message.error("Error")
        })
    }
    const [allCategoriesProducts, setAllCategoriesProducts] = useState(CONSTANTS.CATEGORIES.reduce((acc, cur) => {
        acc[cur] = []
        return acc
    }, {}))
    useEffect(() => {
        const requestProductsByCategory = async () => {
            CONSTANTS.CATEGORIES.forEach(async (item, key) => {
                await getProductByCategory(item).then(res => {
                    if (res.status) {
                        setAllCategoriesProducts(prevState => {
                            return {
                                ...prevState,
                                [item]: res.value
                            };
                        })
                    } else {
                        message.error(res.message)
                    }
                }).catch(err => {
                    message.error("Error")
                })
            })
        }
        requestProductsByCategory()
    }, [])

    // navigate
    const navigateTo = useNavigate()
    return (
        <div className={`productPage`} style={{}}>
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
            <div className='productPage-mainContent'>
                <div className='productPage-categories'>
                    <div className='productPage-categories-title'>
                        <div>{"All Categories".toUpperCase()}</div>
                    </div>
                    <div className='productPage-categories-box'>
                        {CONSTANTS.CATEGORIES.map((item, key) =>
                            <div className={`productPage-categories-box-item`} onClick={() => navigateTo(`category/${item}`, { state: { allProducts: allCategoriesProducts[item] } })} key={key}>
                                <img style={{ width: 100, height: 100, borderRadius: "50%", objectFit: "cover" }} src={Product_Categories_PIC[item]}></img>
                                <div className='productPage-categories-box-item-title'>{item}</div>
                            </div>)}
                    </div>
                </div>
                <div className='productPage-allCategoriesProducts'>
                    {Object.keys(allCategoriesProducts).map((item, key) => <div className={`productPage-allCategoriesProducts-item`} key={key}>
                        <div className='productPage-allCategoriesProducts-item-title'>
                            <div>{item}</div>
                            {allCategoriesProducts[item].length !== 0 && <Button type='primary' onClick={() => navigateTo(`category/${item}`, { state: { allProducts: allCategoriesProducts[item] } })}>{allCategoriesProducts[item].length} products <RightOutlined /></Button>}
                        </div>
                        {allCategoriesProducts[item].length !== 0 && <div className='productPage-allCategoriesProducts-item-content' >
                            {allCategoriesProducts[item].slice(0, 5).map((item, key) => <CardVertical product={item} key={key} />)}
                        </div>}
                        {allCategoriesProducts[item].length === 0 && <div className='productPage-allCategoriesProducts-item-content-empty' >
                            <Empty description={"No related products"} />
                        </div>}
                    </div>)}
                </div>
            </div>
        </div >
    )
}
