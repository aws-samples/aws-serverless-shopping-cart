<template>
  <div class="items">
    <v-list-item>
        <v-icon>mdi-cart</v-icon>
      <v-list-item-content>
        <v-list-item-title class="accent--text font-weight-bold">SHOPPING CART</v-list-item-title>
      </v-list-item-content>
    </v-list-item>

    <v-divider></v-divider>

    <v-list dense>
      <v-list-item v-for="item in getCart" :key="item.sk" link>
        <v-list-item-content>
          <v-list-item-content>
            <p>
              {{ item.productDetail.name }}
              <span class="font-weight-light">x {{item.quantity}}</span>
            </p>
            <span class="font-weight-light">${{getTotalPrice(item)}}</span>
          </v-list-item-content>
        </v-list-item-content>
      </v-list-item>
      <v-list-item-content>
        <v-list-item v-if="cartTotalAmount > 0">
          <v-btn to="/checkout" block color="accent">Checkout ${{cartTotalAmount}}</v-btn>
        </v-list-item>
        <v-list-item v-else>Cart Empty</v-list-item>
      </v-list-item-content>
    </v-list>
  </div>
</template>

<script>
import { mapGetters, mapState } from "vuex";
import { Decimal } from "decimal.js";

export default {
  name: "cart-drawer",
  data() {
    return {
      signedIn: false
    };
  },
  computed: {
    ...mapGetters(["cartTotalAmount", "getCart"]),
    ...mapState(["cart"])
  },
  methods: {
    getTotalPrice(item) {
      return new Decimal((item.productDetail.price/100) * item.quantity).toFixed(2);
    }
  }
};
</script>

<style>
.header {
  font-weight: bold !important;
  font-size: 30px !important;
  text-decoration: none;
}
</style>