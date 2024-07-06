<template>
    <div class="content-wrapper">
        <h2>共通項目詳細</h2>
        <table class="list-chart w-100">
            <thead>
                <tr>
                    <th class="p05rem">項目</th>
                    <th class="p05rem">値</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="(value, key) in catinfo" :key="key">
                    <td class="p05rem">{{ key }}</td>
                    <td class="p05rem"
                    v-if="typeof value == 'string'">
                        <input v-model="catinfo[key]" @input="updateCat(key, $event.target.value)" class="w-100 lh2rem font1rem"/>
                    </td>
                    <td class="p05rem"
                    v-else>
                        <table>
                            <tr
                            v-for="(value2, key2) in value" :key="key2"
                            >
                                <td>{{ key2 }}</td>
                                <td>
                                    <input
                                    v-model="catinfo[key][key2]" @input="updateCatsCat(key2, $event.target.value)"
                                    class="w-100 lh2rem font1rem"/>
                                </td>
                            </tr>
                        </table>
                    </td>
                </tr>
            </tbody>
        </table>
        <div class="flex-container mt2rem font1rem">
            <button @click="goBack" class="menu-list-button menuicon submitButton button_blue font1rem">戻る</button>
            <button type="button" @click="rebaseCategory" class="submitButton button_blue font1rem">更新する</button>
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
</template>

<script lang="ts">
import { Vue } from "vue-class-component";
import { store } from '../store/common/index';
import { GenericObject } from '../module/type';
import { API } from '../module/function';
import { lnarr, fullLinArr } from '../module/prop';

export default class commonInfo extends Vue {
    categoryName = '';
    categoryDescription = '';
    categoryOgImgPath = '';
    catinfo: GenericObject = {};
    lnarr: GenericObject = lnarr;
    fullLinArr: GenericObject = fullLinArr;
    translateLnArr: string[] = [];
    catdir = '';

    created() {
        this.setCatData();
        this.readData();
        this.checkTranslateSuccess();
    }

    setCatData() {
        this.catdir = `${process.env.VUE_APP_listupPath}${this.$route.path}/index.json`;
    }

    readData() {
        API.post(
            `${store.state.pageinfo.base_url}${process.env.VUE_APP_categoryDetailDirectory}`,
            { filePath: this.catdir},
            (response: GenericObject) => {
                let rawdata = JSON.parse(response.data.data);
                this.catinfo = rawdata;
            }
        );
    }

    updateCat(key: string, newValue: string) {
        this.catinfo[key] = newValue;
    }
    updateCatsCat(key: string, key2: string, newValue: string) {
        this.catinfo[key][key2] = newValue;
    }

    rebaseCategory() {
        API.post(
            `${store.state.pageinfo.base_url}${process.env.VUE_APP_categoryDetailRebaseDirectory}`,
            { filePath: this.catdir, rebaseData: this.catinfo },
            (response: GenericObject) => {
                console.log(response);
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
                fileData: store.state.jsondata,
                filePath: `${process.env.VUE_APP_commonDirPath}/${this.$route.params.country}/index.json`,
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
            { directory: process.env.VUE_APP_commonDirPath},
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
            { directory: process.env.VUE_APP_commonDirPath},
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

    goBack() {
        this.$router.go(-1);
    }
}
</script>

<style lang="scss" scoped>
</style>
