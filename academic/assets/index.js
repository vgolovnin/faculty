import Vue from 'vue'
import VueResource from 'vue-resource'
import Cookies from 'js-cookie'
import _ from 'lodash'

import './css/main.css'


Vue.use(VueResource)
Vue.http.headers.common['X-CSRFToken'] = Cookies.get('csrftoken');

import Reserve from './vue/Reserve.vue'
import Reports from './vue/Reports.vue'

const routes = {
    '/' : Reserve,
    '/reports/': Reports,
}



var vm = new Vue({
    el: '#app',
    data: {
        currentRoute: window.location.pathname,
    },
    computed: {
        ViewComponent() {
            return routes[this.currentRoute] || null
        },
    },
  render(h) { return h(this.ViewComponent); }
})


window.addEventListener('popstate', () => {
  vm.currentRoute = window.location.pathname
})

