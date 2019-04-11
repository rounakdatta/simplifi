<template>
  <pre id="editor"></pre>
</template>

<script>
  import * as monaco from 'monaco-editor';
  import firepad from 'firepad';

  export default {
    name: 'monaco-editor',
    mounted() {
      addEventListener('dragover', this.dragOverHandler, false)
      addEventListener('drop', this.dropHandler, false)

      this.editor = 
        monaco.editor.create(document.getElementById('editor'), {
          // value: this.$store.state.code[this.$store.state.language],
          minimap: {
            showSlider: false
          },
          language: this.$store.state.languageMode,
          automaticLayout: true,
          dragAndDrop: true,
          fontFamily: this.$store.state.font,
          fontSize: this.$store.state.fontSize,
          parameterHints: true,
          renderIndentGuides: true,
          lineNumbersMinChars: 3,
          theme: this.$store.state.theme,
          scrollBeyondLastLine: true
        })

      this.editor.onDidChangeModelContent(() => {
        this.$store.commit('updateCode', this.editor.getValue())
      })

      this.$store.subscribe((mutation, state) => {
        switch (mutation.type) {
          case "resetCode":
          case "uploadCode":
          case "setCode":
          case "changeLanguage":
            monaco.editor.setModelLanguage(this.editor.getModel(), this.$store.state.languageMode)
            this.editor.setValue(this.$store.state.code[this.$store.state.language] || '')
            break;
          case "changeTheme":
            monaco.editor.setTheme(this.$store.state.theme)
            break;
          case "changeFont":
            this.editor.updateOptions({
              fontFamily: this.$store.state.font
            })
            break;
          case "changeFontSize":
            this.editor.updateOptions({
              fontSize: this.$store.state.fontSize
            })
            break;
          case "resetEditor":
            monaco.editor.setTheme(this.$store.state.theme);
            this.editor.updateOptions({
              fontFamily: this.$store.state.font,
              fontSize: this.$store.state.fontSize
            })
            break;
          case "firebase/enablePairMode": 
            const value = this.editor.getValue()
            // need to clear editor before initializing firepad
            this.editor.setValue('')
            // setup firepad to track the editor now
            firepad.fromMonaco(this.$store.state.firebase.ref, this.editor)
            
            if (mutation.payload && mutation.payload.keepText) {
              this.editor.setValue(value)
            }

            this.$store.commit('setCodeTitle', `CodePairing: #${this.$store.state.firebase.ref.key}`)
            break;
        }
      })

      this.$store.subscribe((plugin, state) => {
        switch (plugin.type) {
          case "createPersistedState":
            monaco.editor.setTheme(this.$store.state.theme)
            this.editor.updateOptions({
              fontFamily: this.$store.state.font,
              fontSize: this.$store.state.fontSize
            })
            break;
        }
      })

      if (!this.$store.state.isPairing) {
        this.editor.setValue(this.$store.state.code[this.$store.state.language])
      }
    },
    destroyed() {
      removeEventListener('dragover', this.dragOverHandler, false)
      removeEventListener('drop', this.dropHandler, false)
    },
    methods: {
      dragOverHandler(e) {
        e.preventDefault()
        e.stopPropagation()
      },
      dropHandler(e) {
         e.preventDefault()
         e.stopPropagation()
         const dt = e.dataTransfer
         if (dt && dt.types && (dt.types.indexOf ?
             dt.types.indexOf('Files') !== -1 : dt.types.contains('Files'))) {
           if (File && FileReader) {
             const reader = new FileReader()
             const file = dt.files[0]
             reader.readAsText(file, 'UTF-8')
             reader.onload = (e) => {
               console.log('Uploaded File: ' + file.name)
               this.$notify({
                text: 'Code Uploaded Successfully',
                type: 'success'
               })
               this.$store.commit('uploadCode', e.target.result)
               this.$store.commit('fileNameChange', file.name)
             };
           }
         }
       }
    }
  }
</script>

<style scoped>
  #editor {
    overflow: hidden;
    position: relative;
    border: none;
    height: calc(100vh - 40px);
    width: 100vw;
    z-index: 10;
    margin: 0;
    border-radius: 0;
    padding-top: 35px;
  }
  .inputarea {
    opacity: 0;
  }
</style>
