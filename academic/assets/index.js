import Vue from 'vue'
import VueResource from 'vue-resource'
import VueRouter from 'vue-router'
import Cookies from 'js-cookie'
import vmodal from 'vue-js-modal' 
import _ from 'lodash'

import './css/main.css'

Vue.use(VueRouter)
Vue.use(VueResource)
Vue.use(vmodal) 
Vue.http.headers.common['X-CSRFToken'] = Cookies.get('csrftoken');


const router = new VueRouter({
    base: process.env.APP_URL,
    mode: 'history',
    routes: [
    {path: '/', component: require('./vue/Reserve.vue')},
    {path: '/reports/', component: require('./vue/Reports.vue')},
]})

const vue = new Vue({
    router: router,
    components: {
        'navbar': require('./vue/NavBar.vue'),
    }
}).$mount('#fs');

