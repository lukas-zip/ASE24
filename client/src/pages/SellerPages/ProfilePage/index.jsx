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
    const updateUser = {
        address: "update 18, Bern",
        description: "I´m selling update goods.",
        email: "update@example.com",
        phone: "324314332414",
        profile_picture: "NONE",
        shop_id: "2c1f74e3-33f0-47a2-97e5-ad4cc5953ed3",
        shop_name: "update Hydro",
        type: "Shop"
    }
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
