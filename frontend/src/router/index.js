import Vue from 'vue';
import VueRouter from 'vue-router';
import Settings from '../components/Settings.vue';
import InteractiveClick from '../components/InteractiveClick.vue';

Vue.use(VueRouter);

// create a vuerouter instance
const router = new VueRouter({
  mode: 'history',
  base: __dirname,
  routes: [{
    path: '/',
    component: Settings,
    name: 'home',
  },
  {
    path: '/ic',
    component: InteractiveClick,
    name: 'ic',
  },
  {
    path: '/settings',
    component: Settings,
    name: 'settings',
  },
  ],
});

export default router;
