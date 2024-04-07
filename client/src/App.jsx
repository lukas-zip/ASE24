import useUserTheme from './hooks/useUserTheme';
import './index.less'
import MyRouter from './router/routers.jsx'
import { ConfigProvider, theme } from 'antd';
import enUS from 'antd/locale/en_US';

const App = () => {
    const userTheme = useUserTheme()
    return (
        <ConfigProvider locale={enUS} theme={{ algorithm: userTheme === "dark" ? theme.darkAlgorithm : theme.defaultAlgorithm }}>
            <MyRouter />
        </ConfigProvider>
    )
}
export default App
