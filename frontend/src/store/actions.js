import {
    postCart,
    getCart,
    getProducts,
    cartMigrate,
    putCart,
    cartCheckout
} from "@/backend/api.js"

import router from '@/router'

const setLoading = ({
    commit
}, payload) => {
    commit("setLoading", {value: payload.value,
    message: payload.message})
}

const fetchProducts = ({
    commit
}) => {
    getProducts().then((response) => {
        commit("setUpProducts", response.products);
    });
}
const fetchCart = ({
    commit
}) => {
    commit("setLoading", {value: true})
    getCart()
        .then((response) => {
            commit("setUpCart", response.products)
            commit("setLoading", {value: false})
        })
}
const addToCart = ({
    commit
}, obj) => {
    commit("setProductLoading", {
        "product": obj,
        "value": true,
        "btn": "add"
    })
    postCart(obj)
        .then((response) => {
            commit("setCartLoading", 1)
            commit("addToCart", response.productId);
            commit("setProductLoading", {
                "product": obj,
                "value": false,
                "btn": "add"
            })
            setTimeout(() => {
                commit("setCartLoading", -1)
            }, 500)
        }).catch(() => {
            commit("setProductLoading", {
                "product": obj,
                "value": false,
                "btn": "add"
            })
        });
}
const removeFromCart = ({
    commit
}, obj) => {
    commit("setProductLoading", {
        "product": obj,
        "value": true,
        "btn": "remove"
    })
    postCart(obj, -1)
        .then((response) => {
            commit("setCartLoading", 1)
            commit("removeFromCart", response.productId)
            commit("setProductLoading", {
                "product": obj,
                "value": false,
                "btn": "remove"
            })
            setTimeout(() => {
                commit("setCartLoading", -1)
            }, 500)
        }).catch(() => {
            commit("setProductLoading", {
                "product": obj,
                "value": false,
                "btn": "remove"
            })
        })
}
const updateCart = ({
    commit
}, obj) => {
    putCart(obj.product, obj.quantity)
        .then((response) => {
            commit("setCartLoading", 1)
            commit("updateCart", response)
            setTimeout(() => {
                commit("setCartLoading", -1)
            }, 500)
        })
}
const migrateCart = ({
    commit
}) => {
    commit("setLoading", {value: true})
    cartMigrate()
        .then((response) => {
            commit("setUpCart", response.products)
            commit("setLoading", {value: false})
        })
}

const checkoutCart = ({
    commit
}) => {
    commit("setLoading", {value: true, message: "This is where we'd handle payment before clearing the cart..."})
    cartCheckout()
        .then(() => {
            commit("setUpCart", [])
            setTimeout(function() {commit("setLoading", {value: false})}, 3000)
            setTimeout(function() {router.push("/")}, 3200)
        })
}

export default {
    setLoading,
    fetchCart,
    fetchProducts,
    migrateCart,
    updateCart,
    removeFromCart,
    addToCart,
    checkoutCart
}