<template>
    <div class="content-wrapper">
        <div
        v-for="(value, key, index) in jsondata"
        :key="key"
        >
        <AddTaskModal v-if="showChild" @ReRender="toggle"></AddTaskModal>
            <div
            v-if="tag.getElementTag(key)"
            class="editelem">
                <div
                :class="getPaddingClass(key, index)"
                >
                    <span
                        :index="index"
                        :data-itemkey="key"
                        :class="tag.getElementTagLabel(key)"
                        v-if="!EditingTargetIndex[index]"
                        @click="clickTagButton($event, key)"
                        style="min-height:1.5rem;"
                        v-html="displayArticleHTML(key, value)"
                    >
                    </span>
                    <textarea
                        v-else
                        :class="tag.getElementTagLabel(key)"
                        :value="inputValues[key]"
                        :style="textareaStyle"
                        @input="handleInput($event, key)"
                    >
                    </textarea>
                </div>
                <div
                    @mouseover="mouseOverButton"
                    @mousemove="mouseOverButton"
                    @mouseout="mouseOutButton"
                    :index="index"
                    class="addcontent-wrapper position-absolute"
                >
                    <button
                    @click="addBlockFunc"
                    class="addcontentbutton position-absolute"
                    ><img
                    :index="index"
                    @mouseover="mouseOverButton"
                    @mousemove="mouseOverButton"
                    @mouseout="mouseOutButton"
                    :style="addButtonStyle(index)"
                    :src="addcontenticon"
                    :data-plusnum="index+1"></button>
                    <span class="addcontent-border bottom-border"></span>
                </div>
                <button
                v-if="key != 'pagetitle'"
                class="trashbutton position-absolute">
                    <img
                    :src="trashicon"
                    @click="deleteElement(key)"
                    >
                </button>
            </div>
        </div>
        <div class="meta-setting-area">
            <div v-for="field in fields" :key="field.id" class="meta-label-wrapper">
                <div class="font-weight-bold">{{ field.label }}</div>
                <textarea
                :class="tag.getTagLabel(field.id)"
                @input="genericInput($event, field.id)"
                :value="jsondata[field.id]"
                ></textarea>
            </div>
        </div>
        <div class="submitButtonWrapper">
            <div class="submitButtonInner">
                <button
                class="submitButton"
                @click="updateJsonData"
                >更新する</button>
                <button
                class="translationButton"
                @click="translateJsonData"
                >翻訳する</button>
            </div>
        </div>
    </div>
</template>

<script lang="ts">
import { Vue, Options } from "vue-class-component";
import { mapState } from 'vuex';

import {store} from '../store/common/index';
import { PATH, TAG } from '../module/prop';
import { API } from '../module/function';
import { Menu } from '../module/editMenu/index';
import { GenericObject } from '../module/type';

@Options({
    computed: {
        ...mapState(['modalStatus', 'jsondata', 'HoverTargetIndex', 'EditingTargetIndex', 'isLoading']),
        EditingTargetIndex() {
            return store.state.EditingTargetIndex;
        },
        HoverTargetIndex() {
            return store.state.HoverTargetIndex;
        },
        isLoading() {
            return store.state.isLoading;
        }
    }
})
export default class editMenu extends Vue {
    path: PATH = new PATH();
    tag: TAG = new TAG();
    menu: Menu = new Menu();

    textareaStyle!: string;
    inputValues: {
        [key: string]: GenericObject;
    } = {};
    fields = this.menu.fields;
    displayTrash = 'hide-trash';
    addcontenticon = this.path.addcontenticon;
    trashicon = this.path.trashicon;
    touchtag: GenericObject = {};

    created () {
        //初期のデータを定義
        this.readData();
        //編集中のタグ情報の状態を初期化
        this.resetObj(store.state.jsondata, 'updateStoreObj', 'EditingTargetIndex');
        this.inputValues = store.state.jsondata;
    }
    readData() {
        API.post (
            `${store.state.pageinfo.base_url}${process.env.VUE_APP_fileReadEndpoint}`,
            {filePath: `${process.env.VUE_APP_articleDirPath}${this.$route.path}/index.json`},
            (response: GenericObject) => {
                store.commit('setJsonData', response.data);
            }
        );
    }
    updateJsonData () {
        this.ModifyJsonFile (
            `${store.state.pageinfo.base_url}${process.env.VUE_APP_fileEndpoint}`,
            `${process.env.VUE_APP_articleDirPath}${this.$route.path}/index.json`
        );
        this.ModifyJsonFile (
            `${store.state.pageinfo.base_url}${process.env.VUE_APP_UpdateDirContentEndpoint}`,
            "dummy"
        );
    }
    translateJsonData () {
        this.ModifyJsonFile (
            `${store.state.pageinfo.base_url}${process.env.VUE_APP_fileTranslateEndpoint}`,
            `${process.env.VUE_APP_articleDirPath}${this.$route.path}/index.json`
        );
    }
    private clickTagButton (e: Event, key: string) {//今クリックしたタグの情報を更新する。状態管理はupdateTargetTagInfoが実行されtargetTagInfoが更新される。
        const target = e.target as HTMLElement
        //編集中のタグ情報の状態を更新
        this.resetObj(store.state.jsondata, 'updateStoreObj', 'EditingTargetIndex');
        store.commit('updateStoreObj', { target: 'EditingTargetIndex', key: Number(target.getAttribute('index')), value: true });
        store.dispatch('TargetIndexProperty');
        this.inputValues = store.state.jsondata;
        this.touchtag = this.isImgTag(this.tag.getElementTagLabel(key));
        //テキストエリアの高さを合わせる
        this.setTagHeight(target);
    }
    private handleInput (e: Event, key: string) {
        const target = e.target as HTMLTextAreaElement;
        this.setInputHeight(target);
        store.state.jsondata[key] = target.value;
        store.commit('setJsonData', store.state.jsondata);
    }
    private genericInput(e: Event, key: string) {
        const target = e.target as HTMLTextAreaElement;
        store.commit('changeJsonData', { key, value: target.value });
    }
    private addBlockFunc (e: MouseEvent) {
        const target = e.target as HTMLElement
        store.commit('updateStoreObj', { target: 'modalStatus', key: 'modalClassName', value: 'modal-show' });
        store.commit('updateStoreObj', { target: 'modalStatus', key: 'modalWrapperClassName', value: 'modal-wrapper-show' });
        store.commit('updateStoreObj', { target: 'modalStatus', key: 'bottom', value: `calc(100vh - 5rem - ${e.clientY}px)` });
        store.commit('updateVariableState', { key: 'nexttagNum', value: target.dataset.plusnum });
    }
    private mouseOverButton (e: Event) {
        const target = e.target as HTMLTextAreaElement;
        this.resetObj(store.state.HoverTargetIndex, 'updateStoreObj', 'HoverTargetIndex');
        store.commit('updateStoreObj', { target: 'HoverTargetIndex', key: Number(target.getAttribute('index')), value: true });
        store.dispatch('TargetIndexProperty');
    }
    private mouseOutButton () {
        this.resetObj(store.state.HoverTargetIndex, 'updateStoreObj', 'HoverTargetIndex');
        store.dispatch('TargetIndexProperty');
    }
    private resetObj (jsondata:GenericObject, commit: string, target: string) {
        Object.keys(jsondata).forEach((obj: string, i: number) => {
            store.commit(commit, { target: target, key: i, value: false });
        });
    }
    private TargetIndexProperty() {
      return store.state.EditingTargetIndex
    }
    private HoverIndexProperty() {
      return store.state.HoverTargetIndex
    }
    private deleteElement(key: string) {
        delete store.state.jsondata[key];
        store.commit('setJsonData', store.state.jsondata);
    }
    private isLoading() {
      return store.state.isLoading
    }
    private ModifyJsonFile (endpoint: string, filepath: string) {
        store.dispatch('isLoading');
        API.post (
            endpoint,
            {
                fileData: store.state.jsondata,
                filePath: filepath
            },
            (response: GenericObject) => {
                console.log(response.data);
            }
        );
    }

    /***** html *****/
    private setTagHeight (target: HTMLElement) {
        this.textareaStyle = '';
        if (!this.touchtag["isimg"]) {
            this.textareaStyle = `height: ${target.offsetHeight}px; margin-bottom: 0;`;
        }
    }
    private setInputHeight (target: HTMLElement) {
        target.style.height = 'auto';
        if (!this.touchtag["isimg"]) {
            target.style.height = `${target.scrollHeight}px`;
        }
    }
    private addButtonStyle (index: number) {
        if (store.state.HoverTargetIndex[index]) {
            return 'opacity:1; transition: all .5s;';
        }
        return 'opacity:0; transition: all .5s;';
    }
    private getPaddingClass(key: string, index: number) {
        let classname = "";
        const entries = Object.entries(store.state.jsondata);
        if (0 < index) {
            if (this.tag.getElementTagLabel(key) === 'for-p') {
                classname = `p-${this.tag.getElementTagLabel( entries[index - 1][0])}`
            } else {
                classname = `div-${this.tag.getElementTagLabel(key)}`;
            }
        }
        return classname;
    }
    private isImgTag (tagname: string) {
        let wclass = this.tag.tagjson[tagname] ? this.tag.tagjson[tagname] : '';
        let isimg = this.tag.tagjson[tagname] ? true : false;
        return {"isimg": isimg, "wclass": wclass}
    }
    private displayArticleHTML (key: string, value: string) {
        let prop = this.isImgTag(this.tag.getElementTagLabel(key));
        return !prop["isimg"] ? value : `<img src='${process.env.VUE_APP_website_path}${value}' class='${prop["wclass"]}'>`;
    }
}
</script>
<style lang="scss" scoped>
.content-wrapper {
    .editelem {
        width: 100%;
        float: left;
        margin: 1rem .5rem;
        position: relative;
        div {
            width: 98%;
            textarea {
                border: none;
                background: rgb(0, 0, 0, 0.05);
            }
        }
        div:not(.addcontent-wrapper) {
            margin: 0 auto;
            float: left;
            width: 100%;
            position: relative;
        }
    }
    .editelem > * {
        cursor: pointer;
    }
}
.meta-label-wrapper {
    textarea {
        font-size: 1rem;
        padding: .5rem 0 0 .5rem;
        width: 100%;
    }
}
.meta-setting-area {
    margin: 1rem auto;
    padding: 0 .5rem;
    .meta-label-wrapper {
        margin-bottom: 1rem;
    }
}
.meta-setting-area .meta-label-wrapper,
.meta-setting-area {
    display: inline-block;
    width: 100%;
}

h2,
.for-h2 {
    font-size: 1.5rem;
    margin: 0 0 .5rem 0;
}

h3,
.for-h3,
.for-box-h3 {
    font-size: 1.17rem;
    margin: 0 0 .5rem 0;
}

h4,
.for-h4 {
    font-size: 1.05rem;
    margin: 0 0 .5rem 0;
}

p,
.for-p,
.for-box-description {
    font-size: 1rem;
    margin: 0 0 .5rem 0;
}

.p-for-h2 {
    padding-left: 1rem;
}
.div-for-h3 {
    padding-left: 1rem;
}
.p-for-h3 {
    padding-left: 2rem;
}
.div-for-h4 {
    padding-left: 2rem;
}
.p-for-h4 {
    padding-left: 3rem;
}
.div-for-h5 {
    padding-left: 3rem;
}
.p-for-h5 {
    padding-left: 4rem;
}
.div-for-h6 {
    padding-left: 4rem;
}
.p-for-h6 {
    padding-left: 5rem;
}

.submitButton,
.translationButton {
    font-size: 1rem;
}
.display-addbutton,
.display-trash {
    opacity: 1;
}
.hide-addbutton,
.hide-trash {
    opacity: 0;
}
.display-addbutton,
.hide-addbutton,
.display-trash,
.hide-trash {
    transition: all .3s;
}
.addcontentbutton,
.addcontentbutton img {
    cursor: pointer;
}
.submitButtonWrapper {
    width: 100%;
    margin-bottom: 3rem;
    text-align: center;
    display: inline-block;
}
.submitButtonInner {
    display: flex;
    gap: 3px;
    max-width: 15rem;
    width: 50%;
    margin: 0 auto;
}
.submitButton {
    border-bottom: 7px solid #0686b2;
    background: #27acd9;
    color: #fff;
}
.translationButton {
    border-bottom: 7px solid #C50B4F;
    background: #f54785;
    color: #fff;
}
.submitButton,
.translationButton {
    display: block;
    flex:1;
    cursor: pointer;
    text-align: center;
    vertical-align: middle;
    text-decoration: none;
    padding: 1rem 0rem;
    font-weight: bold;
    border-radius: 0.3rem;
    border: none;
    transition: all .3s;
}
.submitButton:hover,
.translationButton:hover {
    margin-top: 6px;
	color: #fff;
    transition: all .3s;
}
.submitButton:hover{
    border-bottom: 1px solid #0686b2;
}
.translationButton:hover {
	border-bottom: 1px solid #C50B4F;
}
.trashbutton {
    right: 2rem;
}
</style>