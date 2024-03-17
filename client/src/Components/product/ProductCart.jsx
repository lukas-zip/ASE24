import React from "react"
import { useDispatch } from "react-redux"

export const ProductCart = ({ key, id, cover, name, price }) => {
  // const dispatch = useDispatch()
  // const addToCart = () => {
  //   dispatch(cartActions.addToCart({ id, name, price, cover }))
  // }
  return (
    <>
      <div className='box boxItems' id='product'>
        <div className='img'>
          <img src={cover} alt='cover' />
        </div>
        <div className='details'>
          <h3>${price}</h3>
          <p>{name}</p>
        </div>
        <div>
          +
        </div>
      </div>
    </>
  )
}
