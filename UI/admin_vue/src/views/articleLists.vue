<template>
    <div class="content-wrapper">
        <h2>記事リスト</h2>
        <table class="article-list-table w-100">
            <thead>
                <tr>
                    <td class="font-weight-bold">タイトル</td>
                    <td class="font-weight-bold">カテゴリ</td>
                </tr>
            </thead>
            <tbody>
                <template v-for="(value, key, index) in pagelist" :key="key">
                    <tr v-if="pagelist[key]">
                        <td v-if="pagelist[key]">
                            <router-link :to="path.detailDirFormat(value)"
                            class="text-decoration-none accent-text-color">
                            {{pageInfoArr[value] && pageInfoArr[value]["title"] ? pageInfoArr[value]["title"] : ''}}
                            </router-link>
                        </td>
                        <td v-if="pagelist[key]"
                        class="text-decoration-none accent-text-color">
                            <select v-model="selectedCategories[value]">
                                <option
                                v-for="(info, pageInfoKey) in pageInfoArr"
                                :key="pageInfoKey"
                                :value="info.categoryID">
                                    {{ info.category }}
                                </option>
                            </select>
                        </td>
                        <td>
                            <button
                            v-if="pagelist[key]"
                            class="trashbutton position-relative">
                                <img
                                :src="trashicon"
                                @click="deleteElement(value)"
                                >
                            </button>
                        </td>
                    </tr>
                    <tr v-if="pagelist[key] && value == maxPageNum">
                        <td></td>
                        <td>
                            <div
                            class="addcontent-wrapper"
                            >
                                <button
                                @click="addBlockFunc(value)"
                                class="addcontentbutton"
                                >
                                    <img
                                    :index="index"
                                    :src="addcontenticon">
                                </button>
                            </div>
                        </td>
                        <td></td>
                    </tr>
                </template>
            </tbody>
        </table>
    </div>
</template>

<script lang="ts">
import { Vue } from "vue-class-component";
import {store} from '../store/common/index';
import { GenericObject } from '../module/type';
import { PATH, TAG } from '../module/prop';
import { API } from '../module/function';

export default class articleLists extends Vue {
    pagelist: string[] = [];
    pageInfoArr = {}
    maxPageNum=1;
    path: PATH = new PATH();
    tag: TAG = new TAG();

    selectedCategories: GenericObject = {};

    addcontenticon = this.path.addcontenticon;
    trashicon = this.path.trashicon;

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
        API.post (
            `${store.state.pageinfo.base_url}${process.env.VUE_APP_rebaseDirEndpoint}`,
            {filePath: this.pagelist},
            (response: GenericObject) => {
                console.log(response);
            }
        );
    }
    getFileDirectory () {
        API.post (
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
        API.post (
            `${store.state.pageinfo.base_url}${process.env.VUE_APP_filetitle}`,
            {filePath: this.pagelist},
            (response: GenericObject) => {

                this.selectedCategories = Object.keys(response.data).reduce((acc, key) => ({
                ...acc,
                [key.toString()]: response.data[key].categoryID.toString(),
                }), {});

                this.pageInfoArr = response.data;
                this.maxPageNum = this.getMaxNumber(this.pagelist);
                console.log("selectedCategoriesselectedCategoriesselectedCategoriesselectedCategoriesselectedCategories");
                console.log(this.selectedCategories);
            }
        );
    }
}
</script>

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
.article-list-table thead {
    background: #0686b2;
    color: #ffff;
}
.article-list-table tbody > tr:nth-child(2n):not(:last-child) {
    background: rgba(0,0,0,.1);
}
.article-list-table tbody > tr:nth-child(2n+1):not(:last-child) {
    background: #ffff;
}
.article-list-table tr td {
    padding: .5rem;
}
.content-wrapper {
    table {
        box-shadow: .5px .5px 4px rgba(0,0,0,.3);
    }
}
</style>