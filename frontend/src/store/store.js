import Vue from 'vue'
import Vuex from 'vuex'
import actions from './actions';
import mutations from './mutations';
import getters from './getters';


Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    products: null,
    cart: [],
    user: null,
    loading: false,
    cartLoading: 0,
    loadingText: ""
  },
  getters,
  mutations,
  actions
})