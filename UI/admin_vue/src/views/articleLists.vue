<template>
  記事リスト
  <ul>
      <li v-for="(value, key) in pagelist" :key="key">
          <router-link :to="`/${value}`">{{pageandtitle[value]}}</router-link>
          <span class="bottom-border"></span>
      </li>
  </ul>
</template>

<style lang="scss" scoped>
  ul li {
    position: relative;
    list-style: none;
    padding: .5rem 0;
  }
  .bottom-border {
    bottom: 0;
  }
</style>

<script lang="ts">
import { Vue } from "vue-class-component";
import axios from 'axios';
import {store} from '../store/index';
import { GenericObject } from '../module/type';

export default class articleLists extends Vue {
    pagelist: string[] = [];
    pageandtitle = {}

    created () {
        this.getFileDirectory();
    }
    getFileDirectory () {
        axios.post(`${store.state.pageinfo.base_url}${process.env.VUE_APP_fileDirectory}`,
        {
            filePath: process.env.VUE_APP_articleDirPath
        }
        )
        .then((response: GenericObject) => {
            response.data.forEach((obj: string) => {
                this.pagelist.push(`${obj}/language/jp`);
                console.log(obj);
                this.getTitleFromPageId();
            });
        })
        .catch((error: GenericObject) => {
            console.error(error);
        });
    }
    getTitleFromPageId () {
        axios.post(`${store.state.pageinfo.base_url}${process.env.VUE_APP_filetitle}`,
        {
            filePath: this.pagelist
        }
        )
        .then((response: GenericObject) => {
            this.pageandtitle = response.data
            console.log(response);
            console.log(this.pageandtitle);
        })
        .catch((error: GenericObject) => {
            console.error(error);
        });
    }
}
</script>