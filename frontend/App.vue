// App.vue

<template>
  <div class="container">
    <h1> {{bundler}} </h1>
    <editor />
  </div>
</template>

<script lang="ts">
import Vue from "vue";
import Editor from "./Editor.vue";

export default Vue.extend({
  components: {
    'editor': Editor
  },
  data() {
    return {
      bundler: "Academic Style Corrector"
    };
  }
});
</script>

<style lang="stylus">
.container
  color #e57200
</style>