<template>
  <v-card outlined class="flexcard" height="100%">
    <v-row class="pb-0" dense>
      <v-col :cols="8" class="mb-5">
        <v-card-title primary-title class="pb-0 pt-2">
          <p class="subtitle-2">{{product.name}}</p>
        </v-card-title>
      </v-col>
      <v-col>
        <p class="text-truncate body-2 pt-2 pb-0 pr-2 grow text-right mb-1">{{product.category}}</p>
      </v-col>
    </v-row>
    <v-card-text class="pt-0 pl-4 pb-0">
      <p class="pt-0 pb-0 mb-0 body-2">"{{product.description}}"</p>
      <p class="price pt-0 pb-0 grow accent--text mb-1">${{getPrice(product)}}</p>
    </v-card-text>
    <v-card-actions class="card-actions pa-0 ml-3 mb-2 mt-2 justify-center">
      <v-btn
        icon
        small
        :disabled="cartItemCount(product.productId) < 1"
        @click="removeProductFromCart(product)"
        :loading="product.removeLoading"
      >
        <v-icon>mdi-minus</v-icon>
      </v-btn>
      <cart-quantity-editor @input="updateCart" :product="product" :value="cartItemCount(product.productId)"></cart-quantity-editor>
      <v-btn icon small depressed @click="addProductToCart(product)" :loading="product.addLoading">
        <v-icon>mdi-plus</v-icon>
      </v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>
import { Decimal } from "decimal.js";

export default {
  props: ["product"],
  name: "product",
  methods: {
    cartItemCount(id) {
      let item = this.$store.state.cart.find(obj => obj.sk === id);
      if (item) {
        return item.quantity;
      } else {
        return 0;
      }
    },
    addProductToCart(product) {
      this.$store.dispatch("addToCart", product);
    },
    removeProductFromCart(product) {
      this.$store.dispatch("removeFromCart", product);
    },
    getPrice(product) {
      return new Decimal(product.price/100).toFixed(2);
    },
    updateCart(event) {
      this.$store.dispatch("updateCart", event)
    }
  }
};
</script>

<style scoped>
.flexcard {
  position: relative;
  padding-bottom: 50px;
}
.card-actions {
  position: absolute;
  bottom: 0;
  border: 1px solid;
  border-radius: 15px !important;
  border-color: #dce1e9;
}
</style>