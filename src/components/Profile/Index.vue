<template>
  <div class="page">
    <h1> 
      <router-link tag="i" class="fa fa-arrow-left" to="/"></router-link>
      Welcome {{userStore.currentUser.firstname}} 
    </h1>
    <div class="searchUtil">
    <input class="black search" type="text" placeholder="🔍 Search by title..." v-model=searchStr @change=searchTextChanged>
    </div>
    <CodeList :codes=codes></CodeList>
  </div>
</template>


<script>
import { httpGet } from '@/utils/api'
import { mapState } from 'vuex'

import CodeList from './CodeList.vue'

export default {
  name: 'profile',
  components: {
    CodeList
  },
  data () {
    return {
      searchStr: '',
      codes: []
    }
  },
  computed: mapState({
    userStore: 'user'
  }),
  async created () {
    this.fetchCodes()
  },
  methods: {
    async fetchCodes (title = '', offset = 0, limit) {
      const { data } = await httpGet('/code', {
        filter: {
          title: {
            $iLike: `%${title}%`
          }
        },
        offset,
        limit
      })

      this.codes = data.codes
    },
    searchTextChanged (e) {
      this.fetchCodes(this.searchStr)
    },
    goBack () {
      this.$router.push({ name: 'root'})
    }
  }
  
}
</script>

<style scoped>
  .page {
    height: 100vh;
    padding: 1% 10%;
    overflow: auto;
  }
  h1 {
    color: whitesmoke;
  }
  .searchUtil {
    display: flex;
    justify-content: center;
    font-size: 35px;
  }
  input.search {
    width: 50%;
  }
  i {
    cursor: pointer;
  }
</style>