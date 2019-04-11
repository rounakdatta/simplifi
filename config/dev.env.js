'use strict'
const merge = require('webpack-merge')
const prodEnv = require('./prod.env')

module.exports = merge(prodEnv, {
  NODE_ENV: '"development"',
  url: '"http://localhost:8080/"',
  api: '"http://localhost:3000/"',
  ONEAUTH: {
    url: '"https://account.codingblocks.com/"',
    clientId: '"9157831146"',
    clientSecret: '"PLmcYBDa169KQamXgNCqLoad0pVGTWdyEuc8xOrEZCSIQMWEgul9r6LveSirT7GX"',
  },
  firebase: {
    apiKey: '"AIzaSyD1bGr7kMHEWxK0X-oIKWfsZ29QNhjJA5U"',
    databaseURL: '"https://cb-ide.firebaseio.com/"',
    projectId: '"cb-ide"'
  }
})
