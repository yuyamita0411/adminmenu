<template>
  記事リスト
  <ul>
        <li v-for="(value, key, index) in pagelist" :key="key">
            <router-link :to="`/${value}`">{{key+1}}. {{pageandtitle[value]}}</router-link>
            <div class="addcontent-wrapper">
                <button
                @click="addBlockFunc(key)"
                :class="`addcontentbutton`"
                ><img
                :index="index"
                :src="addcontenticon"></button>
                <span class="bottom-border addcontent-border"></span>
            </div>
            <button
            :class="`trashbutton`">
                <img
                :src="trashicon"
                @click="deleteElement(key)"
                >
            </button>
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
import {store} from '../store/index';
import { GenericObject } from '../module/type';
import { PROP } from '../module/prop';
import { FUNCTION } from '../module/function';

export default class articleLists extends Vue {
    pagelist: string[] = [];
    pageandtitle = {}
    func = new FUNCTION();
    prop = new PROP();

    addcontenticon = this.prop.addcontenticon;
    trashicon = this.prop.trashicon;

    created () {
        this.getFileDirectory();
    }
    addBlockFunc (key: number) {
        console.log(this.pagelist);
        this.pagelist[key+1] = `${this.getMaxNumber(this.pagelist)+1}/language/jp`;
        //{0: "1/language/jp"}
        console.log(this.getMaxNumber(this.pagelist));
        console.log(key);
    }

    private getMaxNumber = (arr: string[]): number => {
        return arr
            .map(item => {
                const match = item.match(/^\d+/);
                return match ? parseInt(match[0], 10) : 0;
            })
            .reduce((max, curr) => curr > max ? curr : max, 0);
    };

    deleteElement(key: number) {
        console.log(this.pagelist);
        delete this.pagelist[key];
        console.log(key);
    }
    getFileDirectory () {
        this.func.postAPI (
            `${store.state.pageinfo.base_url}${process.env.VUE_APP_fileDirectory}`,
            {filePath: process.env.VUE_APP_articleDirPath},
            (response: GenericObject) => {
                this.pagelist = response.data.map((obj: string) => {
                    return `${obj}/language/jp`;
                });
                this.pagelist.forEach(() => {
                    this.getTitleFromPageId();
                });
            }
        );
    }
    getTitleFromPageId () {
        this.func.postAPI (
            `${store.state.pageinfo.base_url}${process.env.VUE_APP_filetitle}`,
            {filePath: this.pagelist},
            (response: GenericObject) => {
                this.pageandtitle = response.data;
            }
        );
    }
}
</script>