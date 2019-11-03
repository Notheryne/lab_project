import Vue from 'vue'
import Router from 'vue-router'

import App from './App.vue'
import Character from './components/Character.vue'
import Expedition from './components/Expedition.vue'
import Arena from './components/Arena.vue'
import Healer from'./components/Healer.vue'
import Trader from'./components/Trader.vue'
import Manage from'./components/Manage.vue'
import Logout from'./components/Logout.vue'



Vue.use(Router);

const router = new Router({
  routes: [
    {
      path: '/',
      name: 'app',
      component: App
    },
    {
      path: '/character',
      name: 'character',
      component: Character
    },
    {
      path: '/expedition',
      name: 'expedition',
      component: Expedition
    },
    {
      path: '/arena',
      name: 'arena',
      component: Arena
    },
    {
      path: '/healer',
      name: 'healer',
      component: Healer
    },
    {
      path: '/trader',
      name: 'trader',
      component: Trader
    },
    {
      path: '/manage',
      name: 'manage',
      component: Manage
    },
    {
      path: '/logout',
      name: 'logout',
      component: Logout
    },
  ]
});

new Vue({
  el: '#app',
  router,
  render: h => h(App)
});
