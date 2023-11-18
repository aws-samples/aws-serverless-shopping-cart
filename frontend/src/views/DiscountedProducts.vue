<template>
    <v-container grid-list-md fluid class="mt-0" pt-0>
      <v-layout row wrap>
        <v-flex v-for="product in discountedProducts" :key="product.productId" xs12 lg4 sm6>
          <DiscountedProduct :discountedProduct="product" />
        </v-flex>
      </v-layout>
    </v-container>
</template>

<script>
export default {
  computed: {
    discountedProducts() {
      return this.$store.state.discountedProducts;
    }
  },
  created() {
    this.$store.dispatch("fetchDiscountedProducts");
  }
};
</script>
