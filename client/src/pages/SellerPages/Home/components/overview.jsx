import MyCard from './myCard'
const orderSVG = <svg t="1712448958272" class="icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="4288" width="200" height="39px"><path d="M319.521032 96.421161 400.68129 96.421161C408.642065 44.428387 453.33471 4.492387 507.573677 4.492387 561.812645 4.492387 606.439226 44.428387 614.466065 96.421161L698.401032 96.421161 698.401032 228.252903 319.488 228.252903 319.488 96.421161 319.521032 96.421161ZM924.176516 890.252387C924.176516 957.968516 869.309935 1012.868129 801.626839 1012.868129L220.193032 1012.868129C152.443871 1012.868129 97.643355 957.968516 97.643355 890.252387L97.643355 221.580387C97.643355 153.89729 152.443871 99.03071 220.193032 99.03071L244.339613 99.03071 244.339613 309.512258 777.447226 309.512258 777.447226 99.03071 801.593806 99.03071C869.276903 99.03071 924.143484 153.89729 924.143484 221.580387L924.143484 890.252387 924.176516 890.252387Z" fill="#93a1e3" p-id="4289"></path></svg>
const productSVG = <svg t="1712449108776" class="icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="5518" width="200" height="39px"><path d="M960 303.68a32 32 0 0 0-2.24-10.88 9.6 9.6 0 0 0 0-2.56 11.52 11.52 0 0 0 0-2.88l-128-208A32 32 0 0 0 800 64H224a32 32 0 0 0-27.52 15.36L68.8 288a11.52 11.52 0 0 0 0 2.88v2.56a32 32 0 0 0-4.8 10.24V928a32 32 0 0 0 32 32h832a32 32 0 0 0 32-32V304zM240.64 128h544l87.68 144H152.96zM896 896H128V336h768z" p-id="5519" fill="#84bae1"></path><path d="M256 512h256v64H256zM256 672h384v64H256z" p-id="5520" fill="#84bae1"></path></svg>


export default function Overview({ products = [], orders = [] }) {
    return (
        <div className='content-mainbox-statistic-overview'>
            <div className='content-mainbox-statistic-overview-cards'>
                <MyCard key={1} SVG={productSVG} title={"Product"} value={products.length} />
                <MyCard key={2} navigation={"/shop/order"} SVG={orderSVG} title={"Order"} value={orders.length} />
            </div>
        </div>
    )
}
