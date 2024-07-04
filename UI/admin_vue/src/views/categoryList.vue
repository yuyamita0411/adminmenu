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
            <div class="flex-container mt2rem font1rem">
                <button type="button" @click="addCategory" class="submitButton button_blue font1rem">カテゴリを追加する</button>
                <button type="button" class="submitButton button_blue font1rem">ChatGPTで翻訳する</button>
            </div>
        </div>
    </div>
</template>

<script lang="ts">
import { Vue } from "vue-class-component";
import {store} from '../store/common/index';
import { PATH } from '../module/prop';
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
    currentPath = '';

    created () {
        this.setCatData();
        this.readData();
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
                console.log(this.catinfo);
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
                console.log(response.data);
                this.catinfo = response.data;
            }
        );
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