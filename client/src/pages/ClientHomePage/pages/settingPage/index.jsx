import './index.less'
import ProfileCard from './components/profileCard'
import APPTHEME from '@/constants/COLORS/APPTHEME';
import SIZE from '@/constants/SIZE';
import { useSelector } from 'react-redux';
export const cardType = {
    exercise: 'exercise',
    blog: 'blog',
}
export default function SettingPage() {
    const THEME = APPTHEME["light"]
    const { user } = useSelector(state => state.user)
    return (
        <div className={`settingPage`} style={{ backgroundColor: THEME.contentColor }}>
            <div className={"overflowAuto"} style={{ flex: 1, display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 20 }}>
                <div style={{ flex: 1, width: "80%", padding: '0 20px', marginBottom: SIZE.NormalMargin }}>
                    <ProfileCard />
                </div>
            </div>
        </div >
    )
}
