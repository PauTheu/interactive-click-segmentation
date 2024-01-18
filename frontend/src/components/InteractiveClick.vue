<template>
<div class="flex flex-col align-center justify-center full-height">
    <!-- Canvas with imagebackground -->
        <div class="flex flex-col align-center justify-center full-height">
          <b-card class="text-center"
          title="Guide">
  <b-card-body>
    <p class="card-text">"Left-click" for positive click</p>
    <p class="card-text">"ALT" + "Left-click" for negative click</p>
    <p class="card-text">Blue area represents lower confidence regions</p>
    <p class="card-text">Apply either suggested or custom label</p>
  </b-card-body>
</b-card>
    <div class="mt-4">
      <b-row class="mb-3 text-left">
    <b-col><h5>Applied Label:</h5></b-col>
  </b-row>
        <b-row v-for="(label, index) in appliedLabel" :key="label">
          <b-button disabled class="m-2">{{ label }}</b-button>
          <b-button variant="danger" class="m-2" @click="removeLabel(index)">
            <i class="bi bi-trash"></i>
          </b-button>
        </b-row>
    </div>
    </div>
    <b-row class="mb-3 text-center">
  <b-col>
    <h5>Suggested or Custom Label:</h5>
  </b-col>
</b-row>
    <b-row>
      <b-col v-for="item in imgLabels" :key="item">
        <b-button class="mb-3 button-style" @click="userInput = item">{{ item }}</b-button>
      </b-col>
    </b-row>
    <b-form-group class="text-left">
    <b-row>
        <b-col xs="9">
          <b-form-input class="mb-3" type="text" v-model="userInput" placeholder="Custom Label"
          :style="{ width: '150px' }"></b-form-input>
        </b-col>
        <b-col xs="3">
          <b-button variant="success" @click="addLabel">Apply Label</b-button>
        </b-col>
      </b-row>
    </b-form-group>
      <Editor
      v-bind:class="{ 'magic-wand': isActiveWand }"
      :canvasWidth="640"
      :canvasHeight="480"
      ref="editor"
      editorId="canvas1"
      style="margin: 0 auto"
    />
    <ProgressBar />
    <div class="flex flex-col align-center justify-center full-height">
    <ToolsSelection />
  </div>
  </div>
</template>
<script>

import { defineComponent } from '@vue/composition-api';
import { storeToRefs } from 'pinia';
import useEditorStore from '../state/editor';
import Editor from './vue-image-markup/src/Editor.vue';
import ToolsSelection from './ToolSelection.vue';
import ProgressBar from './ProgressBar.vue';

export default defineComponent({
  name: 'ImageEditor',
  components: {
    Editor,
    ToolsSelection,
    ProgressBar,
  },
  setup() {
    const store = useEditorStore();
    const {
      isActiveWand,
      isActiveRec,
      editor,
      i,
      clickRadius,
      imgLabels,
      appliedLabel,
    } = storeToRefs(store);
    const {
      setEditor,
      activeOb,
      uploadImg,
      clickImg,
      uploadImgWithMask,
      setImage,
      loadImgLabels,
    } = store;

    return {
      isActiveWand,
      isActiveRec,
      editor,
      i,
      clickRadius,
      imgLabels,
      appliedLabel,
      setEditor,
      activeOb,
      uploadImg,
      clickImg,
      uploadImgWithMask,
      setImage,
      loadImgLabels,
    };
  },
  data() {
    return {
      userInput: '',
    };
  },
  methods: {
    // Sets Canvas (Editor) into select Mode
    selectMode() {
      this.$refs.editor.set('selectMode');
    },
    addLabel() {
      if (this.appliedLabel.length === 0) {
        this.appliedLabel.push(this.userInput);
        console.log(this.appliedLabel);
      }
    },
    removeLabel(index) {
      this.appliedLabel.splice(index, 1);
    },
  },
  async mounted() {
    this.setEditor(this.$refs.editor);
    if (localStorage.i) this.i = localStorage.i;
    // upload image set in db
    this.uploadImg();
    // set image to controller
    this.setImage();
    this.loadImgLabels();
    console.log(this.imgLabels);
    // Implement drawing rect for pointer
    const onCanvasClick = (e) => {
      // eslint-disable-next-line
      const pointer = this.$refs.editor.canvas.getPointer(e);
      console.log(e);
      // eslint-disable-next-line
      const click = {
        x: pointer.x,
        y: pointer.y,
        positive: Boolean(!e.altKey),
        clickRadius: this.clickRadius,
      };
      const ClickColor = click.positive ? 'green' : 'red';
      const paramsCircle = {
        left: pointer.x - this.clickRadius - 0.3,
        top: pointer.y - this.clickRadius - 0.3,
        radius: this.clickRadius,
        strokeWidth: 1,
        stroke: ClickColor,
        fill: ClickColor,
        borderColor: ClickColor,
        noScaleCache: false,
      };
      this.clickImg(click);
      this.editor.drawCircle(paramsCircle);
    };
    document.querySelector('.upper-canvas').addEventListener('click', onCanvasClick);
  },
  beforeDestroy() {
    // window.localStorage.clear();
    document
      .querySelector('.upper-canvas')
      .removeEventListener('mousemove', this.onMouseCanvasMove);
    document.querySelector('.upper-canvas').removeEventListener('click', this.onCanvasClick);
  },
  // retrieving current id incase of sudden load
  watch: {
    i(newI) {
      localStorage.i = newI;
    },
  },
});
</script>
<style scoped>
.button-style {
  background-color: #1f1f1f;
  color: white;
}
.lable-pad {
  padding-bottom: 10px;
}
</style>
