<template>
  記事リスト
  <ul>
    <li v-for="(value, key, index) in pagelist" :key="key">
        <div
        v-if="pagelist[key]"
        >
            <router-link :to="`/${value}/language/jp`">{{value}}. {{pageandtitle[value]}}</router-link>
            <div
            class="addcontent-wrapper"
            v-if="value == maxPageNum"
            >
                <button
                @click="addBlockFunc(value)"
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
                @click="deleteElement(value)"
                >
            </button>
        </div>
    </li>
  </ul>
</template>

<style lang="scss" scoped>
  ul li {
    position: relative;
    list-style: none;
    div {
        padding: .5rem 0;
    }
  }
  .bottom-border {
    bottom: 0;
  }
</style>

<script lang="ts">
import { Vue } from "vue-class-component";
import {store} from '../store/common/index';
import {articleListStore} from '../store/articleList/index';
import { GenericObject } from '../module/type';
import { PROP } from '../module/prop';
import { FUNCTION } from '../module/function';

export default class articleLists extends Vue {
    pagelist: string[] = [];
    pageandtitle = {}
    maxPageNum=1;
    func = new FUNCTION();
    prop = new PROP();

    addcontenticon = this.prop.addcontenticon;
    trashicon = this.prop.trashicon;

    created () {
        this.getFileDirectory();
    }
    addBlockFunc (key: number) {
        this.maxPageNum = this.getMaxNumber(this.pagelist)+1;
        this.pagelist[Number(key)+1] = `${this.maxPageNum}`;
        this.rebaseDirectory();
        this.getFileDirectory();
    }

    private getMaxNumber = (arr: string[]): number => {
        return arr
            .map(item => {
                const match = item.match(/^\d+/);
                return match ? parseInt(match[0], 10) : 0;
            })
            .reduce((max, curr) => curr > max ? curr : max, 0);
    };

    deleteElement(value: number) {
        delete this.pagelist[value];
        if (value === this.maxPageNum) {
            this.maxPageNum = value;
        }
        this.maxPageNum = this.getMaxNumber(this.pagelist);
        //ここでディレクトリ更新
        this.rebaseDirectory();
    }
    rebaseDirectory () {
        this.func.postAPI (
            `${store.state.pageinfo.base_url}${process.env.VUE_APP_rebaseDirEndpoint}`,
            {filePath: this.pagelist},
            (response: GenericObject) => {
                console.log(response);
            }
        );
    }
    getFileDirectory () {
        this.func.postAPI (
            `${store.state.pageinfo.base_url}${process.env.VUE_APP_fileDirectory}`,
            {filePath: process.env.VUE_APP_articleDirPath},
            (response: GenericObject) => {
                response.data.forEach((obj: string) => {
                    this.pagelist[Number(obj)] = obj;
                });
                this.getTitleFromPageId();
            }
        );
    }
    getTitleFromPageId () {
        this.func.postAPI (
            `${store.state.pageinfo.base_url}${process.env.VUE_APP_filetitle}`,
            {filePath: this.pagelist},
            (response: GenericObject) => {
                this.pageandtitle = response.data;
                this.maxPageNum = this.getMaxNumber(this.pagelist);
            }
        );
    }
}
</script>