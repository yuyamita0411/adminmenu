<template>
  <nav :class="navstatus">
    <router-link :to="`/language/${lang}`" class="menu-list-button menuicon"><img :src="homeicon"></router-link>
    <router-link to="/page/list" class="menu-list-button menuicon"><img :src="pagelisticon"></router-link>
    <router-link :to="`/category/${lang}`" class="menu-list-button menuicon"><img :src="categoryicon"></router-link>
    <router-link :to="`/common/${lang}`" class="menu-list-button menuicon"><img :src="commonicon"></router-link>
  </nav>
  <div class="menubutton-wrapper">
    <button
      class="menu-open-close-button menuicon"
      @click="openButton">
      <img :src="buttonsrc">
    </button>
  </div>
  <section class="contents">
    <LoadingIconview class="dashboardloading w-100 d-inline-block text-center" v-if="isLoading"/>
    <router-view/>
  </section>
  <Modal />
</template>

<script lang="ts">
import { Vue, Options } from "vue-class-component";
import { mapState } from 'vuex';
import { PATH, TAG } from './module/prop';
import Modal from '@/components/Modal.vue';
import {store} from './store/common/index';

import LoadingIconview from '@/components/icon/loadingIcon.vue';

@Options({
    computed: {
      ...mapState(['isLoading'])
    },
    components: {
        Modal,
        LoadingIconview
    }
})

export default class App extends Vue {

    path: PATH = new PATH();
    tag: TAG = new TAG();

    navstatus = 'nav-open'
    buttonsrc = this.path.buttonsrc;
    homeicon = this.path.homeicon;
    pagelisticon = this.path.pagelisticon;
    categoryicon = this.path.categoryicon;
    commonicon = this.path.commonicon;
    lang = process.env.VUE_APP_FromCode;

    created(){
        store.commit('updateStoreObj', { target: 'pageinfo', key: 'base_url', value: process.env.VUE_APP_API_Base_URL });
    }

    openButton () {
        this.navstatus = this.navstatus === 'nav-open' ? 'nav-close' : 'nav-open';
        this.buttonsrc = this.navstatus === 'nav-open' ? this.path.openicon : this.path.closeicon;
    }
}
</script>

<style lang="scss">
@import "./views/style.scss";
nav {
  padding: 4rem .5rem 0 .5rem;
  position: fixed;
  top: 0;
  height: 100vh;
  box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.3);
  width:3rem;
  background: #ffff;
  z-index:1;

  a {
    width: 100%;
    text-align: left;
    display: inline-block;
    font-weight: bold;
    color: #2c3e50;
    margin-bottom: .5rem;

    &.router-link-exact-active {
      color: #42b983;
    }
  }
  .menu-list-button {
    width: 2rem;
    height: 2rem;
    clear: both;
    padding: .25rem 1rem 1rem .25rem;
  }
  .menu-list-button{
    box-shadow: 2px 3px 1px -2px rgba(0, 0, 0, 0.3);
  }
  .menu-list-button:hover{
    box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.3);
  }
  .menu-list-button,
  .menu-list-button:hover {
    transition: all .25s;
  }
  .menu-list-button {
    float: left;
  }
}
.nav-open {
  left: 0;
  opacity: 1;
}
.nav-close {
  left: -3rem;
  opacity: 0;
}
.nav-open,
.nav-close {
  transition: all .5s;
}
.menubutton-wrapper {
  position: fixed;
  left: .5rem;
  top: 0rem;
  z-index:2;
  button {
    padding: 0;
    background: transparent;
    border: none;
    cursor: pointer;
    img {
      display: inline-block;
      width: 100%;
    }
  }
}
.menu-open-close-button {
  width: 3rem;
  height: 3rem;
}
.menuicon {
    img {
      display: inline-block;
      width: 100%;
    }
}
.contents {
    background: rgb(0, 0, 0, 0.1);
    text-align: left;
    padding: 0 2rem 0 6rem;
    min-height: 100vh;
    float: left;
    width: 100%;
    ul {
        background: #ffff;
        padding: 1rem;
        min-height: 70vh;
    }
}
</style>