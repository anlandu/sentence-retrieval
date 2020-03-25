// App.vue

<template>
  <div class="container">
    <h1> Hello {{bundler}} </h1>
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
      bundler: "Information Retrieval"
    };
  }
});
</script>

<style lang="stylus" scoped>
.container
  color #e57200
</style>