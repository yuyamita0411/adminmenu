<template>
    <div class="edit-wrapper">
        <div
        v-for="(value, key, index) in jsondata"
        :key="key"
        >
            <div
            v-if="prop.getElementTag(key)"
            class="editelem">
                <div
                >
                    <span
                        :index="index"
                        :data-itemkey="key"
                        :class="`for-${prop.getElementTag(key)}`"
                        v-if="!EditingTargetIndex[index]"
                        @click="clickTagButton"
                        style="min-height:1.5rem;"
                    >
                        {{ value }}
                    </span>
                    <textarea
                        v-else
                        :class="`for-${prop.getElementTag(key)}`"
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
                    :class="`addcontent-wrapper`"
                >
                    <button
                    @click="addBlockFunc"
                    :class="`addcontentbutton`"
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
                :class="`trashbutton`">
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
                :class="`for-${field.id}`"
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

import {store} from '../store/index';
import { PROP } from '../module/prop';
import { FUNCTION } from '../module/function';
import { GenericObject } from '../module/type';

@Options({
    computed: {
        ...mapState(['modaldisplaystatus', 'modalStatus', 'whichtag', 'jsondata']),
        EditingTargetIndex() {
            // Vuex ストアの state から EditingTargetIndex を取得してコンポーネントにマッピング
            return store.state.EditingTargetIndex;
        },
        HoverTargetIndex() {
            // Vuex ストアの state から HoverTargetIndex を取得してコンポーネントにマッピング
            return store.state.HoverTargetIndex;
        }
    }
})
export default class editMenu extends Vue {
    prop = new PROP();
    func = new FUNCTION();

    textareaStyle!: string;
    inputValues: {
        [key: string]: GenericObject;
    } = {};
    fields = [
        { id: 'pagetitle', label: 'タイトル' },
        { id: 'description', label: 'ディスクリプション' },
        { id: 'categoryID', label: 'categoryID' },
        { id: 'thumbnail', label: 'thumbnail' },
        { id: 'ogImg', label: 'ogImg' },
        { id: 'created_at', label: '投稿日' },
        { id: 'updated_at', label: '更新日' },
    ];
    displayTrash = 'hide-trash';
    addcontenticon = this.prop.addcontenticon;
    trashicon = this.prop.trashicon;

    created () {
        //初期のデータを定義
        this.readData();
        //編集中のタグ情報の状態を初期化
        this.resetObj(store.state.jsondata, 'updateStoreObj', 'EditingTargetIndex');
        this.inputValues = store.state.jsondata;
    }
    private clickTagButton (e: Event) {//今クリックしたタグの情報を更新する。状態管理はupdateTargetTagInfoが実行されtargetTagInfoが更新される。
        const target = e.target as HTMLElement
        //編集中のタグ情報の状態を更新
        this.resetObj(store.state.jsondata, 'updateStoreObj', 'EditingTargetIndex');
        store.commit('updateStoreObj', { target: 'EditingTargetIndex', key: Number(target.getAttribute('index')), value: true });
        store.dispatch('TargetIndexProperty');
        this.inputValues = store.state.jsondata;
        //テキストエリアの高さを合わせる
        this.setTagHeight(target);
    }
    private handleInput (e: Event, key: string) {
        const target = e.target as HTMLTextAreaElement;
        target.style.height = 'auto';
        target.style.height = `${target.scrollHeight}px`;
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
    private setTagHeight (target: HTMLElement) {
        this.textareaStyle = `height: ${target.offsetHeight}px; margin-bottom: 0;`;
    }
    private addButtonStyle (index: number) {
        if (store.state.HoverTargetIndex[index]) {
            return 'opacity:1; transition: all .5s;';
        }
        return 'opacity:0; transition: all .5s;';
    }
    private deleteElement(key: string) {
        delete store.state.jsondata[key];
        console.log(store.state.jsondata);
        store.commit('setJsonData', store.state.jsondata);
    }
    readData() {
        this.func.postAPI (
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
    }
    translateJsonData () {
        this.ModifyJsonFile (
            `${store.state.pageinfo.base_url}${process.env.VUE_APP_fileTranslateEndpoint}`,
            `${process.env.VUE_APP_articleDirPath}${this.$route.path}/index.json`
        );
    }
    private ModifyJsonFile (endpoint: string, filepath: string) {
        this.func.postAPI (
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
}
</script>

<style lang="scss" scoped>
.edit-wrapper {
    max-width: 50rem;
    padding-top: 4rem;
    min-height: 100vh;
    margin: 0 auto;
    background: #ffff;
    .editelem {
        width: 100%;
        float: left;
        margin: 1rem .5rem;
        position: relative;
        div {
            width: 98%;
        }
        div:not(.addcontent-wrapper) {
            margin: 0 auto;
            float: left;
            width: 100%;
            position: relative;
        }
        .addcontent-wrapper {
            position: absolute;
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
</style>