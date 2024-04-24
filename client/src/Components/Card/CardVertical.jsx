import './CardVertical.less'
import { Rate } from 'antd';
import { useEffect, useState } from 'react';
import ProductDetailModal from '../../pages/ClientHomePage/components/ProductDetailModal';
import { formatNumber } from '@/utils/FormatNumber';
export default function CardVertical({ product, pic = "https://i.ytimg.com/vi/YmFuedpSldA/oar2.jpg?sqp=-oaymwEdCJUDENAFSFWQAgHyq4qpAwwIARUAAIhCcAHAAQY=&rs=AOn4CLA1Raa3y-da_nvF7O2G_Zsbwqo38A" }) {
  const { product_name, product_description, product_picture, product_price, product_price_reduction } = product
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
          <div className='tutorialCardVertical-cover-detail-level'>-{product_price_reduction}%</div>
          {/* <div className='tutorialCardVertical-cover-detail-duration'>100+ bought</div> */}
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
          <div style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
            <div style={{ display: 'flex', alignItems: 'baseline', fontSize: 16, gap: 2, fontWeight: 'bold', color: '#4790ff' }}>
              <div>CHF</div>
              <div style={{ fontSize: 26 }}>{formatNumber(product_price * (100 - product_price_reduction) / 100)}</div>
            </div>
            {(100 - product_price_reduction) != 0 && <>
              <div style={{ color: 'rgb(170, 170, 170)', fontSize: 14, textDecoration: 'line-through' }}>{product_price}</div>
            </>}
          </div>
        </div>
      </div>
      <ProductDetailModal isOpen={detailModelOpen} setIsOpen={closeModal} item={product} />
    </div>
  )
}
