import React, { useEffect, useState } from 'react'
import { Avatar, message, Modal, Tag, Skeleton, List, Popover, Rate, Divider, InputNumber, Dropdown, Button, Input, Space } from 'antd'
import { useSelector } from 'react-redux'
import { UserOutlined, EditOutlined, EllipsisOutlined, DeleteOutlined, PlusOutlined, } from '@ant-design/icons';
import MyCarousel from '@/Components/myCarousel'
import "./index.less"
import { createReview, getReviewByProductId, getShopById } from '../../../../api/user.api';

const items = [
    {
        key: '1',
        danger: true,
        icon: <DeleteOutlined />,
        label: (
            <a target="_blank" rel="noopener noreferrer" href="https://www.antgroup.com">
                delete
            </a>
        ),
    },
    {
        key: '2',
        icon: <EditOutlined />,
        label: (
            <a target="_blank" rel="noopener noreferrer" href="https://www.aliyun.com">
                edit
            </a>
        ),
    }
]
const desc = ['terrible', 'bad', 'normal', 'good', 'wonderful'];
export default function ProductDetailModal({ item, isOpen, setIsOpen }) {
    const {
        product_assemblies,
        product_name,
        product_description,
        product_bom,
        product_picture,
        product_search_attributes,
        product_price,
        product_owner,
        product_price_reduction,
        product_id,
    } = item



    const [reviewsData, setReviews] = useState([])
    const [averageRating, setAverageRating] = useState(0)
    useEffect(() => {
        const totalRating = reviewsData.reduce((acc, review) => acc + Number(review.rating), 0)
        isNaN(totalRating / reviewsData.length) && setAverageRating(totalRating / reviewsData.length)
    }, [reviewsData])


    const { user: { user_id } } = useSelector((state) => state.user)
    const [quantity, setQuantity] = useState(1)
    const getReviews = async () => {
        await getReviewByProductId(product_id).then((res) => {
            if (res.status === true) {
                console.log(res.value[1].customer_id);
                setReviews(res.value)
            }
        }).catch((err) => {
            message.error(err.message)
        })
    }
    const getProductOwnerInfo = async () => {
        await getShopById(product_owner).then((res) => {
            if (res.status === true) {

            }
        })
    }
    useEffect(() => {
        getReviews();
        getProductOwnerInfo()
    }, [])
    const handleOk = () => {
        setIsOpen(false);
    };
    const handleCloseDetailModal = (e) => {
        e.stopPropagation();
        setIsOpen(false);
    };

    const [addReviewModalOpen, setAddReviewModalOpen] = useState(false);
    const [confirmLoading, setConfirmLoading] = useState(false);
    const [rate, setRate] = useState(0)
    const [review, setReview] = useState('')
    const handleAddReviewModalOpen = () => {
        setAddReviewModalOpen(true);
    }
    const handleSubmitReview = async () => {
        if (review && rate) {
            const newReview = {
                product_id,
                customer_id: user_id,
                reviewcontent: review,
                rating: rate,
                time_lastedit: "20.03.2024 - 11:50:00",
                time_created: "20.03.2024 - 11:50:00"
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
            }).catch(err => {
                setRate(0)
                setReview('')
                setConfirmLoading(false)
            })

        } else {
            message.error("Please complete all the content");
        }
    }
    return (
        <Modal destroyOnClose={true} style={{ top: 60 }} styles={{ body: { height: '80vh' }, mask: { 'opacity': 0.8, backgroundColor: '#000' } }} width={"80%"} footer={null} open={isOpen} onOk={handleOk} onCancel={handleCloseDetailModal}>
            <div className={`BlogModal BlogModal-light`} >
                <div className='blogImg'><MyCarousel imgArr={product_picture} /></div>
                <div className={`blogMainPart`} >
                    <div className='blogInfo'>
                        <div className='blogTitle'>{product_name}</div>
                        <div className='blogDescri'>{product_description}</div>
                        <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                            <div style={{ fontSize: 14, color: 'rgb(170, 170, 170)' }}>{product_assemblies} Product</div>
                            <div style={{ display: 'flex', alignItems: 'center' }}>
                                {/* <span style={{ fontSize: 14 }}>{averageRating}&nbsp;</span> */}
                                <span style={{ fontSize: 14 }}>{"-"}&nbsp;</span>
                                <Rate defaultValue={averageRating} disabled style={{ fontSize: 14 }} />
                                <span style={{ cursor: 'pointer', marginLeft: 10, fontSize: 12, color: '#306f83' }}>
                                    <span>{reviewsData.length}&nbsp;</span>
                                    <span>ratings</span>
                                </span>
                            </div>
                        </div>
                        <div className='tags'>
                            {product_search_attributes.map((tag, index) => <Tag key={index} bordered={false} color="processing">
                                <span>#{tag}</span>
                            </Tag>)}
                        </div>
                        <div className='blogOperation'>
                            <div className='Info buttonHover' onClick={() => {
                                // navigateTo(`/chat/contacts/detail/${user._id}`)
                            }}>
                                <Avatar size={30} icon={<UserOutlined />} src={''} />
                                <div className='Info-sub'>
                                    <div style={{ fontSize: 14, fontWeight: 'bold' }}>{"Store Name"}</div>
                                    <div style={{ color: '#306f83' }}>{"Visit the Store"}</div>
                                </div>
                            </div>
                        </div>
                        <Divider />
                        <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                            <div style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
                                <div style={{ display: 'flex', alignItems: 'baseline', fontSize: 16, gap: 2, fontWeight: 'bold', color: '#4790ff' }}>
                                    <div>CHF</div>
                                    <div style={{ fontSize: 26 }}>{(product_price * (100 - product_price_reduction) / 100).toPrecision(2)}</div>
                                </div>
                                {(100 - product_price_reduction) != 0 && <><div style={{ color: '#4790ff', fontSize: 14, borderRadius: 6, padding: "0 6px", border: "1px solid #4790ff" }}>-{product_price_reduction}%</div>
                                    <div style={{ color: 'rgb(170, 170, 170)', fontSize: 14, textDecoration: 'line-through' }}>{product_price}</div>
                                </>}
                            </div>
                            <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
                                <div style={{ fontWeight: 'bold' }}>Quantity: </div>
                                <div><InputNumber min={1} max={6} defaultValue={quantity} onChange={(num) => setQuantity(num)} /></div>
                            </div>
                        </div>
                        <div className='CheckOutBtn'>Add to cart</div>
                    </div>
                    <div className='blogComments'>
                        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                            <div style={{ fontSize: 16, fontWeight: 'bold' }}>Item reviews ({reviewsData.length})</div>
                            <div
                                onClick={() => handleAddReviewModalOpen()}
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
                                            {user_id === item.customer_id && <Dropdown Dropdown menu={{ items }} placement="top" arrow={{ pointAtCenter: true }}>
                                                <EllipsisOutlined onClick={() => { }} />
                                            </Dropdown>}
                                        </div>
                                    ]}
                                >
                                    <Skeleton avatar loading={false} active>
                                        <List.Item.Meta
                                            // avatar={<Avatar size={49} src={noGender} />}
                                            avatar={<Avatar size={36} />}
                                            title={<a href="#">User</a>}
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
        </Modal >
    )
}
