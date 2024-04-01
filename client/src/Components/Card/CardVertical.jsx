import './CardVertical.less'
import { CalendarFilled, ShoppingCartOutlined, ShoppingTwoTone } from '@ant-design/icons'
import { useNavigate } from 'react-router-dom';
import SIZE from '../../constants/SIZE';
import COLORS from '../../constants/COLORS';
export default function CardVertical({ img = "https://i.ytimg.com/vi/YmFuedpSldA/oar2.jpg?sqp=-oaymwEdCJUDENAFSFWQAgHyq4qpAwwIARUAAIhCcAHAAQY=&rs=AOn4CLA1Raa3y-da_nvF7O2G_Zsbwqo38A" }) {
  const navigateTo = useNavigate()
  return (
    <div onClick={() => {
      // navigateTo(`/`)
    }} className={`tutorialCardVertical tutorialCardVertical-light`}>
      <div className='tutorialCardVertical-cover'>
        <img style={{ maxWidth: '100%', width: 'auto', height: 'auto', objectFit: 'cover' }} src={img} />
      </div>
      <div className='tutorialCardVertical-bottom'>
        <div className={`tutorialCardVertical-bottom-desc`}>
          <div className='tutorialCardVertical-bottom-desc-title'>NAME</div>
          <div className='tutorialCardVertical-bottom-desc-brief'>Brief</div>
        </div>
        <div className='TutorialCardVertical-bottom-extraBtn'>
          <ShoppingTwoTone twoToneColor="#3d3d3d" style={{ fontSize: SIZE.NormalTitle, color: COLORS.backgroundGray }} />
        </div>
      </div>
      <div className='tutorialCardVertical-bottom-detail'>
        <div className='tutorialCardVertical-bottom-detail-level'>CHF 100</div>
        <div className='tutorialCardVertical-bottom-detail-duration'>100+ bought</div>
      </div>
    </div >
  )
}
