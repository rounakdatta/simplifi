<template>
  <div id="shareId" class="btn-group">
    <button id="shareButton" type="button" class="btn btn-sm btn-menu" @click="getURL">
      Share<i class="fa fa-reply-all" aria-hidden="true"></i>
    </button>
    <div name="shareModal" v-show="showShareModal">
      <div class="modal-mask">
        <div class="modal-wrapper">
          <div class="modal-container">
            <div class="modal-header text-center">
              <h3>Share</h3>
            </div>

            <div class="modal-body text-center">
              <div class="shortURLBox">
                <input id="shareURL" v-model="shortURL" type="url" title="Share Shorten URL" readonly="readonly">
                <button type="button" class="btn btn-sm btn-run"
                        v-clipboard:copy="shortURL"
                        v-clipboard:success="onCopy">Copy!
                </button>
              </div>
              <social-sharing :url="shortURL"
                              title="Here is my code. Find it at Coding Blocks IDE."
                              description="Here is my code. Find it at Coding Blocks IDE."
                              quote="Here is my code. Find it at Coding Blocks IDE."
                              hashtags="cbide,codingblocks,code"
                              twitter-user="CodingBlocksIN"
                              inline-template>
                <div class="socialShareGroup">
                  <network network="email">
                    <span class="socialShare"><i class="fa fa-envelope"></i> Email</span>
                  </network>
                  <network network="facebook">
                    <span class="socialShare"><i class="fa fa-facebook"></i> Facebook</span>
                  </network>
                  <network network="twitter">
                    <span class="socialShare"><i class="fa fa-twitter"></i> Twitter</span>
                  </network>
                </div>
              </social-sharing>
            </div>

            <div class="modal-footer">
              <button class="btn btn-run btn-sm" @click="showShareModal=false">
                Close
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  import axios from 'axios'

  export default {
    name: 'Share',
    data() {
      return {
        showShareModal: false,
        longURL: '',
        shortURL: ''
      }
    },
    props: ['url'],
    methods: {
      getURL() {
        this.showShareModal = true;
        if (window.location.href !== this.longURL)
          axios.post('https://cb.lk/api/v1/shorten', {
            url: window.location.href,
            code: '',
            secret: ''
          }).then((response) => {
            this.longURL = window.location.href;
            this.shortURL = 'https://cb.lk/' + response.data.shortcode;
          })

        // // only enablePairMode if not already pairing
        // const state = this.$store.state
        // if (!state.isPairing)
        //   this.$store.commit('enablePairMode', {keepText: true})

        // const middle = state.codeId ? '/s/' + state.codeId + '?ref=' : '/j/'
        // this.shortURL = window.location.host + middle + state.firebase.ref
      },
      onCopy() {
        this.$notify({
          text: 'Short URL Copied Successfully',
          type: 'success'
        })
      }
    }
  }
</script>

<style scoped>
  i.fa {
    margin-left: 4px;
  }

  .shortURLBox {
    margin: 10px 0;
  }

  #shareURL {
    font-size: 18px !important;
    color: #202020;
    border-radius: 50px !important;
    border-color: #e31d3b !important;
    border: 2px solid;
    text-align: center;
  }

  .socialShareGroup {
    margin: 10px 0;
  }

  .socialShare {
    cursor: pointer !important;
    margin: 0 15px;
  }
</style>
