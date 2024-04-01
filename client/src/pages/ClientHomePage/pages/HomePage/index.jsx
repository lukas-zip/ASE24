import './index.less'
import APPTHEME from '@/constants/COLORS/APPTHEME';
import SIZE from '@/constants/SIZE';
import { useSelector } from 'react-redux';
import CardVertical from '../../../../Components/Card/CardVertical';
import { Input } from 'antd';
import { EnvironmentFilled, EnvironmentOutlined, EnvironmentTwoTone } from '@ant-design/icons';
import COLORS from '../../../../constants/COLORS';
const { Search } = Input
export default function UserHomePage() {
    const THEME = APPTHEME["light"]
    const { user } = useSelector(state => state.user)
    const onSearch = async () => {

    }
    return (
        <div className={`productPage`} style={{}}>
            {/* <div className={"overflowAuto"} style={{ flex: 1, display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 20 }}> */}
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
            <div className='productPage-container'>
                <div className='productPage-container-box'>
                    <CardVertical />
                    <CardVertical />
                    <CardVertical />
                    <CardVertical />
                </div>
            </div>
            {/* </div> */}
        </div >
    )
}
