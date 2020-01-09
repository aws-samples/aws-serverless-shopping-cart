<template>
  <div>
    <input
      type="text"
      v-if="edit"
      class="cart-quantity-input text-center"
      :class="{ 'input-error': $v.quantity.$error }"
      v-model.trim="$v.quantity.$model"
      @focus="oldquantity=$event.target.value, $event.target.select()"
      @blur="submit($event, product)"
      @keyup.enter="$event.target.blur()"
      v-focus
    />
    <div
      @click="edit = true;"
      v-else
      v-bind:class="{ 'font-weight-light': quantity < 1 }"
      class="pl-2 pr-2 noselect"
    >{{quantity}}</div>
  </div>
</template>

<script>
import { validationMixin } from "vuelidate";
import { required, between, integer } from "vuelidate/lib/validators";

export default {
  props: ["value", "product"],

  data() {
    return {
      edit: false,
      quantity: this.value,
      oldquantity: null
    };
  },
  methods: {
    submit(event, product) {
      this.quantity = event.target.value;
      this.$v.quantity.$touch();
      if (this.$v.$invalid) {
        this.quantity = this.oldquantity
        this.edit = false;
      } else {
        this.edit = false;
        this.$emit("input", { quantity: this.quantity, product });
      }
    }
  },
  validations: {
    quantity: {
      required,
      between: between(0, 500),
      integer
    }
  },
  mixins: [validationMixin],
  watch: {
    value: function() {
      this.quantity = this.value;
    }
  },
  directives: {
    focus: {
      inserted(el) {
        el.focus();
      }
    }
  }
};
</script>

<style scoped>
.cart-quantity-input {
  width: 25px;
}
.noselect {
  -webkit-touch-callout: none; /* iOS Safari */
  -webkit-user-select: none; /* Safari */
  -khtml-user-select: none; /* Konqueror HTML */
  -moz-user-select: none; /* Old versions of Firefox */
  -ms-user-select: none; /* Internet Explorer/Edge */
  user-select: none; /* Non-prefixed version, currently
                                  supported by Chrome, Opera and Firefox */
}
.input-error {
  color: red;
}
</style>