import COLORS from '@/constants/COLORS';
import './index.less'
import CardVertical from '@/Components/Card/CardVertical';
import { LeftOutlined } from '@ant-design/icons';
import { Empty, } from 'antd';
import { useLocation, useNavigate, useParams } from 'react-router-dom';
export default function SpecificCategoryProducts() {
    const Location = useLocation()
    const navigateTo = useNavigate()
    const { category } = useParams()
    const { allProducts = [] } = Location.state
    return (
        <div className={`SpecificCategoryProducts`} style={{}}>
            <div className='SpecificCategoryProducts-header' style={{}}>
                <div onClick={() => navigateTo(-1)} style={{ fontSize: 20, display: 'flex', userSelect: 'none', cursor: 'pointer', alignItems: 'center', color: COLORS.commentText, fontWeight: 500, justifyContent: 'center', backgroundColor: "#fff", padding: "0 16px", height: 50, borderRadius: 18, marginRight: 10 }}>
                    <LeftOutlined /> Back
                </div>
            </div>
            <div className='SpecificCategoryProducts-mainContent'>
                <div className='SpecificCategoryProducts-categories'>
                    <div className='SpecificCategoryProducts-categories-title'>
                        <div>{category.toUpperCase()}</div>
                    </div>
                    <div className='SpecificCategoryProducts-allCategoriesProducts'>
                        {Object.keys(allProducts).map((item, key) => <div className={`SpecificCategoryProducts-allCategoriesProducts-item`} key={key}>
                            {allProducts !== 0 && <div className='SpecificCategoryProducts-allCategoriesProducts-item-content' >
                                {allProducts.map((item, key) => <CardVertical product={item} key={key} />)}
                                {allProducts.map((item, key) => <CardVertical product={item} key={key} />)}
                                {allProducts.map((item, key) => <CardVertical product={item} key={key} />)}
                                {allProducts.map((item, key) => <CardVertical product={item} key={key} />)}
                                {allProducts.map((item, key) => <CardVertical product={item} key={key} />)}
                                {allProducts.map((item, key) => <CardVertical product={item} key={key} />)}
                                {allProducts.map((item, key) => <CardVertical product={item} key={key} />)}
                                {allProducts.map((item, key) => <CardVertical product={item} key={key} />)}
                                {allProducts.map((item, key) => <CardVertical product={item} key={key} />)}
                                {allProducts.map((item, key) => <CardVertical product={item} key={key} />)}
                                {allProducts.map((item, key) => <CardVertical product={item} key={key} />)}
                                {allProducts.map((item, key) => <CardVertical product={item} key={key} />)}
                                {allProducts.map((item, key) => <CardVertical product={item} key={key} />)}
                                {allProducts.map((item, key) => <CardVertical product={item} key={key} />)}
                                {allProducts.map((item, key) => <CardVertical product={item} key={key} />)}
                                {allProducts.map((item, key) => <CardVertical product={item} key={key} />)}
                                {allProducts.map((item, key) => <CardVertical product={item} key={key} />)}
                                {allProducts.map((item, key) => <CardVertical product={item} key={key} />)}
                                {allProducts.map((item, key) => <CardVertical product={item} key={key} />)}
                                {allProducts.map((item, key) => <CardVertical product={item} key={key} />)}
                                {allProducts.map((item, key) => <CardVertical product={item} key={key} />)}
                                {allProducts.map((item, key) => <CardVertical product={item} key={key} />)}
                                {allProducts.map((item, key) => <CardVertical product={item} key={key} />)}
                                {allProducts.map((item, key) => <CardVertical product={item} key={key} />)}
                                {allProducts.map((item, key) => <CardVertical product={item} key={key} />)}
                                {allProducts.map((item, key) => <CardVertical product={item} key={key} />)}
                                {allProducts.map((item, key) => <CardVertical product={item} key={key} />)}
                                {allProducts.map((item, key) => <CardVertical product={item} key={key} />)}
                                {allProducts.map((item, key) => <CardVertical product={item} key={key} />)}
                                {allProducts.map((item, key) => <CardVertical product={item} key={key} />)}
                                {allProducts.map((item, key) => <CardVertical product={item} key={key} />)}
                                {allProducts.map((item, key) => <CardVertical product={item} key={key} />)}
                                {allProducts.map((item, key) => <CardVertical product={item} key={key} />)}
                                {allProducts.map((item, key) => <CardVertical product={item} key={key} />)}
                                {allProducts.map((item, key) => <CardVertical product={item} key={key} />)}
                                {allProducts.map((item, key) => <CardVertical product={item} key={key} />)}
                                {allProducts.map((item, key) => <CardVertical product={item} key={key} />)}
                                {allProducts.map((item, key) => <CardVertical product={item} key={key} />)}
                                {allProducts.map((item, key) => <CardVertical product={item} key={key} />)}
                                {allProducts.map((item, key) => <CardVertical product={item} key={key} />)}
                            </div>}
                            {allProducts.length !== 0 && <div style={{ color: COLORS.commentText, marginTop: 20, display: 'flex', alignItems: 'center', justifyContent: 'center', }}>
                                --No more products--
                            </div>}

                        </div>)}
                        {allProducts.length === 0 && <div className='SpecificCategoryProducts-allCategoriesProducts-item-content-empty' >
                            <Empty description={"No related products"} />
                        </div>}
                    </div>
                </div>
            </div>
        </div >
    )
}
