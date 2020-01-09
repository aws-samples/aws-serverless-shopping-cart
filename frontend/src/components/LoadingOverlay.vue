<template>
    <v-layout row justify-center>
      <v-dialog v-model="loading" persistent fullscreen content-class="loading-dialog">
        <v-container fill-height>
          <v-layout row justify-center align-center>
            <v-progress-circular indeterminate :size="70" :width="7" color="accent"></v-progress-circular>
          </v-layout>
        </v-container>
      </v-dialog>
    </v-layout>
</template>

<script>
import { mapState } from "vuex";

export default {
  name: 'loading-overlay',
  data() {
    return {};
  },
  computed: {
    ...mapState(["loading"])
  }
};
</script>

<style>
.loading-dialog {
   background-color: #303030b2; 
}
</style>