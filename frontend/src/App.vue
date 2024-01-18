<template>
  <div id="header">
    <head>
      <link
        rel="stylesheet"
        href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css"
        integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm"
        crossorigin="anonymous"
      />
      <title>Interactive LabelAI</title>
    </head>

    <nav
      class="navbar navbar-expand-lg navbar-light"
      style="background-color: #1f1f1f"
    >
      <a class="navbar-brand" href="/" style="color: white">
        <img
          src="../public/logo.png"
          width="30"
          height="30"
          class="d-inline-block align-mid"
          alt=""
        />
        Interactive Segmentation</a
      >
      <button
        class="navbar-toggler"
        type="button"
        data-toggle="collapse"
        data-target="#navbarSupportedContent"
        aria-controls="navbarSupportedContent"
        aria-expanded="false"
        aria-label="Toggle navigation"
      >
        <span class="navbar-toggler-icon"></span>
      </button>

      <div class="collapse navbar-collapse flex" id="navbarSupportedContent">
        <div class="flex-spacer"></div>
        <ul class="navbar-nav">
          <li class="nav-item">
            <a
              v-show="!home_class"
              class="nav-link"
              href="#"
              style="color: white"
              @click="exportData()"
              >Export Data</a
            >
          </li>
        </ul>
      </div>
    </nav>

    <div class="app-content">
      <router-view></router-view>
    </div>
  </div>
</template>

<script>
import { defineComponent } from '@vue/composition-api';
import { storeToRefs } from 'pinia';
import { backendPrefix } from './constants';
import useEditorStore from './state/editor';

export default defineComponent({
  setup() {
    const store = useEditorStore();
    const { i, labelCount } = storeToRefs(store);

    return {
      i,
      labelCount,
    };
  },
  data() {
    return {
      // eslint-disable-next-line
      home_class: this.$route.path === '/' ? true : false,
      // eslint-disable-next-line
      labelling_class: this.$route.path === '/labelling' ? true : false,
      // eslint-disable-next-line
      settings_class: this.$route.path === '/settings' ? true : false,
    };
  },
  methods: {
    exportData() {
      window.open(`${backendPrefix}/api/export.zip`);
    },
  },
  watch: {
    i() {},
  },
});
</script>

<style>
html,
body,
#header {
  overflow: hidden;
  height: 100%;
  background: #fafafa;
}

#header {
  font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

.page-root {
  height: calc(100% - 32px);
  padding: 16px;
}

.flex {
  display: flex;
  flex-wrap: wrap;
}

.flex-row {
  flex-direction: row;
  align-items: center;
}

.flex-col {
  flex-direction: column;
}

.flex-spacer {
  flex-grow: 1;
}

.justify-start {
  justify-content: start;
}

.justify-center {
  justify-content: center;
}

.justify-end {
  justify-content: flex-end;
}

.align-start {
  align-items: start;
}

.align-center {
  align-items: center;
}

.align-stretch {
  align-items: stretch;
}

.align-self-start {
  align-self: flex-start;
}

.justify-self-start {
  justify-self: flex-start;
}

#navbar {
  background-color: #686868;
}

.navbar {
  height: 56px;
}

.app-content {
  overflow: auto;
  height: calc(100% - 56px);
}

.full-height {
  height: 100%;
}

.tools-box-content {
  padding: 8px;
  background: rgba(65, 65, 65, 1);
  border-radius: 16px;
  color: #fff;
  margin: 0 64px;
  width: 240px;
}
</style>
