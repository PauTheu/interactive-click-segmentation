import Vue from 'vue';
import { BootstrapVue, IconsPlugin } from 'bootstrap-vue';
import 'bootstrap-vue/dist/bootstrap-vue.css';
import Button from 'vue-js-toggle-button';
import { createPinia, PiniaVuePlugin } from 'pinia';
import Toast from 'vue-toastification';
// Import the CSS or use your own!
import 'vue-toastification/dist/index.css';
import App from './App.vue';
// Import the CSS or use your own!
import router from './router/index';

Vue.config.productionTip = false;
Vue.use(BootstrapVue);
Vue.use(IconsPlugin);
Vue.use(Button);
Vue.use(PiniaVuePlugin);
Vue.use(Toast);
const pinia = createPinia();

// pass the router to the app config
new Vue({
  router,
  render: (h) => h(App),
  pinia,
}).$mount('#app');
