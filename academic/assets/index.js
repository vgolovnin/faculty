import Vue from 'vue'
import VueResource from 'vue-resource'
import VueRouter from 'vue-router'
import Cookies from 'js-cookie'
import _ from 'lodash'

import './css/main.css'

Vue.use(VueRouter)
Vue.use(VueResource)
Vue.http.headers.common['X-CSRFToken'] = Cookies.get('csrftoken');

import Reserve from './vue/Reserve.vue'
import Reports from './vue/Reports.vue'

const router = new VueRouter({
    base: process.env.APP_URL,
    mode: 'history',
    routes: [
    {path: '/', component: Reserve},
    {path: '/reports/', component: Reports},
]})

new Vue({router}).$mount('#fs')