import React, { useEffect, useState } from 'react'
import { Avatar, message, Modal, Tag, Skeleton, List, Popover, Rate, Divider, InputNumber, Dropdown, Button, Input, Space } from 'antd'
import { useSelector } from 'react-redux'
import { UserOutlined, EditOutlined, EllipsisOutlined, DeleteOutlined, PlusOutlined, } from '@ant-design/icons';
import MyCarousel from '@/Components/myCarousel'
import "./index.less"
import { addProductIntoOrder, createOrder, createReview, deleteReview, getReviewByProductId, getShopById, updateReview } from '../../../../api/user.api';
import { formatNumber } from '@/utils/FormatNumber';
import { useNavigate } from 'react-router-dom';
import { useStateContext } from '../../context';
import { myDebounceFunc } from '@/utils/debounceFunc';

const desc = ['terrible', 'bad', 'normal', 'good', 'wonderful'];
export default function ProductDetailModal({ item, isOpen, setIsOpen }) {
    const navigateTo = useNavigate()
    const { getOrders, orders, unpaidOrders } = useStateContext()
    const { user: { user_id } } = useSelector((state) => state.user)
    const {
        product_assemblies,
        product_name,
        product_description,
        product_picture,
        product_search_attributes,
        product_current_stock,
        product_price,
        product_owner,
        product_price_reduction,
        product_id,
    } = item

    // review function
    const [confirmLoading, setConfirmLoading] = useState(false);
    const [addReviewModalOpen, setAddReviewModalOpen] = useState(false);
    const [updateReviewModalOpen, setUpdateReviewModalOpen] = useState(false);
    const [rate, setRate] = useState(0)
    const [review, setReview] = useState('')
    const handleSubmitReview = async () => {
        if (review && rate) {
            const newReview = {
                product_id,
                customer_id: user_id,
                reviewcontent: review,
                rating: rate.toString(),
            }
            setConfirmLoading(true);
            await createReview(newReview).then((msg) => {
                if (msg.status === true) {
                    message.success("Add review successfully!")
                    setAddReviewModalOpen(false)
                } else {
                    message.error(msg.message)
                }
                setRate(0)
                setReview('')
                setConfirmLoading(false)
                getReviews()
            }).catch(err => {
                setRate(0)
                setReview('')
                setConfirmLoading(false)
            })
        } else {
            message.error("Please complete all the content");
        }
    }
    const [selectedReview, setSelectedReview] = useState(null)
    const handleUpdateReview = async () => {
        if (review && rate && selectedReview?.review_id) {
            const newReview = {
                product_id,
                review_id: selectedReview.review_id,
                customer_id: user_id,
                reviewcontent: review,
                rating: rate.toString(),
            }
            setConfirmLoading(true);
            await updateReview(newReview).then((msg) => {
                if (msg.status === true) {
                    message.success("Update review successfully!")
                    setUpdateReviewModalOpen(false)
                    getReviews()
                } else {
                    message.error(msg.message)
                }
                setRate(0)
                setReview('')
                setConfirmLoading(false)
            }).catch(err => {
                setRate(0)
                setReview('')
                setConfirmLoading(false)
            })
        } else {
            message.error("Please complete all the content");
        }
    }
    const DeleteReview = async (reviewId) => {
        const reqData = {
            review_id: reviewId,
            product_id,
            customer_id: user_id,
        }
        await deleteReview(reqData).then((msg) => {
            if (msg.status === true) {
                message.success("Delete review successfully!")
                getReviews()
            } else {
                message.error(msg.message)
            }
        }).catch(err => {
            message.error(err.message)
        })
    }
    const [reviewsData, setReviews] = useState([])
    const [averageRating, setAverageRating] = useState(0)
    useEffect(() => {
        const totalRating = reviewsData.reduce((acc, review) => acc + Number(review.rating), 0)
        !isNaN(totalRating / reviewsData.length) && setAverageRating(totalRating / reviewsData.length)
    }, [reviewsData])
    const getReviews = async () => {
        await getReviewByProductId(product_id).then((res) => {
            if (res.status === false && res.message?.length === 0) {
                setReviews([])
            }
            if (res.status === true) {
                console.log("zhe", res.value);
                setReviews(res.value)
            }
        }).catch((err) => {
            message.error(err.message)
        })
    }


    // get Shop info
    const [ShopInfo, setShopInfo] = useState({ shop_name: "", profile_picture: "", shop_description: "" })
    const getProductOwnerInfo = async () => {
        await getShopById(product_owner).then((res) => {
            if (res.status === true) {
                setShopInfo(res.value)
            }
        })
    }
    useEffect(() => {
        getReviews();
        getProductOwnerInfo()
    }, [])

    // order
    const [quantity, setQuantity] = useState(1)
    const AddToChart = async () => {
        if (unpaidOrders.length === 0) {
            console.log("zhele no");
            const reqData = {
                product_id,
                quantity,
                user_id: user_id,
            }
            await createOrder(reqData).then((res) => {
                console.log(res);
                getOrders()
                message.success("Add to cart successfully!")
                setIsOpen(false)
            })
        } else {
            console.log("zhele you");
            const reqData = {
                product_id,
                quantity,
            }
            await addProductIntoOrder(unpaidOrders[0].order_id, reqData).then((res) => {
                if (res.status) {
                    getOrders()
                    message.success("Add to cart successfully!")
                    setIsOpen(false)
                } else {
                    message.error(res.message.value)
                }
            })
        }
    }
    const debouncedAddToCart = myDebounceFunc(AddToChart, 500)
    return (
        <Modal destroyOnClose={true} style={{ top: 60 }} styles={{ body: { height: '80vh' }, mask: { 'opacity': 0.8, backgroundColor: '#000' } }} width={"80%"} footer={null} open={isOpen}
            onOk={() => setIsOpen(false)}
            onCancel={(e) => {
                e.stopPropagation()
                setIsOpen(false)
            }}>
            <div className={`BlogModal BlogModal-light`} >
                <div className='blogImg'><MyCarousel imgArr={product_picture} /></div>
                <div className={`blogMainPart`} >
                    <div className='blogInfo'>
                        <div className='blogTitle'>{product_name}</div>
                        <div className='blogDescri'>{product_description}</div>
                        <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                            <div style={{ fontSize: 14, color: 'rgb(170, 170, 170)' }}>{product_assemblies} Product</div>
                            {(averageRating && averageRating !== 0) ? !isNaN(averageRating) && <div style={{ display: 'flex', alignItems: 'center' }}>
                                {/* <span style={{ fontSize: 14 }}>{averageRating}&nbsp;</span> */}
                                <span style={{ fontSize: 14 }}>{averageRating}&nbsp;</span>
                                <Rate defaultValue={averageRating} disabled style={{ fontSize: 14 }} />
                                <span style={{ cursor: 'pointer', marginLeft: 10, fontSize: 12, color: '#306f83' }}>
                                    <span>{reviewsData.length}&nbsp;</span>
                                    <span>ratings</span>
                                </span>
                            </div> : <div></div>}
                        </div>
                        <div className='tags'>
                            {product_search_attributes.map((tag, index) => <Tag key={index} bordered={false} color="processing">
                                <span>#{tag}</span>
                            </Tag>)}
                        </div>
                        <div className='blogOperation'>
                            <div className='Info buttonHover' onClick={() => {
                                navigateTo(`/user/home/shop/${product_owner}`)
                            }}>
                                <Avatar size={30} icon={<UserOutlined />} src={ShopInfo.profile_picture} />
                                <div className='Info-sub'>
                                    <div style={{ fontSize: 14, fontWeight: 'bold' }}>{ShopInfo.shop_name}</div>
                                    <div style={{ color: '#306f83' }}>{"Visit the Store"}</div>
                                </div>
                            </div>
                        </div>
                        <Divider />
                        <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                            <div style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
                                <div style={{ display: 'flex', alignItems: 'baseline', fontSize: 16, gap: 2, fontWeight: 'bold', color: '#4790ff' }}>
                                    <div>CHF</div>
                                    <div style={{ fontSize: 26 }}>{formatNumber(product_price * (100 - product_price_reduction) / 100)}</div>
                                </div>
                                {(100 - product_price_reduction) != 0 && <><div style={{ color: '#4790ff', fontSize: 14, borderRadius: 6, padding: "0 6px", border: "1px solid #4790ff" }}>-{product_price_reduction}%</div>
                                    <div style={{ color: 'rgb(170, 170, 170)', fontSize: 14, textDecoration: 'line-through' }}>{product_price}</div>
                                </>}
                            </div>
                            <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
                                <div style={{ fontWeight: 'bold' }}>Quantity: </div>
                                <div><InputNumber min={1} max={product_current_stock} defaultValue={quantity} onChange={(num) => setQuantity(num)} /></div>
                            </div>
                        </div>
                        <div onClick={debouncedAddToCart} className='CheckOutBtn'>Add to cart</div>
                    </div>
                    <div className='blogComments'>
                        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                            <div style={{ fontSize: 16, fontWeight: 'bold' }}>Item reviews ({reviewsData.length})</div>
                            <div
                                onClick={() => setAddReviewModalOpen(true)}
                                style={{ cursor: 'pointer' }}
                            >
                                <PlusOutlined />
                            </div>
                        </div>
                        <List
                            className="demo-loadmore-list"
                            itemLayout="horizontal"
                            size='small'
                            dataSource={reviewsData}
                            renderItem={(item) => (
                                <List.Item
                                    actions={[
                                        <div className='btn'>
                                            {user_id === item.customer_id && <Dropdown Dropdown menu={
                                                {
                                                    items: [
                                                        {
                                                            key: '1',
                                                            danger: true,
                                                            icon: <DeleteOutlined />,
                                                            label: (<a>delete</a>),
                                                        },
                                                        {
                                                            key: '2',
                                                            icon: <EditOutlined />,
                                                            label: (<a>edit</a>),
                                                        }
                                                    ],
                                                    onClick: (e) => {
                                                        if (e.key === '1') {
                                                            DeleteReview(item.review_id)
                                                        } else if (e.key === '2') {
                                                            setSelectedReview(item)
                                                            setReview(item.reviewcontent)
                                                            setRate(item.rating)
                                                            setUpdateReviewModalOpen(true)
                                                        }
                                                    }
                                                }} placement="top" arrow={{ pointAtCenter: true }}>
                                                <EllipsisOutlined onClick={() => { }} />
                                            </Dropdown>}
                                        </div>
                                    ]}
                                >
                                    <Skeleton avatar loading={false} active>
                                        <List.Item.Meta
                                            // avatar={<Avatar size={49} src={noGender} />}
                                            avatar={<Avatar size={36} icon={<UserOutlined />} src={item?.customer?.profile_picture ? item.customer.profile_picture : ''} />}
                                            title={<a href="#">{item?.customer?.username ? item.customer?.username : "User"}</a>}
                                            description={<div>
                                                <Rate disabled defaultValue={Number(item.rating)} />
                                                <div>{item.reviewcontent}</div>
                                            </div>}
                                        />
                                    </Skeleton>
                                </List.Item>
                            )}
                        />
                    </div>
                </div>
            </div >
            <Modal title="Add Review" open={addReviewModalOpen} onOk={handleSubmitReview} onCancel={() => setAddReviewModalOpen(false)} confirmLoading={confirmLoading} okText="Submit">
                <div style={{ display: 'flex', alignItems: 'center', gap: 10, marginBottom: 10, }}>
                    <div>Rate: </div>
                    <Rate tooltips={desc} style={{ fontSize: 20 }} defaultValue={rate} onChange={(rateValue) => setRate(rateValue)} />
                </div>
                <Input.TextArea variant="filled" defaultValue={review} placeholder='Pleaset enter your review here' onChange={({ target: { value } }) => setReview(value)} rows={4} />
            </Modal>
            <Modal title="Update Review" open={updateReviewModalOpen} onOk={handleUpdateReview} onCancel={() => setUpdateReviewModalOpen(false)} confirmLoading={confirmLoading} okText="Submit">
                <div style={{ display: 'flex', alignItems: 'center', gap: 10, marginBottom: 10, }}>
                    <div>Rate: </div>
                    <Rate tooltips={desc} style={{ fontSize: 20 }} defaultValue={rate} onChange={(rateValue) => setRate(rateValue)} />
                </div>
                <Input.TextArea variant="filled" defaultValue={review} placeholder='Pleaset enter your review here' onChange={({ target: { value } }) => setReview(value)} rows={4} />
            </Modal>
        </Modal >
    )
}
