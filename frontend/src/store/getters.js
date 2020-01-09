import {
    Decimal
} from "decimal.js"


const cartSize = (state) => {
    return state.cart.reduce((total, cartProduct) => {
        return total + cartProduct.quantity
    }, 0)
}
const cartTotalAmount = (state) => {
    let val = state.cart.reduce((total, cartProduct) => {
        return new Decimal(total).plus(new Decimal(cartProduct.productDetail.price/100).times(cartProduct.quantity));
    }, 0);
    return new Decimal(val).toFixed(2)
}
const currentUser = (state) => {
    return state.user
}
const getCart = (state) => {
    return state.cart.filter((prod) => prod.quantity > 0)
}

export default {
    cartSize,
    cartTotalAmount,
    currentUser,
    getCart
}