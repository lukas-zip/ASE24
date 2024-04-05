import React, { useEffect, useState } from 'react'
import { Avatar, message, Modal, Tag, Skeleton, List, Popover, Rate, Divider, InputNumber } from 'antd'
import { useSelector } from 'react-redux'
import { UserOutlined, LikeFilled, EllipsisOutlined, } from '@ant-design/icons';
import MyCarousel from '@/Components/myCarousel'
import "./index.less"
import { useNavigate } from 'react-router-dom';

export default function ProductDetailModal({ item, isOpen, setIsOpen }) {
    const navigateTo = useNavigate()
    const [itemInfo, setItemInfo] = useState(item)
    const { title = "mocktitle", content = "mockcontent", reviews = [], imgUrl = ["https://archive.trufflesuite.com/img/docs/ganache/ganache-home-empty.png"], tags = ["1", "34dsf"], price = 100 } = itemInfo || {}
    const { user } = useSelector((state) => state.user)
    const [quantity, setQuantity] = useState(1)
    const getUserData = async () => {
    }
    const getBlogComments = async () => {
    }
    useEffect(() => {
        getUserData();
        getBlogComments()
    }, [])
    const handleOk = () => {
        setIsOpen(false);
    };
    const handleCloseDetailModal = (e) => {
        e.stopPropagation();
        setIsOpen(false);
    };
    return (
        <Modal destroyOnClose={true} style={{ top: 60 }} styles={{ body: { height: '80vh' }, mask: { 'opacity': 0.8, backgroundColor: '#000' } }} width={"80%"} footer={null} open={isOpen} onOk={handleOk} onCancel={handleCloseDetailModal}>
            <div className={`BlogModal BlogModal-light`} >
                {imgUrl.length !== 0 && <div className='blogImg'><MyCarousel imgArr={imgUrl} /></div>}
                <div className={`blogMainPart`} >
                    <div className='blogInfo'>
                        <div className='blogTitle'>{title}dsfsdfkjas;dfjkasd;fjkas;lfjkaslkfjasdlfhaslkdfha;sdjfk;alsdja;sljkf;lkadjf;lasjkdf;lasdkj;asldjk;lasddjk;ladsjk;las</div>
                        <div className='blogDescri'>{content}</div>
                        <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                            <div style={{ fontSize: 14, color: 'rgb(170, 170, 170)' }}>19 sold</div>
                            <div style={{ display: 'flex', alignItems: 'center' }}>
                                <span style={{ fontSize: 14 }}>{3}&nbsp;</span>
                                <Rate defaultValue={3} disabled style={{ fontSize: 14 }} />
                                <span style={{ cursor: 'pointer', marginLeft: 10, fontSize: 12, color: '#306f83' }}>
                                    <span>34234&nbsp;</span>
                                    <span>ratings</span>
                                </span>
                            </div>
                        </div>
                        <div className='tags'>
                            {tags.map((tag, index) => <Tag key={index} bordered={false} color="processing">
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
                            <div style={{ display: 'flex', alignItems: 'baseline', fontSize: 16, gap: 2, fontWeight: 'bold', color: '#4790ff' }}>
                                <div>CHF</div>
                                <div style={{ fontSize: 20 }}>{price}</div>
                            </div>
                            <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
                                <div style={{ fontWeight: 'bold' }}>Quantity: </div>
                                <div><InputNumber min={1} max={6} defaultValue={quantity} onChange={(num) => setQuantity(num)} /></div>
                            </div>
                        </div>
                        <div className='CheckOutBtn'>Check Out: {price * quantity}</div>
                    </div>
                    <div className='blogComments'>
                        <div style={{ fontSize: 16, fontWeight: 'bold' }}>Item reviews ({reviews.length})</div>
                        <List
                            className="demo-loadmore-list"
                            itemLayout="horizontal"
                            size='small'
                            noDataText="No reviews"
                            dataSource={reviews}
                            renderItem={(item) => (
                                <List.Item
                                    actions={[<div className='btn' onClick={() => { }}><LikeFilled />&nbsp;{ }</div>, <div className='btn'><Popover content={<></>} trigger="click"><EllipsisOutlined onClick={() => { }} /></Popover></div>]}
                                >
                                    <Skeleton avatar loading={false} active>
                                        <List.Item.Meta
                                            // avatar={<Avatar size={49} src={noGender} />}
                                            avatar={<Avatar size={49} />}
                                            title={<a href="#">comment</a>}
                                            description={"description"}
                                        />
                                    </Skeleton>
                                </List.Item>
                            )}
                        />
                    </div>
                </div>
            </div >
        </Modal>
    )
}
