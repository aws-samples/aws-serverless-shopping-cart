<template>
  <v-btn fixed right rounded small @click.stop="toggleDrawer" text icon x-large>
    <v-badge overlap color="accent" v-bind:class="{ 'animated-pulse': cartLoading > 0 }">
      <div slot="badge">{{cartSize}}</div>
      <v-icon color="black" x-large>mdi-cart</v-icon>
    </v-badge>
  </v-btn>
</template>

<script>
import { mapGetters, mapState } from "vuex";

export default {
  name: "cart-button",
  computed: {
    ...mapGetters(["cartSize"]),
    ...mapState(["cartLoading"])
  },
  data() {
    return {
      drawer: false
    };
  },
  methods: {
    toggleDrawer() {
      this.$emit("drawerChange");
    }
  }
};
</script>
<style scoped>
@-webkit-keyframes pulse {
  from {
    -webkit-transform: scale3d(1, 1, 1);
    transform: scale3d(1, 1, 1);
  }

  50% {
    -webkit-transform: scale3d(1.25, 1.25, 1.25);
    transform: scale3d(1.25, 1.25, 1.25);
  }

  to {
    -webkit-transform: scale3d(1, 1, 1);
    transform: scale3d(1, 1, 1);
  }
}

@keyframes pulse {
  from {
    -webkit-transform: scale3d(1, 1, 1);
    transform: scale3d(1, 1, 1);
  }

  50% {
    -webkit-transform: scale3d(1.25, 1.25, 1.25);
    transform: scale3d(1.25, 1.25, 1.25);
  }

  to {
    -webkit-transform: scale3d(1, 1, 1);
    transform: scale3d(1, 1, 1);
  }
}

.animated-pulse {
  animation: pulse 0.5s infinite;
}
</style>