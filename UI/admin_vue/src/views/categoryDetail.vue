<template>
    <div class="content-wrapper">
        <h2>カテゴリ詳細</h2>
        <table>
            <thead>
                <tr>
                    <th>項目</th>
                    <th>値</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="(value, key) in catinfo" :key="key">
                    <td>{{ key }}</td>
                    <td>
                        <input v-model="catinfo[key]" @input="updateCat(key, $event.target.value)" />
                    </td>
                </tr>
            </tbody>
        </table>
        <div>
            <button type="button" @click="rebaseCategory">更新する</button>
        </div>
            <button @click="goBack" class="menu-list-button menuicon">戻る</button>
        <div>
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
            { filePath: this.catdir, cat_id: this.catnum },
            (response: GenericObject) => {
                let rawdata = JSON.parse(response.data.data);
                this.catinfo = rawdata[response.data.cat_id];
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
