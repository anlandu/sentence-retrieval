<template>
  <div class="editor">
    <div class="textarea">
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
            <p style="margin:0">Fixit!</p>
          </button>
        </div>
      </editor-menu-bubble>
      <editor-content :editor="editor"></editor-content>
    </div>
    <div class="recommendation">
      <h2>Scoring Function</h2>
      <div v-for="func in avail_scoring_func" :key="func[0]">
        <input type="radio" :id="func[0]" :value="func[0]" v-model="score_func" />
        <label :for="func[0]">{{func[1]}}</label>
      </div>
      <br>
      <h2>Suggestions</h2>
      <ul v-if="recommendations && recommendations.length">
        <li v-for="(sent, index) in recommendations" :key="index">
          <a href="#" @click.prevent="replaceSelectionWithRec(index)">
            <div v-html="sent"></div>
          </a>
        </li>
      </ul>
      <p v-else>Select a sentence to rewrite!</p>
    </div>
  </div>
</template>

<script>
// Import the editor
import { Editor, EditorContent, EditorMenuBubble } from "tiptap";
import { Slice } from "prosemirror-model";
var apiURL = "recommendations";

const testParaphrase = `<p>Understanding the current research trends, problems, and their innovative solutions remains a bottleneck due to the ever-increasing volume of scientific articles. In this paper, we propose NLPExplorer, a completely automatic portal for indexing, searching, and visualizing Natural Language Processing (NLP) research volume. NLPExplorer presents interesting insights from papers, authors, venues, and topics. In contrast to previous topic modelling based approaches, we manually curate five course-grained non-exclusive topical categories namely Linguistic Target (Syntax, Discourse, etc.), Tasks (Tagging, Summarization, etc.), Approaches (unsupervised, supervised, etc.), Languages (English, Chinese,etc.) and Dataset types (news, clinical notes, etc.). Some of the novel features include a list of young popular authors, popular URLs, and datasets, a list of topically diverse papers and recent popular papers. Also, it provides temporal statistics such as yearwise popularity of topics, datasets, and seminal papers. To facilitate future research and system development, we make all the processed datasets accessible through API calls.</p>`;

export default {
  components: {
    EditorContent,
    EditorMenuBubble
  },
  data() {
    return {
      keepInBounds: true,
      editor: null,
      recommendations: [],
      transaction: null,
      score_func: "ok"
    };
  },
  methods: {
    fixText() {
      const { state } = this.editor;
      const { selection } = state;
      const { from, to } = selection;
      const text = state.doc.textBetween(from, to, " ");
      self.transaction = state.tr;
      this.fetchData(text);
    },
    fetchData: function(queryText) {
      console.log("Quering", queryText);
      var xhr = new XMLHttpRequest();
      var self = this;
      var params = new FormData();
      params.append("query", queryText);
      params.append("score_func", this.score_func);
      xhr.open("POST", apiURL);
      xhr.onload = function() {
        self.recommendations = JSON.parse(xhr.responseText).recommendations;
      };
      xhr.send(params);
    },
    replaceSelectionWithRec: function(index) {
      const { state } = this.editor;
      transaction = self.transaction;
      var temp = document.createElement("div");
      temp.innerHTML = this.recommendations[index];
      transaction.insertText(temp.textContent);
      try {
        this.editor.view.dispatch(transaction);
      } catch (RangeError) {
        alert(
          "Your selection has changed because of editing, please search again!"
        );
      }
      this.recommendations = [];
      self.transaction = null;
    }
  },
  created() {
    this.avail_scoring_func = [
      ["ok", "Okapi BM25"],
      ["bm25f", "BM25F"],
      ["pln", "Pivoted Length Normalization"],
      ["tfidf", "TF-IDF"],
      ["freq", "Frequency"]
    ];
  },
  mounted() {
    this.editor = new Editor({
      content: testParaphrase
    });
  },
  beforeDestroy() {
    this.editor.destroy();
  }
};
</script>

<style lang="stylus">
a:visited
  color unset

a
  color #232d4b

.editor
  position relative
  max-width 90%
  margin 0 auto 5rem

.textarea
  width 50%
  height 700px
  box-shadow 0 1px 3px 1px rgba(60, 60, 60, 0.13)
  float left

div:focus, p:focus
  outline-style none

.recommendation
  margin-left 52%
  width 50%

.menububble
  position absolute
  display -webkit-box
  display -ms-flexbox
  display flex
  z-index 20
  background #e57200
  box-shadow 0 1px 3px 1px rgba(60, 60, 60, 0.13)
  border-radius 5px
  margin-bottom 0.5rem
  -webkit-transform translateX(-50%)
  transform translateX(-50%)
  visibility hidden
  opacity 0
  -webkit-transition opacity 0.2s, visibility 0.2s
  transition opacity 0.2s, visibility 0.2s

.menububble p
  font-family 'bodoni-urw', georgia, serif
  font-size 18px
  font-weight 600
  color white

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