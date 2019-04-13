'use strict'

import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios'
import base64 from 'base-64'
import shajs from 'sha.js'
import VuexPersistence from 'vuex-persist'
import samples from '../assets/js/sample-source'
import VueClipboard from 'vue-clipboard2'
import SocialSharing from 'vue-social-sharing';
import { httpGet, httpPost } from '../utils/api'

import userModule from './user'
import firebaseModule from './firebase'

Vue.use(VueClipboard)
Vue.use(SocialSharing)
Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    code: Object.assign({}, samples),
    sampleCodes: samples,
    language: 'C++',
    languageMode: 'cpp',
    theme: 'vs-dark',
    font: 'Ubuntu Mono',
    fontSize: 16,
    showInOutBox: false,
    showSettings: false,
    customInput: '',
    customInputBuf: '', //input buffer to store customInput when toggled OFF
    output: '',
    fileName: 'download.cpp',
    isChanged: false,
    autoSave: true,
    autoSaveIntervalId: null,
    checkData: '',
    codeId: null,
    codeTitle: ''
  },
  modules: {
    user: userModule,
    firebase: firebaseModule
  },
  mutations: {
    toggleInOutBox(state) {
      state.showInOutBox = !state.showInOutBox
    },
    toogleSettings(state) {
      state.showSettings = !state.showSettings
    },
    changeLanguage(state, val) {
      const languageMode = {
        'C': 'c',
        'C++': 'cpp',
        'C#': 'csharp',
        'Java': 'java',
        'Python': 'python',
        'Javascript': 'javascript',
        'NodeJs': 'javascript',
        'Ruby': 'ruby'
      }
      const extension = {
        'C': '.c',
        'C++': '.cpp',
        'C#': '.cs',
        'Java': '.java',
        'Python': '.py',
        'Javascript': '.js',
        'NodeJs': '.js',
        'Ruby': '.rb'
      }
      state.language = val
      state.languageMode = languageMode[state.language]
      state.fileName = `download${extension[state.language]}`
    },
    updateCode(state, val) {
      state.code[state.language] = val
    },
    setCode(state, val) {
      state.code[state.language] = val
    },
    uploadCode(state, val) {
      state.code[state.language] = val
    },
    updateOutput(state, val) {
      state.output = val
    },
    fileNameChange(state, val) {
      state.fileName = val
    },
    changeCustomInput(state, val) {
      state.customInput = val
    },
    changeTheme(state, val) {
      state.theme = val
    },
    changeFont(state, val) {
      state.font = val
    },
    changeFontSize(state, val) {
      state.fontSize = val
    },
    setCheckData(state, val = '') {
      state.checkData = shajs('sha256').update(val).digest('hex');
    },
    resetEditor(state) {
      state.theme = 'vs-dark'
      state.font = 'Ubuntu Mono'
      state.fontSize = 16
    },
    resetCode(state) {
      state.code[state.language] = samples[state.language];
      state.codeId = null
    },
    setIsChanged(state, val) {
      state.isChanged = val;
    },
    setCodeId(state, val) {
      state.codeId = val
    },
    setCodeTitle(state, val) {
      state.codeTitle = val
    }
  },
  plugins: [
    (new VuexPersistence({
      storage: window.localStorage,
      reducer: function (state) {
        const included = ['user', 'showInOutBox', 'showSettings', 'font', 'fontSize']
        console.log(state)
        return Object.keys(state)
          .filter(key => included.includes(key))
          .reduce((acc, key) => ({[key]: state[key], ...acc}), {})        
      },
      })).plugin
  ],
  actions: {
    runJs(context, {state, code, input}) {
      let jsWorker = new Worker('../../static/jsWorker.js')
      input = JSON.stringify(input)
      jsWorker.postMessage({code, input})
      return new Promise((resolve, reject) => {
        jsWorker.onmessage = function (e) {
          const output = e.data.join('\n')
          context.commit('updateOutput', output)
          if (output.match(/^Error.*$/)) {
            reject({
              result: 'complie_error'
            });
          }
          resolve({
            result: 'success',
            data: {
              testcases: [{
                result: 'success'
              }]
            }
          });
        }
      })
    },

    loadDataFromServer({state, commit, dispatch}) {
      const pasteId = state.route.params.id
      if (state.route.name !== 'saved') {
        return
      }
      return httpGet(`/code/${pasteId}`)
        .then(({data}) => {
          commit('setCodeId', data.id)
          commit('changeLanguage', data.language)
          commit('setCode', data.code)
          commit('changeCustomInput', data.customInput)
          commit('fileNameChange', data.fileName)
          commit('setCheckData', data.code),
          commit('setCodeTitle', data.title)
        })
    },
    saveDataToServer({state, commit, dispatch}) {
      if (state.checkData == shajs('sha256').update(state.code[state.language]).digest('hex'))
        return Promise.resolve({
          data: {
            id: state.codeId
          }
        });
      else {
        return httpPost(`/code`, {
          id: state.codeId || (void 0),
          language: state.language,
          code: state.code[state.language],
          customInput: state.customInput,
          fileName: state.fileName,
          title: state.codeTitle
        }).then(response => {
          const { data } = response
          commit('setCodeId', data.id)
          commit('setCheckData', data.code)
          return response
        })
      }
    },
    runCode({state, commit, dispatch}) {
      let lang = 'c'
      switch (state.language) {
        case 'C++':
          lang = 'cpp';
          break
        case 'C#':
          lang = 'csharp';
          break
        case 'Javascript':
          lang = 'jsv';
          break
        case 'Java':
          lang = 'java';
          break
        case 'Python':
          lang = 'py2';
          break
        case 'NodeJs':
          lang = 'js';
          break
        case 'Ruby':
          lang = 'ruby';
          break;
      }

      if (lang === 'jsv') {
        return dispatch('runJs', {
          state: state,
          code: state.code[state.language],
          input: state.customInput
        });
      }

      const config = {
        headers: {
          'Access-Token': '79f3c2f8301fc60565de003f4ac76a1d4e5242cb0836995ec2bd28fd083ce86f',
          "Access-Control-Allow-Origin": "*",
          "Access-Control-Allow-Headers": "Origin, X-Requested-With, Content-Type, Accept"
        }
      }

      const config2 = {
        headers: {
          'Access-Token': '79f3c2f8301fc60565de003f4ac76a1d4e5242cb0836995ec2bd28fd083ce86f',
          "Access-Control-Allow-Origin": "*",
          "Access-Control-Allow-Headers": "Origin, X-Requested-With, Content-Type, Accept",
          'Content-Type': "application/x-www-form-urlencoded",
          "content-type": "multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW",
        }
      }

      var codeSource = state.code[state.language];

      // send the code first to jsonstore
      axios.post('https://www.jsonstore.io/d2a87b276883fef8b464807a65dc270bf21094ebae987ca5973c95880bd27f40?=', {
        "code": codeSource,
        "language": state.language
      }, config)
        .then(({data}) => {
          console.log(data);
          return data;
        });

      // tell the flaskk server to get the code from jsonstore
      axios.get("http://localhost:5000/ping", { crossdomain: true })
      .then(({data}) => {
        console.log(data);

        if (data['title'] != undefined) {
          alert("Found a serious vulnerability: " + data['title']);
          var win = window.open(data['url'], '_blank');
        }
      })
    
      return axios.post('https://judge.cb.lk/api/submission', {
        lang,
        source: base64.encode(state.code[state.language]),
        test_count: 1,
        input: [base64.encode(state.customInput)],
        expected_output: [''],
        get_output: true,
        wait: true
      }, config)
        .then(({data}) => {
          const output = data.result == 'compile_error' ? data.error : data.data.testcases[0].output
          commit('updateOutput', base64.decode(output))
          return data;
        })
    }
  }
})
