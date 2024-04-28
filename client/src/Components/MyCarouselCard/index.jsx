import React, { useEffect, useState } from 'react'
import './index.less'
import LeftArrow from '@/assets/pic/leftArrow.png'

const MyCarouselDisplay = ({ pictures }) => {
    const [currentIndex, setCurrentIndex] = useState(0)
    const offsetStep = 200
    const scaleStep = 0.8
    const opacityStep = 0.9
    useEffect(() => {
        const timer = setInterval(() => {
            setCurrentIndex((prevIndex) => (prevIndex + 1) % pictures.length)
        }, [5000])
        return () => clearInterval(timer)
    }, [])
    useEffect(() => {
        layout()
    }, [currentIndex])
    const [styleArray, setStyleArray] = useState(pictures.map(item => ({})))
    const layout = () => {
        const updatedStyleArray = styleArray.map((_, index) => {
            // tansform
            // scale
            // opacity
            // zIndex
            // ratate
            const step = index - currentIndex
            const sign = Math.sign(step)
            const offset = step * offsetStep
            const scale = scaleStep ** Math.abs(currentIndex - index)
            const opacity = opacityStep ** Math.abs(currentIndex - index)
            const zIndex = 100 - Math.abs(currentIndex - index)
            const rotate = 45 * -sign
            return {
                transform: `translate(calc(-50% + ${currentIndex === index ? 0 : offset}px), 0) scale(${scale}) rotateY(${rotate}deg)`,
                zIndex,
                opacity
            }
        })
        setStyleArray(updatedStyleArray)
    }
    return <div className='MyCarousel' style={{ height: 400 }}>
        <div className='MyCarousel-prev' onClick={() => {
            console.log(((currentIndex - 1) > 0) ? (currentIndex - 1) : 0)
            setCurrentIndex(((currentIndex - 1) > 0) ? (currentIndex - 1) : 0)
        }}>
            <img src={LeftArrow} style={{ height: 50, width: 50 }} />
        </div>
        <div className='MyCarousel-next' onClick={() => setCurrentIndex(((currentIndex + 1) > (pictures.length - 1)) ? currentIndex : (currentIndex + 1))}>
            <img src={LeftArrow} style={{ height: 50, width: 50, transform: 'rotate(180deg)' }} />
        </div>
        <div className='MyCarousel-list' >
            {pictures.map((item, key) => (
                <div key={key} className='MyCarousel-list-item' style={{ height: 400, width: 500, backgroundImage: `url(${item})`, ...styleArray[key] }}
                    onClick={() => {
                        console.log("dianjie");
                        setCurrentIndex(key);
                    }}>
                    <img style={{ maxHeight: 400, width: '100%', height: "100%", objectFit: 'contain' }} src={item} alt="" />
                </div>
            ))}
        </div>
    </div >
}

export default MyCarouselDisplay