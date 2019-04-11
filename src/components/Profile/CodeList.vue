<template>
  <div class="results">
      <table class="table table-dark table-hover">
        <thead>
          <tr>
            <th scope="col">#</th>
            <th scope="col">Title</th>
            <th scope="col">Language</th>
            <th scope="col">Created At</th>
            <th scope="col">Updated At</th>
          </tr>
        </thead>
        <tbody>
          <Code 
            v-for="code in codes" :key=code.id
            :code=code
          >
          </Code>

          <tr v-show=!codes.length>
            <td colspan="5"> No records found! </td>
          </tr>
        </tbody>
      </table>
    </div>
</template>


<script>
import Code from './Code.vue'

export default {
  name: 'CodeList',
  props: ['codes'],
  components: {
    Code
  }
}
</script>

<style scoped>
  .results {
    display: flex;
    justify-content: center;
  }
  table {
    width: 70%;
    text-align: center;
  }
  tr {
    cursor: pointer;
  }
</style>
