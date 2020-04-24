<template>
  <div class="editor">
    <ul v-if="recommendations">
      <li v-for="(sent, index) in recommendations" :key="index">
        <a href="#" @click.prevent="replaceSelectionWithRec(index)">
          <div v-html="sent"></div>
        </a>
      </li>
    </ul>
    <editor-menu-bubble
      :editor="editor"
      :keep-in-bounds="keepInBounds"
      v-slot="{ commands, isActive, menu }"
    >
      <div
        class="menububble"
        :class="{ 'is-active': menu.isActive }"
        :style="`left: ${menu.left}px; bottom: ${menu.bottom}px;`"
      >
        <button class="menububble__button" :class="{ 'is-active': true }" @click="fixText">
          <p>Fix this!</p>
        </button>
      </div>
    </editor-menu-bubble>
    <editor-content :editor="editor" />
  </div>
</template>

<script>
// Import the editor
import { Editor, EditorContent, EditorMenuBubble } from "tiptap";
import { Slice } from "prosemirror-model";
var apiURL = "recommendations";

export default {
  components: {
    EditorContent,
    EditorMenuBubble
  },
  data() {
    return {
      keepInBounds: true,
      editor: null,
      recommendations: []
    };
  },
  methods: {
    fixText() {
      const { state } = this.editor;
      const { selection } = state;
      const { from, to } = selection;
      const text = state.doc.textBetween(from, to, " ");
      alert('Try fix "' + text + '"');
      this.fetchData(text);
    },
    fetchData: function(queryText) {
      console.log("Quering", queryText);
      var xhr = new XMLHttpRequest();
      var self = this;
      var params = new FormData();
      params.append("query", queryText);
      xhr.open("POST", apiURL);
      xhr.onload = function() {
        self.recommendations = JSON.parse(xhr.responseText).recommendations;
        console.log(self.recommendations);
      };
      xhr.send(params);
    },
    replaceSelectionWithRec: function(index) {
      const { state } = this.editor;
      let transaction = state.tr.replaceSelection();
      var temp = document.createElement("div");
      temp.innerHTML = this.recommendations[index];
      transaction.insertText(temp.textContent);
      this.editor.view.dispatch(transaction);
      this.recommendations = [];
    }
  },
  mounted() {
    this.editor = new Editor({
      content: "<p>This is just a boring paragraph</p>"
    });
  },
  beforeDestroy() {
    this.editor.destroy();
  }
};
</script>

<style lang="stylus" scoped>
a:visited
  color unset

.editor
  position relative
  max-width 50rem
  margin 0 auto 5rem
  box-shadow 0 1px 3px 1px rgba(60, 60, 60, 0.13)

.menububble
  position absolute
  display -webkit-box
  display -ms-flexbox
  display flex
  z-index 20
  background white
  box-shadow 0 1px 3px 1px rgba(60, 60, 60, 0.13)
  border-radius 5px
  padding 0.3rem
  margin-bottom 0.5rem
  -webkit-transform translateX(-50%)
  transform translateX(-50%)
  visibility hidden
  opacity 0
  -webkit-transition opacity 0.2s, visibility 0.2s
  transition opacity 0.2s, visibility 0.2s

.menububble.is-active
  opacity 1
  visibility visible

.menububble__button
  display -webkit-inline-box
  display -ms-inline-flexbox
  display inline-flex
  background transparent
  border 0
  color #fff
  padding 0.2rem 0.5rem
  margin-right 0.2rem
  border-radius 3px
  cursor pointer

.menububble__button:last-child
  margin-right 0

.menububble__button:hover
  background-color hsla(0, 0%, 100%, 0.1)

.menububble__button.is-active
  background-color hsla(0, 0%, 100%, 0.2)

.menububble__form
  display -webkit-box
  display -ms-flexbox
  display flex
  -webkit-box-align center
  -ms-flex-align center
  align-items center

.menububble__input
  font inherit
  border none
  background transparent
  color #fff
</style>