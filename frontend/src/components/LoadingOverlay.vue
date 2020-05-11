<template>
  <v-layout row justify-center>
    <v-dialog v-model="loading" persistent fullscreen content-class="loading-dialog">
      <v-container fill-height justify="center" align="center" style="height: 300px;">
        <v-row justify="center" align="center">
          <v-progress-circular justify-center indeterminate :size="70" :width="7" color="accent"></v-progress-circular>
        </v-row>
        <v-row v-if="loadingText" justify="center" align="center">
          <h1 class="accent--text">{{loadingText}}</h1>
        </v-row>
      </v-container>
    </v-dialog>
  </v-layout>
</template>

<script>
import { mapState } from "vuex";

export default {
  name: "loading-overlay",
  data() {
    return {};
  },
  computed: {
    ...mapState(["loading", "loadingText"])
  }
};
</script>

<style>
.loading-dialog {
  background-color: #303030b2;
}
</style>