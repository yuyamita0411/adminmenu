<template>
    <div :class="`modal-wrapper ${modalStatus['modalWrapperClassName']}`" @click="modalClose">
        <button :class="`modal-close-button`" @click="modalClose"><img :src="closeButtonsrc"></button>
    </div>
    <div :class="`modal ${modalStatus['modalClassName']}`" :style="{bottom: modalStatus['bottom']}">
        <p :class="`modalmenu`" :data-itemkey="prop.tProp.h2.matchpattern" @click="clickTagButton">h2</p>
        <p :class="`modalmenu`" :data-itemkey="prop.tProp.h3.matchpattern" @click="clickTagButton">h3</p>
        <p :class="`modalmenu`" :data-itemkey="prop.tProp.h4.matchpattern" @click="clickTagButton">h4</p>
        <p :class="`modalmenu`" :data-itemkey="prop.tProp.h5.matchpattern" @click="clickTagButton">h5</p>
        <p :class="`modalmenu`" :data-itemkey="prop.tProp.h6.matchpattern" @click="clickTagButton">h6</p>
        <p :class="`modalmenu`" :data-itemkey="prop.tProp.p.matchpattern" @click="clickTagButton">p</p>
        <!--p :class="`modalmenu`" :data-itemkey="prop.tProp.boxmenu.matchpattern" @click="clickTagButton">box menu</p-->
    </div>
</template>

<script lang="ts">
import { Vue } from 'vue-class-component';
import { Options } from 'vue-class-component';

import {store} from '../store/common/index';
import { mapState } from 'vuex';

import { PROP } from '../module/prop';
import { FUNCTION } from '../module/function';

@Options({
    computed: {
        ...mapState(['modalStatus', 'jsondata'])
    }
})

export default class Modal extends Vue {
    prop: PROP = new PROP();
    func: FUNCTION = new FUNCTION();
    closeButtonsrc = this.prop.closebutton;

    created () {
        this.modalClose();
    }
    clickTagButton (e: Event) {
        this.modalClose();
        this.chooseWhichTag(e);
    }
    modalClose () {
        store.commit('updateStoreObj', { target: 'modalStatus', key: 'modalClassName', value: 'modal-hide' });
        store.commit('updateStoreObj', { target: 'modalStatus', key: 'modalWrapperClassName', value: 'modal-wrapper-hide' });
        store.commit('updateStoreObj', { target: 'modalStatus', key: 'bottom', value: '-4rem' });
    }
    chooseWhichTag(e: Event) {
        const target = e.target as HTMLElement;
        if (!target.dataset.itemkey) {
            return;
        }
        console.log(store.state.jsondata);
        console.log(store.state.nexttagNum);
        store.commit(
            'setJsonData',
            this.func.addNewObjectVal (
                store.state.jsondata,
                store.state.nexttagNum,
                target.dataset.itemkey
            )
        );
    }

}
</script>

<style lang="scss" scoped>
.modal-wrapper {
    position: fixed;
    background:#ffff;
    left: 0;
    top: 0;
    opacity: 0;
    width:100%;
    height: 100vh;
    display:inline-block;
    border-right: solid .4px;
    .modal-close-button {
        position: absolute;
        top: .3rem;
        right: .3rem;
        width: 1.5rem;
        height: 1.5rem;
        padding: 0;
        background: transparent;
        border: none;
        cursor:pointer;
        img {
            width: 100%;
        }
    }
}
.modal {
    display: flex;
    width: 50rem;
    left: calc((100% - 50rem) / 2);
    position: fixed;
    background: rgb(0, 0, 0, .5);
    padding: .5rem;
    .modalmenu {
        cursor: pointer;
        background: #ffff;
        font-size: 24px;
        padding:1rem 0 1rem 0;
        flex: 1;
        margin-bottom: 0;
        box-shadow: .1px .3px 2px rgba(0, 0, 0, 0.3);
    }
}
.modal-wrapper-hide {
    z-index: -1;
}
.modal-wrapper-show {
    z-index: 1;
}
.modal-show {
    z-index: 2;
    opacity: 1;
}
.modal-hide {
    opacity: 0;
    pointer-events:none;
}
.modal-show,
.modal-hide {
    transition: all .2s;
}
</style>