<template>
  <div>
    Logging you IN
  </div>
</template>

<script>
import { httpGet } from '@/utils/api'
export default {
  created () {
    this.exchangeGrantCodeForToken()
  },
  methods: {
    exchangeGrantCodeForToken () {
      const { code } = this.$route.query
      httpGet('login', {code}).then(response => {
        this.$store.commit('user/authenticate', {token: response.data.token})
        return this.$store.dispatch('user/fetchUser')
      }).then(() => {
        this.$router.push('/')
      })
    }
  }
}
</script>
