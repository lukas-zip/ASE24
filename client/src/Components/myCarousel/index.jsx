import React, { useState } from 'react'
import './index.less'
import { LeftCircleOutlined, RightCircleOutlined } from '@ant-design/icons';
const MyCarousel = ({ imgArr }) => {
    const [seletedIndex, setSelectedIndex] = useState(0)
    const handleLeftSlideAction = () => setSelectedIndex((seletedIndex - 1 + imgArr.length) % imgArr.length)
    const handleRightSlideAction = () => setSelectedIndex((seletedIndex + 1) % imgArr.length)
    return (
        <div className="myCarouselContainer">
            {imgArr && <div className='myCarousel'>
                {/* 这是照片合集分页 */}
                <div
                    className='myCarouselSlider'
                    style={{ width: `${imgArr.length}00%`, transform: `translate(-${seletedIndex * (100 / imgArr.length)}%)` }}
                >
                    {imgArr.map((item, index) => (
                        <section key={index}>
                            <img src={item} />
                        </section>
                    ))}
                </div>
                {imgArr.length > 1 && <>
                    <div className="myCarouselSliderControls">
                        {/* 这是照片左右滑动按钮 */}
                        <div
                            className="myCarouselSliderControlsBlock left"
                            onClick={handleLeftSlideAction}
                        >
                            <LeftCircleOutlined className="myCarouselSliderControls-arrow left" />
                        </div>
                        <div
                            className="myCarouselSliderControlsBlock right"
                            onClick={handleRightSlideAction}
                        >
                            <RightCircleOutlined className="myCarouselSliderControls-arrow right" />
                        </div>
                        {/* 这是下面的点 */}
                        <ul>
                            {imgArr.map((item, index) => (
                                <li key={index} style={{ backgroundColor: seletedIndex === index ? "#747474" : "transparent" }}></li>
                            ))}
                        </ul>
                    </div>
                    <div className={`displayIndex`}>
                        {seletedIndex + 1} / {imgArr.length}
                    </div>
                </>}
            </div>}
        </div>
    )
}
export default MyCarousel
