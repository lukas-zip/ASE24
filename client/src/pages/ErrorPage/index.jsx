import { useNavigate, useRouteError } from 'react-router-dom'
import { CaretRightOutlined } from '@ant-design/icons';
import './index.less'
import { Button, Result } from 'antd';

export default function ErrorPage() {
    const error = useRouteError()
    const navigateTo = useNavigate()
    return (
        <Result
            status={`${error.status}`}
            title={`${error.status}: ${error.statusText}`}
            subTitle={error.data}
            extra={<Button type='primary' onClick={() => navigateTo('/')}>Back home <CaretRightOutlined /></Button>}
        />
    )
}
