<template>
    <div class="content-wrapper">
        <div class="mb2rem">
            <h2>カテゴリ一覧</h2>
            <table class="list-chart w-100">
                <tbody>
                    <tr v-for="(cat, index) in catinfo" :key="cat.category">
                        <td class="p05rem">
                            <router-link :to="`${currentPath}/${index}`" class="menu-list-button menuicon">
                            {{cat.category}}
                            </router-link>
                        </td>
                        <td class="p05rem"><button type="button" @click="deleteData(index)">
                            <img
                            :src="trashicon"
                            class="w2rem h2rem cursor"
                            >
                        </button></td>
                    </tr>
                </tbody>
            </table>
        </div>
        <div>
            <h2>カテゴリー追加</h2>
            <table class="list-chart w-100">
                <tbody>
                    <tr>
                        <td class="font-weight-bold p05rem">カテゴリ名</td>
                        <td class="p05rem"><input type="text" class="w-100 lh2rem font1rem" v-model="categoryName" @input="editCatInfo('categoryName', $event.target.value)"></td>
                    </tr>
                    <tr>
                        <td class="font-weight-bold p05rem">ディスクリプション</td>
                        <td class="p05rem"><input type="text" class="w-100 lh2rem font1rem" v-model="categoryDescription" @input="editCatInfo('categoryDescription', $event.target.value)"></td>
                    </tr>
                    <tr>
                        <td class="font-weight-bold p05rem">og画像</td>
                        <td class="p05rem"><input type="text" class="w-100 lh2rem font1rem" v-model="categoryOgImgPath" @input="editCatInfo('categoryOgImgPath', $event.target.value)"></td>
                    </tr>
                </tbody>
            </table>
            <div class="submitButtonWrapper">
                <div class="submitButtonInner">
                    <button
                    class="submitButton button_blue"
                    @click="addCategory"
                    >カテゴリを追加する</button>
                </div>
            </div>
            <div class="mb2rem">
                <h2>翻訳する</h2>
                <h3>翻訳に失敗した言語、まだ翻訳が済んでない言語一覧</h3>
                <div>
                    <div
                    v-for="(value, key) in lnarr"
                    :key="key"
                    class="d-inline-block float-left w-auto"
                    >
                        <span
                        v-if="translateLnArr.includes(value)"
                        >{{key}},</span>
                    </div>
                </div>
                <h3>言語を選ぶ</h3>
                <div
                v-for="(value, key) in lnarr"
                :key="key"
                class="translate-language-area d-inline-block float-left w-auto"
                >
                    <input
                    v-if="!translateLnArr.includes(value)"
                    type="checkbox" :id="value" :value="value"
                    v-model="translateLnArr">
                    <input
                    v-else
                    type="checkbox" :id="value" :value="value"
                    v-model="translateLnArr"
                    checked
                    >
                    <label :for="value">{{key}}</label>
                </div>
                <div class="submitButtonInner pt1rem pb1rem">
                    <button
                    class="translationButton button_blue"
                    @click="checkall"
                    >全てにチェックを入れる</button>
                    <button
                    class="translationButton button_blue"
                    @click="unCheckall"
                    >全てのチェックを外す</button>
                    <button
                    class="translationButton button_blue"
                    @click="checkTranslateSuccess"
                    >翻訳できてない箇所のみ</button>
                </div>
                <div class="submitButtonInner">
                    <button
                    class="translationButton button_pink"
                    @click="translateJsonData('ChatGpt')"
                    >ChatGPT</button>
                    <button
                    class="translationButton button_navy"
                    @click="translateJsonData('GoogleAPI')"
                    >Google Translate</button>
                </div>
            </div>
        </div>
    </div>
</template>

<script lang="ts">
import { Vue } from "vue-class-component";
import {store} from '../store/common/index';
import { PATH, lnarr, fullLinArr } from '../module/prop';
import { GenericObject } from '../module/type';
import { API } from '../module/function';

export default class categoryList extends Vue {
    path: PATH = new PATH();
    trashicon = this.path.trashicon;
    categoryName = '';
    categoryDescription = '';
    categoryOgImgPath = '';
    catdir = '';
    catinfo: GenericObject = {}
    lnarr: GenericObject = lnarr;
    fullLinArr: GenericObject = fullLinArr;
    translateLnArr: string[] = [];
    currentPath = '';

    created () {
        this.setCatData();
        this.readData();
        this.checkTranslateSuccess();
        this.currentPath = this.$route.path;
    }
    setCatData() {
        this.catdir = `${process.env.VUE_APP_listupPath}${this.$route.path}/index.json`;
    }
    readData() {
        API.post (
            `${store.state.pageinfo.base_url}${process.env.VUE_APP_categoryDirectory}`,
            {filePath: this.catdir},
            (response: GenericObject) => {
                this.catinfo = response.data;
            }
        );
    }
    addCategory () {
        if (!this.categoryName || !this.categoryDescription || !this.categoryOgImgPath) {
            return;
        }

        let newKey: number;
        if (Object.keys(this.catinfo).length === 0) {
            newKey = 1;
        } else {
            const keys = Object.keys(this.catinfo).map(key => parseInt(key, 10));
            newKey = Math.max(...keys) + 1;
        }

        let today = this.getCurrentDateFormatted();
        this.catinfo[newKey] = {
            "category": this.categoryName,
            "catlist": [],
            "created_at": today,
            "created_at_for_sitemap": today,
            "description": this.categoryDescription,
            "ogImg": this.categoryOgImgPath,
            "updated_at": today,
            "updated_at_for_sitemap": today
        };

        API.post (
            `${store.state.pageinfo.base_url}${process.env.VUE_APP_categoryAddDirectory}`,
            {filePath: this.catdir, newData: this.catinfo},
            (response: GenericObject) => {
                console.log(response);
            }
        );
    }

    editCatInfo(property: string, value: string) {
      (this as any)[property] = value;
    }

    deleteData (val: string) {
        API.post (
            `${store.state.pageinfo.base_url}${process.env.VUE_APP_categoryDeleteDirectory}`,
            {filePath: this.catdir, deleteNum: val},
            (response: GenericObject) => {
                this.catinfo = response.data;
            }
        );
    }

    translateJsonData (whichlng: string) {
        //ChatGpt,GoogleAPI
        const checkedElements = this.$el.querySelectorAll('.translate-language-area input[type="checkbox"]:checked');
        this.translateLnArr = Array.from(checkedElements).map(el => (el as HTMLInputElement).value);
        API.post (
            `${store.state.pageinfo.base_url}${process.env.VUE_APP_fileTranslateEndpoint}`,
            {
                filePath: `${process.env.VUE_APP_listupPath}${this.$route.path}/index.json`,
                translateLanguageArr: this.translateLnArr,
                whichlng: whichlng
            },
            (response: GenericObject) => {
                console.log(response.data);
            }
        );
    }
    checkTranslateSuccess () {
        this.translateLnArr = [];
        API.post(
            `${store.state.pageinfo.base_url}${process.env.VUE_APP_checkFailTranslate}`,
            { directory: process.env.VUE_APP_categoryDirPath},
            (response: GenericObject) => {
                for (let key in this.lnarr) {
                    if (!response.data.data.includes(this.lnarr[key])) {
                        this.translateLnArr.push(this.lnarr[key]);
                    }
                }
            }
        );
    }
    checkall () {
        this.translateLnArr = [];
        API.post(
            `${store.state.pageinfo.base_url}${process.env.VUE_APP_checkFailTranslate}`,
            { directory: process.env.VUE_APP_categoryDirPath},
            (response: GenericObject) => {
                for (let key in this.lnarr) {
                    this.translateLnArr.push(this.lnarr[key]);
                }
            }
        );
    }
    unCheckall () {
        this.translateLnArr = [];
    }
    private getCurrentDateFormatted (): string {
        const today = new Date();
        
        const year = today.getFullYear();
        const month = String(today.getMonth() + 1).padStart(2, '0');
        const day = String(today.getDate()).padStart(2, '0');
        
        return `${year}-${month}-${day}`;
    }
}
</script>

<style lang="scss" scoped>
</style>