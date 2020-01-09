import Vue from 'vue'
import Vuetify from 'vuetify/lib'

Vue.use(Vuetify)

const opts = {
    theme: {
      themes: {
        light: {
            primary: '#DCE1E9',
            secondary: '#363732',
            accent: '#e88b01'
        },
      },
    },
  }

export default new Vuetify(opts)