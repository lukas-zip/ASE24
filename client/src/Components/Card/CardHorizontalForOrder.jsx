import './CardHorizontal.less'
import { CalendarOutlined, ShoppingCartOutlined } from '@ant-design/icons'
import { useDispatch, } from 'react-redux'
import { useNavigate } from 'react-router-dom'
import { message } from 'antd'
export default function CardHorizontal({ img = "https://lh5.googleusercontent.com/p/AF1QipNK6p_2MugdId-dBh8mKuOQdnIm3iXmemRXWCbB=w540-h312-n-k-no" }) {
  const navigateTo = useNavigate()
  const dispatch = useDispatch()
  const handleAddOperation = async () => {
    const isTodayHasAlr = true
    if (isTodayHasAlr) {
      message.error("Error Happens")
    } else {

    }
  }
  return (
    <div
      onClick={() => {
        // navigateTo(`/specifictutorial/${_id}`)
      }}
      className={`TutorialCardHorizontal TutorialCardHorizontal-light`}>
      <div style={{ display: 'flex', alignItems: 'center' }}>
        <span style={{
          flexShrink: 0,
          flexBasis: 100,
          height: 100,
          width: 100,
          borderRadius: 10,
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          overflow: "hidden",
          marginRight: 10
        }}>
          <img style={{ maxHeight: '100%', width: 'auto', height: 'auto', objectFit: 'cover' }} src={img} />
        </span>
        <div style={{ display: 'flex', flexDirection: 'column', justifyContent: 'space-between' }}>
          <div className='TutorialCardHorizontal-desc-content'>Money</div>
          <div className='TutorialCardHorizontal-desc-title'>Name</div>
        </div>
      </div>
      <span
        className='TutorialCardHorizontal-extraBtn'
        onClick={(e) => {
          e.stopPropagation()
          handleAddOperation()
        }}
      >
        <ShoppingCartOutlined />
      </span>
    </div >
  )
}
