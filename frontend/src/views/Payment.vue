<template>
  <v-container grid-list-md fluid class="mt-0" pt-0>
    <h1>Example payment form</h1>
    <v-layout row wrap>
      <v-flex xs12 lg4 sm6>
        <v-card>
          <v-container>
            <v-form pa-2 ma-2>
              <v-text-field
                color="secondary"
                outlined
                required
                @input="$v.cardNumber.$touch()"
                @blur="$v.cardNumber.$touch()"
                v-model="cardNumber"
                label="Card Number"
                v-mask="'#### #### #### ####'"
                :error-messages="cardNumberErrors"
              ></v-text-field>
              <v-text-field
                color="secondary"
                outlined
                required
                @input="$v.cardName.$touch()"
                @blur="$v.cardName.$touch()"
                label="Cardholder Name"
                v-model="cardName"
                :error-messages="cardNameErrors"
              ></v-text-field>
              <v-text-field
                color="secondary"
                outlined
                required
                @input="$v.cardExpiry.$touch()"
                @blur="$v.cardExpiry.$touch()"
                label="Card Expiry"
                v-model="cardExpiry"
                :error-messages="cardExpiryErrors"
              ></v-text-field>
              <v-text-field
                color="secondary"
                outlined
                required
                @input="$v.cardCVC.$touch()"
                @blur="$v.cardCVC.$touch()"
                label="Card CVC"
                v-model="cardCVC"
                :error-messages="cardCVCErrors"
              ></v-text-field>
              <v-btn block color="accent" @click="submit">Submit</v-btn>
            </v-form>
          </v-container>
        </v-card>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
import { mapState, mapGetters } from "vuex";
import { validationMixin } from "vuelidate";
import { required, helpers } from "vuelidate/lib/validators";

const ccvalidate = helpers.regex(
  "alpha",
  /(\d{4} *\d{4} *\d{4} *\d{4})/
); /* I know, I know... */

export default {
  data() {
    return {
      cardNumber: null,
      cardExpiry: null,
      cardName: null,
      cardCVC: null
    };
  },
  mixins: [validationMixin],
  validations: {
    cardNumber: {
      required,
      ccvalidate: ccvalidate
    },
    cardExpiry: {
      required
    },
    cardCVC: {
      required
    },
    cardName: {
      required
    }
  },
  methods: {
    submit() {
      this.$v.$touch();
      if (this.$v.$invalid) {
        console.log("invalid form"); // eslint-disable-line no-console
      } else {
        this.$store.dispatch("checkoutCart")
        // TODO: redirect to confirmation
      }
    }
  },
  computed: {
    ...mapGetters(["cartTotalAmount", "getCart"]),
    ...mapState(["cart"]),
    cardNumberErrors() {
      const errors = [];
      if (!this.$v.cardNumber.$dirty) return errors;
      !this.$v.cardNumber.ccvalidate &&
        errors.push("Valid card number is required.");
      !this.$v.cardNumber.required && errors.push("Card number is required.");
      return errors;
    },
    cardNameErrors() {
      const errors = [];
      if (!this.$v.cardName.$dirty) return errors;
      !this.$v.cardName.required && errors.push("Cardholder name is required.");
      return errors;
    },
    cardExpiryErrors() {
      const errors = [];
      if (!this.$v.cardExpiry.$dirty) return errors;
      !this.$v.cardExpiry.required && errors.push("Cart expiry is required.");
      return errors;
    },
    cardCVCErrors() {
      const errors = [];
      if (!this.$v.cardCVC.$dirty) return errors;
      !this.$v.cardCVC.required && errors.push("Card CVC is required.");
      return errors;
    }
  }
};
</script>

