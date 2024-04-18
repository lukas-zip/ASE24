import COLORS from '@/constants/COLORS';
import './index.less'
import CardVertical from '@/Components/Card/CardVertical';
import { LeftOutlined, UserOutlined } from '@ant-design/icons';
import { Avatar, Divider, Empty, message, } from 'antd';
import { useLoaderData, useNavigate, useParams } from 'react-router-dom';
import { useEffect, useState } from 'react';
import { getAllProductsByShopId } from '@/api/user.api';
export default function ShopDetailPage() {
    const navigateTo = useNavigate()
    const shop = useLoaderData()
    const { profile_picture, phone, address, email, shop_name } = shop
    const { shopID } = useParams()
    const [allProducts, setAllProducts] = useState([])

    const getAllProducts = async () => {
        await getAllProductsByShopId(shopID).then(res => {
            if (res.status) {
                setAllProducts(res.value)
            } else {
                message.error(res.message)
            }
        }).catch(err => {
            message.error("Error")
        })
    }
    useEffect(() => {
        getAllProducts()
    }, [])

    return (
        <div className={`ShopDetailPage`} style={{}}>
            <div className='ShopDetailPage-header' style={{}}>
                <div onClick={() => navigateTo(-1)} style={{ fontSize: 20, display: 'flex', userSelect: 'none', cursor: 'pointer', alignItems: 'center', color: COLORS.commentText, fontWeight: 500, justifyContent: 'center', backgroundColor: "#fff", padding: "0 16px", height: 50, borderRadius: 18, marginRight: 10 }}>
                    <LeftOutlined /> Back
                </div>
            </div>
            <div className='ShopDetailPage-mainContent'>
                <div className='ShopDetailPage-shopInfo'>
                    <div className='ShopDetailPage-shopInfo-name'>
                        <Avatar icon={<UserOutlined />} src={profile_picture} size={60} />
                        <div>
                            <div>{shop_name}</div>
                            <a style={{ color: COLORS.primary, fontSize: 14 }} href={`mailto:${email}`}>Connect Us</a>
                        </div>
                    </div>
                    <div className='ShopDetailPage-shopInfo-details'>
                        <div className='ShopDetailPage-shopInfo-details-item'>
                            <div className='ShopDetailPage-shopInfo-details-item-number'>
                                {allProducts.length}
                            </div>
                            <div className='ShopDetailPage-shopInfo-details-item-title' style={{ color: COLORS.commentText }}>
                                Sold
                            </div>
                        </div>
                        <div style={{ height: 20, width: 2, backgroundColor: "#646464" }}></div>
                        <div className='ShopDetailPage-shopInfo-details-item'>
                            <div className='ShopDetailPage-shopInfo-details-item-number'>
                                {allProducts.length}
                            </div>
                            <div className='ShopDetailPage-shopInfo-details-item-title' style={{ color: COLORS.commentText }}>
                                Items
                            </div>
                        </div>
                    </div>
                </div>
                <Divider />
                <div className='ShopDetailPage-categories'>
                    <div className='ShopDetailPage-allProducts'>
                        {Object.keys(allProducts).map((item, key) => <div className={`ShopDetailPage-allProducts-item`} key={key}>
                            {allProducts !== 0 && <div className='ShopDetailPage-allProducts-item-content' >
                                {allProducts.map((item, key) => <CardVertical product={item} key={key} />)}
                                {allProducts.map((item, key) => <CardVertical product={item} key={key} />)}
                                {allProducts.map((item, key) => <CardVertical product={item} key={key} />)}
                                {allProducts.map((item, key) => <CardVertical product={item} key={key} />)}
                                {allProducts.map((item, key) => <CardVertical product={item} key={key} />)}
                                {allProducts.map((item, key) => <CardVertical product={item} key={key} />)}
                                {allProducts.map((item, key) => <CardVertical product={item} key={key} />)}
                                {allProducts.map((item, key) => <CardVertical product={item} key={key} />)}
                                {allProducts.map((item, key) => <CardVertical product={item} key={key} />)}
                                {allProducts.map((item, key) => <CardVertical product={item} key={key} />)}
                                {allProducts.map((item, key) => <CardVertical product={item} key={key} />)}
                                {allProducts.map((item, key) => <CardVertical product={item} key={key} />)}
                                {allProducts.map((item, key) => <CardVertical product={item} key={key} />)}
                                {allProducts.map((item, key) => <CardVertical product={item} key={key} />)}
                                {allProducts.map((item, key) => <CardVertical product={item} key={key} />)}
                                {allProducts.map((item, key) => <CardVertical product={item} key={key} />)}
                                {allProducts.map((item, key) => <CardVertical product={item} key={key} />)}
                                {allProducts.map((item, key) => <CardVertical product={item} key={key} />)}
                                {allProducts.map((item, key) => <CardVertical product={item} key={key} />)}
                                {allProducts.map((item, key) => <CardVertical product={item} key={key} />)}
                                {allProducts.map((item, key) => <CardVertical product={item} key={key} />)}
                                {allProducts.map((item, key) => <CardVertical product={item} key={key} />)}
                                {allProducts.map((item, key) => <CardVertical product={item} key={key} />)}
                                {allProducts.map((item, key) => <CardVertical product={item} key={key} />)}
                                {allProducts.map((item, key) => <CardVertical product={item} key={key} />)}
                                {allProducts.map((item, key) => <CardVertical product={item} key={key} />)}
                                {allProducts.map((item, key) => <CardVertical product={item} key={key} />)}
                                {allProducts.map((item, key) => <CardVertical product={item} key={key} />)}
                                {allProducts.map((item, key) => <CardVertical product={item} key={key} />)}
                                {allProducts.map((item, key) => <CardVertical product={item} key={key} />)}
                                {allProducts.map((item, key) => <CardVertical product={item} key={key} />)}
                                {allProducts.map((item, key) => <CardVertical product={item} key={key} />)}
                                {allProducts.map((item, key) => <CardVertical product={item} key={key} />)}
                                {allProducts.map((item, key) => <CardVertical product={item} key={key} />)}
                                {allProducts.map((item, key) => <CardVertical product={item} key={key} />)}
                                {allProducts.map((item, key) => <CardVertical product={item} key={key} />)}
                                {allProducts.map((item, key) => <CardVertical product={item} key={key} />)}
                                {allProducts.map((item, key) => <CardVertical product={item} key={key} />)}
                                {allProducts.map((item, key) => <CardVertical product={item} key={key} />)}
                                {allProducts.map((item, key) => <CardVertical product={item} key={key} />)}
                            </div>}
                            {allProducts.length !== 0 && <div style={{ color: COLORS.commentText, marginTop: 20, display: 'flex', alignItems: 'center', justifyContent: 'center', }}>
                                --No more products--
                            </div>}

                        </div>)}
                        {allProducts.length === 0 && <div className='ShopDetailPage-allProducts-item-content-empty' >
                            <Empty description={"No products"} />
                        </div>}
                    </div>
                </div>
            </div>
        </div >
    )
}
