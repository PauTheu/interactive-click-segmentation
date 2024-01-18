<template>
  <div class="root flex flex-row">
    <!-- Next button -->
    <b-icon
      id="previousB"
      icon="arrow-left-square"
      font-scale="2.5"
      style="color: black"
      @click.stop="
        checkBoxes('previous');
        getObjects();
        resetButtonAll(false);
        activeOb();
      "
    />

    <b-progress id="progressBar" :max="IDs" height="2rem" class="flex-spacer">
      <b-progress-bar :value="i" variant="success">
        <span
          ><strong>{{ i }} / {{ IDs }}</strong></span
        >
      </b-progress-bar>
    </b-progress>

    <b-icon
      id="nextB"
      icon="arrow-right-square"
      font-scale="2.5"
      style="color: black"
      @click.stop="
        checkBoxes('next');
        getObjects();
        resetButtonAll(false);
        activeOb();
      "
    />
    <!-- Alert for non-labeled Bounding Box  -->
    <AlertBoundingBox ref="alert" />
  </div>
</template>

<script>
import { defineComponent } from '@vue/composition-api';
import { storeToRefs } from 'pinia';
import useEditorStore from '../state/editor';

export default defineComponent({
  setup() {
    const store = useEditorStore();
    const {
      objects, i, IDs, assistiveObjects, oneshotObjects, editor, appliedLabel,
    } = storeToRefs(store);
    const {
      resetButtonAll,
      activeOb,
      getObjects,
      uploadBoxes,
      uploadImg,
      setImage,
      getBoxes,
      getAssistiveBoxes,
      getOneshotBoxes,
      getID,
      loadImgLabels,
    } = store;

    return {
      objects,
      assistiveObjects,
      oneshotObjects,
      i,
      IDs,
      editor,
      appliedLabel,
      resetButtonAll,
      activeOb,
      uploadBoxes,
      uploadImg,
      setImage,
      getObjects,
      getBoxes,
      getAssistiveBoxes,
      getOneshotBoxes,
      getID,
      loadImgLabels,
    };
  },
  created() {
    this.getID();
    localStorage.i = 1;
  },
  methods: {
    // Checks preformed before previous and next buttons clicked
    // Checks preformed before previous and next buttons clicked
    async checkBoxes(prevNext) {
      if (prevNext === 'next') {
        if (this.i === this.IDs) {
          // eslint-disable-next-line
          this.i = 1;
        } else {
          // eslint-disable-next-line
          this.i++;
        }
      }
      if (prevNext === 'previous') {
        if (this.i === 1) {
          // eslint-disable-next-line
          this.i = this.IDs;
        } else {
          // eslint-disable-next-line
          this.i--;
        }
      }
      this.appliedLabel = [];
      this.uploadImg();
      this.setImage();
      this.loadImgLabels();
      this.editor.clear();
    },
    handleKeydown(e) {
      if (e.keyCode === 37) {
        this.resetButtonAll(false);
        this.checkBoxes('previous');
        this.activeOb();
      }
      if (e.keyCode === 39) {
        this.resetButtonAll(false);
        this.checkBoxes('next');
        this.activeOb();
      }
    },
  },
  beforeMount() {
    window.addEventListener('keydown', this.handleKeydown, null);
  },
  beforeDestroy() {
    window.removeEventListener('keydown', this.handleKeydown);
  },
});
</script>

<style scoped>
.root {
  margin-top: 16px;
  width: 640px;
}

#previousB {
  cursor: pointer;
}

#nextB {
  cursor: pointer;
}

#progressBar {
  margin: 0 16px;
  height: 40px;
  white-space: nowrap;
  text-align: center;
  font-family: Helvetica Neue;
  font-style: normal;
  font-size: 18px;
  color: rgba(0, 0, 0, 1);
}
</style>
