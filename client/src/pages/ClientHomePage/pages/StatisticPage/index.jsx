import './index.less'
import APPTHEME from '@/constants/COLORS/APPTHEME';
import SIZE from '@/constants/SIZE';
import { useSelector } from 'react-redux';

export default function StatisticPage() {
    const THEME = APPTHEME["light"]
    const { user } = useSelector(state => state.user)
    return (
        <div className={`settingPage`} style={{ backgroundColor: THEME.contentColor }}>
            <div className={"overflowAuto"} style={{ flex: 1, display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 20 }}>

            </div>
        </div >
    )
}
