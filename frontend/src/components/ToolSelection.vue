<template>
  <div class="Tools tools-box">
    <!-- Header and body -->
    <div class="tools-box-content">
      <!-- Header and body -->
      <div class="flex flex-row align-center">
        <div
          class="flex-spacer flex justify-end"
          v-b-tooltip.hover.right="{ variant: 'secondary' }"
          title="Assistive Tools"
        >
          <b-icon icon="info-circle"></b-icon>
        </div>
      </div>
      <div class="tool-container flex flex-col">
        <div class="tool-row flex flex-row">
          <b-button variant="success" v-on:click="saveM"> Save Mask</b-button>
        </div>
      </div>
      <div class="tool-container flex flex-col">
        <div class="tool-row flex flex-row">
          <b-button variant="warning" v-on:click="resetC"> Undo Click</b-button>
        </div>
      </div>
      <div class="tool-container flex flex-col">
        <div class="tool-row flex flex-row">
          <b-button variant="danger" v-on:click="resetAllC">
            Reset Clicks</b-button
          >
        </div>
      </div>
      <div class="tool-container flex flex-col">
        <div class="tool-row flex flex-row">
          <b-button variant="info" v-on:click="exportData">
            Export Data</b-button
          >
        </div>
      </div>
      <div>
        <b-form-input
          id="range-1"
          v-model="value"
          v-bind="changeClickRadius()"
          type="range"
          min="2"
          max="6"
        >
        </b-form-input>
        <div>Click Radius: {{ value - 1 }}</div>
        <div class="parent-container">
          <div
            class="cursor-container"
            :style="{ width: value * 2 + 'px', height: value * 2 + 'px' }"
          ></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { defineComponent } from '@vue/composition-api';
import { storeToRefs } from 'pinia';
import useEditorStore from '../state/editor';
import { backendPrefix } from '../constants';

export default defineComponent({
  setup() {
    const store = useEditorStore();
    const {
      isActiveBB,
      isActiveWand,
      isActiveRec,
      editor,
      i,
      saveMaskError,
      clickRadius,
      appliedLabel,
    } = storeToRefs(store);
    // eslint-disable-next-line
    const {
      setBB,
      setWand,
      setRec,
      saveMaskWithLabel,
      undoClick,
      resetClicks,
    } = store;
    return {
      isActiveBB,
      isActiveWand,
      isActiveRec,
      editor,
      i,
      saveMaskError,
      clickRadius,
      setBB,
      setWand,
      setRec,
      saveMaskWithLabel,
      undoClick,
      resetClicks,
      appliedLabel,
    };
  },
  data() {
    return {
      value: 4,
    };
  },
  methods: {
    changeClickRadius() {
      this.clickRadius = this.value - 1;
      console.log(this.clickRadius);
    },
    // Sets Canvas into select mode
    selectMode() {
      this.editor.set('selectMode');
    },
    saveM() {
      const singleLabel = {
        label: this.appliedLabel[0],
      };
      this.saveMaskWithLabel(singleLabel);
      if (this.appliedLabel.length === 0) {
        // eslint-disable-next-line
        this.$toast.error('Please set Label', {
          // eslint-disable-next-line
          timeout: 2000,
          // eslint-disable-next-line
        });
      } else {
        // eslint-disable-next-line
        this.$toast.success('Mask with label saved successfully', {
          // eslint-disable-next-line
          timeout: 2000,
          // eslint-disable-next-line
        });
      }
    },
    resetC() {
      this.undoClick();
      this.editor.undo();
    },
    resetAllC() {
      this.resetClicks();
      this.editor.clear();
    },
    exportData() {
      window.open(`${backendPrefix}/api/export.zip`);
    },
  },
  watch: {
    i(newI) {
      localStorage.i = newI;
    },
  },
});
</script>

<style scoped>
.Tools {
  overflow: visible;
  white-space: nowrap;
  text-align: center;
  font-family: Helvetica Neue;
  font-style: normal;
  font-weight: bold;
  height: 410px;
  align-self: flex-end;
  display: flex;
}

.tool-container {
  margin-top: 18px;
  margin-bottom: 18px;
  align-items: center;
}

.tools-box-content {
  background-color: #1f1f1f;
}

.tool-row {
  margin-bottom: 16px;
}

img {
  margin-right: 12px;
  margin-left: 12px;
}

.parent-container {
  display: flex;
  align-items: center;
  justify-content: center;
  padding-top: 5px;
}
.cursor-container {
  padding-top: 4px;
  background-color: white;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
}

label {
  display: inline-block;
  margin-bottom: 0;
}
</style>
