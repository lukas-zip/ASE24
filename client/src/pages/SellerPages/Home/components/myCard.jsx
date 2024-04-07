import React from 'react'
import { useNavigate } from 'react-router-dom'

export default function MyCard({ SVG, title, value, prefix, suffix, navigation }) {
    const navigateTo = useNavigate()
    return (
        <div className='content-mainbox-statistic-overview-cards-card' onClick={() => navigation && navigateTo(navigation)}>
            <div className='content-mainbox-statistic-overview-cards-card-left'>
                <div className='card-svg'>
                    {SVG}
                </div>
            </div>
            <div className='content-mainbox-statistic-overview-cards-card-right'>
                <div className='card-right-title'>
                    {title}
                </div>
                <div className='card-right-value'>
                    {prefix && prefix}{value}{suffix && suffix}
                </div>
            </div>
        </div>
    )
}
