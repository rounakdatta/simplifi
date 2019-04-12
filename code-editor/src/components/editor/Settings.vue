<template>
  <div class="panel panel-default">
    <div class="headPanel panel-heading" style=" border-bottom-width:0px; ">
      <div class="btn-group">
        <b>Font:</b>
        <select @change="changeFont">
          <option v-for="font in fontOptions" :value="font" :selected="setDefault('font', font)"> {{font}} </option>
        </select>
      </div>
      <div class="btn-group">
        <b>Size:</b>
        <select @change="changeSize">
          <option v-for="size in sizeOptions" :value="size" :selected="setDefault('size', size)">{{size}}</option>
        </select>
      </div>
      <div class="btn-group">
        <b>Theme:</b>
        <select @change="changeTheme">
          <option v-for="theme in themeOptions" :value="theme" :selected="setDefault('theme', theme)">{{themeOptionsMap[theme]}}</option>
        </select>
      </div>
      <ul class="list-inline panel-actions">
        <li @click="resetEditor"><a href="#">Reset Defaults</a></li>
      </ul>
    </div>
  </div>
</template>

<script>
  export default {
    name: 'settings',
    data () {
      return {
        themeOptions: ['vs-dark', 'vs', 'hc-black'],
        themeOptionsMap: {
          'vs-dark': 'Visual Studio Dark',
          'vs': 'Visual Studio',
          'hc-black': 'High Contract Dark'
        },
        fontOptions: ['Lucida Console', 'Anonymous Pro', 'Courier', 'Droid Sans Mono', 'Inconsolata', 'Source Code Pro', 'Ubuntu Mono'],
        sizeOptions: Array(30).fill(0).map((el, ind) => 6 + (2 * ind)),
      }
    },
    methods: {
      changeTheme (e) {
        this.$store.commit('changeTheme', e.target.value)
      },
      changeFont (e) {
        this.$store.commit('changeFont', e.target.value)
      },
      changeSize (e) {
        this.$store.commit('changeFontSize', e.target.value)
      },
      resetEditor () {
        this.$store.commit('resetEditor')
      },
      setDefault (type, val) {
        switch (type) {
          case 'theme':
            return val === this.$store.state.theme
          case 'size':
            return val === parseInt(this.$store.state.fontSize)
          case 'font':
            return val === this.$store.state.font
        }
      }
    }
  }
</script>

<style scoped>
  .btn-group, .panel-actions {
    margin: 10px;
  }

  .panel {
    width: 100vw;
    height: 40px;
    z-index: 20;
    position: absolute;
    margin: 0;
  }

  .panel-actions {
    float: right;
  }

  .panel-heading {
    background: #272727;
    color: #fff;
    border-color: #272727;
    overflow: hidden;
  }

  .panel-heading a {
    color:#fff;
  }

  .panel select {
    z-index: 20;
    color: #202020;
    background: white !important;
    border-radius: 4px;
    overflow: hidden;
  }

  .panel select:focus {
    outline: none;
  }

  .panel select {
    height: 28px;
    padding: 4px;
    margin-left: 8px;
    border: none;
  }
</style>
