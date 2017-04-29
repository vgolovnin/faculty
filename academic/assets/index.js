import Vue from 'vue'
import VueResource from 'vue-resource'
import VueRouter from 'vue-router'
import Cookies from 'js-cookie'
import _ from 'lodash'

import './css/main.css'

Vue.use(VueRouter)
Vue.use(VueResource)
Vue.http.headers.common['X-CSRFToken'] = Cookies.get('csrftoken');


const router = new VueRouter({
    base: process.env.APP_URL,
    mode: 'history',
    routes: [
    {path: '/', component: require('./vue/Reserve.vue')},
    {path: '/reports/', component: require('./vue/Reports.vue')},
]})

new Vue({router}).$mount('#fs')