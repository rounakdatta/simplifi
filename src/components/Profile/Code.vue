<template>
  <tr @click=goToSnippet>
    <td>{{code.id}}</td>
    <td>{{code.title}}</td>
    <td>{{code.language}}</td>
    <td>{{createdAt}}</td>
    <td>{{updatedAt}}</td>
  </tr>
</template>


<script>
import moment from 'moment'

export default {
  name: 'Code',
  props: ['code'],
  computed: {
    createdAt () {
      return moment(this.code.createdAt).format('DD MMM YYYY hh:mm:ss')
    },
    updatedAt () {
      return moment(this.code.updatedAt).format('DD MMM YYYY hh:mm:ss')
    }
  },
  methods: {
    goToSnippet () {
      const route = this.$router.resolve({ path: '/s/' + this.code.id})
      window.open(route.href, "_blank")
    }
  }
}
</script>
