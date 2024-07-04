<template>
    <div class="content-wrapper">
        <h2>カテゴリ詳細</h2>
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
                    <td class="p05rem">
                        <input v-model="catinfo[key]" @input="updateCat(key, $event.target.value)" class="w-100 lh2rem font1rem"/>
                    </td>
                </tr>
            </tbody>
        </table>
        <div class="flex-container mt2rem font1rem">
            <button @click="goBack" class="menu-list-button menuicon submitButton font1rem">戻る</button>
            <button type="button" @click="rebaseCategory" class="submitButton font1rem">更新する</button>
        </div>
    </div>
</template>

<script lang="ts">
import { Vue } from "vue-class-component";
import { store } from '../store/common/index';
import { GenericObject } from '../module/type';
import { API } from '../module/function';

export default class categoryDetail extends Vue {
    categoryName = '';
    categoryDescription = '';
    categoryOgImgPath = '';
    catinfo: GenericObject = {};
    catdir = '';
    catnum: any = 0;

    created() {
        this.setCatData();
        this.readData();
    }

    setCatData() {
        let parts = this.$route.path.split('/');
        this.catnum = parts.length > 0 ? parts[parts.length - 1] : null;
        this.catdir = `${process.env.VUE_APP_listupPath}/${parts[1]}/${parts[2]}/index.json`;
    }

    readData() {
        API.post(
            `${store.state.pageinfo.base_url}${process.env.VUE_APP_categoryDetailDirectory}`,
            { filePath: this.catdir},
            (response: GenericObject) => {
                let rawdata = JSON.parse(response.data.data);
                this.catinfo = rawdata[this.catnum];
            }
        );
    }

    updateCat(key: string, newValue: string) {
        this.catinfo[key] = newValue;
    }

    rebaseCategory() {
        API.post(
            `${store.state.pageinfo.base_url}${process.env.VUE_APP_categoryDetailRebaseDirectory}`,
            { filePath: this.catdir, cat_id: this.catnum, rebaseData: this.catinfo },
            (response: GenericObject) => {
                console.log(response);
            }
        );
    }

    goBack() {
        this.$router.go(-1);
    }
}
</script>

<style lang="scss" scoped>
</style>
