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
                <button :class="`trashbutton ${displayTrash}`"><img :src="trashicon"></button>
            </div>
        </div>

        <div class="meta-setting-area">
            <div class="meta-label">タイトル</div>
            <textarea
                class="for-pagetitle"
                @input="titleInput($event)"
                :value="pagetitle"
            >
            </textarea>
            <div class="meta-label">ディスクリプション</div>
            <textarea
                class="for-description"
                @input="descriptionInput($event)"
                :value="description"
            >
            </textarea>

            <div class="meta-label">categoryID</div>
            <textarea
                class="for-categoryID"
                @input="categoryIDInput($event)"
                :value="categoryID"
            >
            </textarea>
            <div class="meta-label">thumbnail</div>
            <textarea
                class="for-thumbnail"
                @input="thumbnailInput($event)"
                :value="thumbnail"
            >
            </textarea>
            <div class="meta-label">ogImg</div>
            <textarea
                class="for-ogImg"
                @input="ogImgInput($event)"
                :value="ogImg"
            >
            </textarea>
            <div class="meta-label">投稿日</div>
            <textarea
                class="for-created_at"
                @input="createdInput($event)"
                :value="created_at"
            >
            </textarea>
            <div class="meta-label">更新日</div>
            <textarea
                class="for-updated_at"
                @input="updatedInput($event)"
                :value="updated_at"
            >
            </textarea>
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
import axios from 'axios';

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

    pagetitle!: string
    description!: string
    categoryID!: string
    thumbnail!: string            
    ogImg!: string
    created_at!: string
    updated_at!: string

    displayTrash = 'hide-trash';

    addcontenticon = this.prop.addcontenticon;

    created () {
        //初期のデータを定義
        this.readData();
        //編集中のタグ情報の状態を初期化
        this.resetObj(store.state.jsondata, 'updateStore', 'EditingTargetIndex');
        this.inputValues = store.state.jsondata;
        console.log(this.inputValues);
        console.log(store.state.jsondata);
    }
    private clickTagButton (e: Event) {//今クリックしたタグの情報を更新する。状態管理はupdateTargetTagInfoが実行されtargetTagInfoが更新される。
        const target = e.target as HTMLElement

        //編集中のタグ情報の状態を更新
        this.resetObj(store.state.jsondata, 'updateStore', 'EditingTargetIndex');
        store.commit('updateEditingTargetIndex', { key: Number(target.getAttribute('index')), value: true });
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
    private titleInput(e: Event) {
        const target = e.target as HTMLTextAreaElement;
        this.pagetitle = target.value;
        store.commit('changeJsonData', { key: "pagetitle", value: target.value });
    }
    private descriptionInput(e: Event) {
        const target = e.target as HTMLTextAreaElement;
        this.description = target.value;
        store.commit('changeJsonData', { key: "description", value: target.value });
    }

    private updatedInput(e: Event) {
        const target = e.target as HTMLTextAreaElement;
        this.updated_at = target.value;
        store.commit('changeJsonData', { key: "updated_at", value: target.value });
    }
    private createdInput(e: Event) {
        const target = e.target as HTMLTextAreaElement;
        this.created_at = target.value;
        store.commit('changeJsonData', { key: "created_at", value: target.value });
    }
    private ogImgInput(e: Event) {
        const target = e.target as HTMLTextAreaElement;
        this.ogImg = target.value;
        store.commit('changeJsonData', { key: "ogImg", value: target.value });
    }
    private thumbnailInput(e: Event) {
        const target = e.target as HTMLTextAreaElement;
        this.thumbnail = target.value;
        store.commit('changeJsonData', { key: "thumbnail", value: target.value });
    }
    private categoryIDInput(e: Event) {
        const target = e.target as HTMLTextAreaElement;
        this.categoryID = target.value;
        store.commit('changeJsonData', { key: "categoryID", value: target.value });
    }


    private addBlockFunc (e: MouseEvent) {
        const target = e.target as HTMLElement
        store.commit('updateStore', { target: 'modalStatus', key: 'modalClassName', value: 'modal-show' });
        store.commit('updateStore', { target: 'modalStatus', key: 'modalWrapperClassName', value: 'modal-wrapper-show' });
        store.commit('updateStore', { target: 'modalStatus', key: 'bottom', value: `calc(100vh - 5rem - ${e.clientY}px)` });

        store.commit('updateState', { key: 'nexttagNum', value: target.dataset.plusnum });
    }
    private mouseOverButton (e: Event) {
        const target = e.target as HTMLTextAreaElement;
        this.resetObj(store.state.HoverTargetIndex, 'updateStore', 'HoverTargetIndex');
        store.commit('updateStore', { target: 'HoverTargetIndex', key: Number(target.getAttribute('index')), value: true });
        store.dispatch('TargetIndexProperty');
    }
    private mouseOutButton () {
        this.resetObj(store.state.HoverTargetIndex, 'updateStore', 'HoverTargetIndex');
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

    deleteElement(target: GenericObject, key: string) {
        delete target[key];
    }
    readData () {
        axios.post(`${store.state.pageinfo.base_url}${process.env.VUE_APP_fileReadEndpoint}`,
        {
            filePath: `${process.env.VUE_APP_articleDirPath}${this.$route.path}/index.json`
        }
        )
        .then((response: GenericObject) => {
            this.pagetitle = response.data["pagetitle"];
            this.description = response.data["description"];

            this.categoryID = response.data["categoryID"];
            this.thumbnail = response.data["thumbnail"];
            this.ogImg = response.data["ogImg"];
            this.created_at = response.data["created_at"];
            this.updated_at = response.data["updated_at"];
            store.commit('setJsonData', response.data);
        })
        .catch((error: GenericObject) => {
            console.error(error);
        });
    }
    updateJsonData () {
        //ここでAPIを叩いてjsonファイルを生成する
        axios.post(`${store.state.pageinfo.base_url}${process.env.VUE_APP_fileEndpoint}`,
        {
            fileData: store.state.jsondata,
            filePath: `${process.env.VUE_APP_articleDirPath}${this.$route.path}/index.json`
        }
        )
        .then((response: GenericObject) => {
            console.log(response.data);
        })
        .catch((error: GenericObject) => {
            console.error(error);
        });
    }
    translateJsonData () {
        axios.post(`${store.state.pageinfo.base_url}${process.env.VUE_APP_fileTranslateEndpoint}`,
        {
            fileData: store.state.jsondata,
            filePath: `${process.env.VUE_APP_articleDirPath}${this.$route.path}/index.json`
            //./translation_tool/language/detail/1/language/jp/index.json
        }
        )
        .then((response: GenericObject) => {
            console.log(response.data);
        })
        .catch((error: GenericObject) => {
            console.error(error);
        });
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

.meta-setting-area {
    margin: 1rem auto;
    padding: 0 .5rem;
}
.meta-setting-area .meta-label,
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
    border-bottom: 7px solid #0686b2;
    background: #27acd9;
    color: #fff;
    transition: all .3s;
}
.submitButton:hover,
.translationButton:hover {
	margin-top: 6px;
	border-bottom: 1px solid #0686b2;
	color: #fff;
    transition: all .3s;
}
</style>