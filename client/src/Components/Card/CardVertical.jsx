import './CardVertical.less'
import { CalendarFilled } from '@ant-design/icons'
import { useNavigate } from 'react-router-dom';
export default function CardVertical({ img = "https://i.ytimg.com/vi/YmFuedpSldA/oar2.jpg?sqp=-oaymwEdCJUDENAFSFWQAgHyq4qpAwwIARUAAIhCcAHAAQY=&rs=AOn4CLA1Raa3y-da_nvF7O2G_Zsbwqo38A" }) {
  const navigateTo = useNavigate()
  return (
    <div onClick={() => {
      // navigateTo(`/`)
    }} className={`tutorialCardVertical tutorialCardVertical-light`}>
      <div className='tutorialCardVertical-cover'>
        <img src={img} />
        <div className='tutorialCardVertical-cover-detail'>
          <div className='tutorialCardVertical-cover-detail-level'>level</div>
          <div className='tutorialCardVertical-cover-detail-duration'>duration</div>
        </div>
      </div>
      <div className='tutorialCardVertical-bottom'>
        <div className={`tutorialCardVertical-bottom-desc`}>
          <div className='tutorialCardVertical-bottom-desc-title'>NAME</div>
          <div className='tutorialCardVertical-bottom-desc-brief'>Brief</div>
        </div>
        <div className='TutorialCardHorizontal-bottom-extraBtn'>
          <CalendarFilled />
        </div>
      </div>
    </div >
  )
}
