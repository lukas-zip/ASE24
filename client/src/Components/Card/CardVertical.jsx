import './CardVertical.less'
import { Rate } from 'antd';
import { useEffect, useState } from 'react';
import ProductDetailModal from '../../pages/ClientHomePage/components/ProductDetailModal';
export default function CardVertical({ product, pic = "https://i.ytimg.com/vi/YmFuedpSldA/oar2.jpg?sqp=-oaymwEdCJUDENAFSFWQAgHyq4qpAwwIARUAAIhCcAHAAQY=&rs=AOn4CLA1Raa3y-da_nvF7O2G_Zsbwqo38A" }) {
  const { product_name, product_description, product_picture, product_price } = product
  const [detailModelOpen, setDetailModelOpen] = useState(false)
  const closeModal = () => {
    setDetailModelOpen(false)
  }
  return (
    <div onClick={() => {
      setDetailModelOpen(true)
    }} className={`tutorialCardVertical tutorialCardVertical-light`}>
      <div className='tutorialCardVertical-cover'>
        <img style={{ maxWidth: '100%', width: 'auto', height: 'auto', objectFit: 'cover' }} src={product_picture[0]} />
        <div className='tutorialCardVertical-cover-detail'>
          <div className='tutorialCardVertical-cover-detail-level'>Promote</div>
          <div className='tutorialCardVertical-cover-detail-duration'>100+ bought</div>
        </div>
      </div>
      <div className='tutorialCardVertical-bottom'>
        <div className={`tutorialCardVertical-bottom-desc`}>
          <div className='tutorialCardVertical-bottom-desc-title'>{product_name}</div>
          <div className='tutorialCardVertical-bottom-desc-title'>{product_description}</div>
        </div>
      </div>
      <div className='tutorialCardVertical-bottom-detail'>
        <div className='tutorialCardVertical-bottom-detail-level'>
          <div className='tutorialCardVertical-bottom-detail-level-unit'>CHF&nbsp;</div>
          <div className='tutorialCardVertical-bottom-detail-level-price'>100</div>
        </div>
        <div className='tutorialCardVertical-bottom-detail-rate'>
          <Rate disabled defaultValue={2} />
          <span>(174)</span>
        </div>
      </div>
      <ProductDetailModal isOpen={detailModelOpen} setIsOpen={closeModal} item={product} />
    </div>
  )
}
