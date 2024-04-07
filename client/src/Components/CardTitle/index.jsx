import './index.less'
export default function CardTitle({ title, extra }) {
    return (
        <div className='CardTitle'>
            <div className='CardTitle-title'>
                <div className='CardTitle-title-Vline'></div>
                <div className='CardTitle-title-value'>{title}</div>
                {extra && <div className='CardTitle-title-extra'>{extra}</div>}
            </div>
        </div>
    )
}
