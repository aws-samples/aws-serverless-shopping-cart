<template>
  <v-app>
    <v-app-bar elevate-on-scroll app class="primary">
      <v-toolbar-title>
        <router-link tag="div" to="/">
          <a class="accent--text header font-weight-black">
            DEMO
            <span class="font-weight-thin subheading secondary--text">Store</span>
          </a>
        </router-link>
      </v-toolbar-title>
      <v-toolbar-items>
        <v-btn to="/auth" v-if="!currentUser" text class="ml-2">Sign In</v-btn>
        <cart-button @drawerChange="toggleDrawer" />
        <div class="sign-out">
          <amplify-sign-out v-if="currentUser" class="Form--signout pl-2"></amplify-sign-out>
        </div>
      </v-toolbar-items>
    </v-app-bar>
    <v-content>
      <v-container fluid>
        <loading-overlay />
        <v-fade-transition mode="out-in">
          <router-view></router-view>
        </v-fade-transition>
      </v-container>
      <v-navigation-drawer
        style="position:fixed; overflow-y:scroll;"
        right
        v-model="drawer"
        temporary
        align-space-around
        column
        d-flex
      >
        <cart-drawer />
      </v-navigation-drawer>
    </v-content>
  </v-app>
</template>

<script>
import { mapGetters, mapState } from "vuex";

export default {
  name: "app",
  data() {
    return {
      drawer: null
    };
  },
  mounted() {
    this.$store.dispatch("fetchCart");
  },
  computed: {
    ...mapGetters(["cartSize", "currentUser"]),
    ...mapState(["cartLoading"])
  },
  methods: {
    logout() {
      this.$store.dispatch("logout");
    },
    toggleDrawer() {
      this.drawer = !this.drawer;
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

:root {
  /* Colors */
  --amazonOrange: #e88b01 !important;
}
</style>