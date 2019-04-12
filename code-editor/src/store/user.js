import { setToken, httpGet } from '../utils/api'

const userModule = {
  namespaced: true,
  state: {
    currentUser: null,
    token: null,
    isAuthenticated: false
  },
  mutations: {
    authenticate (state, val) {
      state.token = val.token,
      state.isAuthenticated = true
      setToken(val.token)
    },
    setCurrentUser (state, val) {
      state.currentUser = val
    },
    logout (state) {
      state.currentUser = null
      state.token = null
      state.isAuthenticated = false
    }
  },
  actions: {
    fetchUser ({ state, commit}) {
      httpGet('/users/me').then(res => {
        commit('setCurrentUser', res.data)
      })
    }
  }
}

export default userModule