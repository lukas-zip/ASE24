import "./product.css"
import CardHorizontal from "../Card/CardHorizontalForOrder"
import CardVertical from "../Card/CardVertical"

export const Product = () => {
  return (
    <section className='product'>
      <div className='container grid3'>
        <CardHorizontal />
        <CardHorizontal />
        <CardHorizontal />
        <CardHorizontal />
      </div>
    </section>
  )
}
