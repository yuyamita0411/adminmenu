import { createStore } from 'vuex';
import { StoreState, UpdateStatePayload, GenericObject } from '../module/type';

export const store = createStore<StoreState>({
    state: {
        pageinfo: {},
        modaldisplaystatus: 'modal-hide',
        targetTagInfo: {order: 0, setTargetTagNow: '', setTargetTagDetail: ''},
        modalStatus: {},
        EditingTargetIndex: {},
        HoverTargetIndex: {},
        targetTagNow: "",
        targetTagDetail: "",
        addtag: "",
        nexttagNum: 0,
        pagedirList:[],
 
        whichtag: "",
        additemkey: "",
        jsondata: {}
    },
    mutations: {
        setPageInfo(state, payload: { key: number; value: string }) {
            state.pageinfo[payload.key] = payload.value;
        },
        changeModalStatus(state, payload: { key: number; value: string }) {
            state.modalStatus[payload.key] = payload.value;
        },
        updateEditingTargetIndex(state, payload: { key: number; value: boolean }) {
            state.EditingTargetIndex[payload.key] = payload.value;
        },
        updateHoverTargetIndex(state, payload: { key: number; value: boolean }) {
            state.HoverTargetIndex[payload.key] = payload.value;
        },
        updatePagedirList(state, payload: { key: string; value: string }) {
            state.pagedirList[payload.key] = payload.value;
        },
        updateState(state, payload: UpdateStatePayload) {
            const { key, value } = payload;
            if (key in state) {
                state[key] = value;
            }
        },
        updateStore(state, payload: GenericObject) {
            const { key, value, target } = payload;
            if (target === 'pagedirList' && Array.isArray(state[target])) {
                state[target][key] = value;
            } else if (typeof state[target] === 'object') {
                state[target][key] = value;
            } else {
                console.warn(`Target ${target} is not a valid state property`);
            }
        },
        setJsonData(state, data: GenericObject) {
            state.jsondata = data;
        },
        changeJsonData(state, payload: { key: string; value: string }) {
            state.jsondata[payload.key] = payload.value;
        },
/*
        setTargetTagNow(state, tag: string) {
            state.targetTagNow = tag;
        },
        setTargetTagDetail(state, tag: string) {
            state.targetTagDetail = tag;
        },
*/
        setTag(state, tag: string) {
            state.whichtag = tag;
        },
/*
        setItemKey(state, itemkey: string) {
            state.additemkey = itemkey;
        },
        addValJsonData (state, newVal: string): void {
            state.jsondata = {
                ...state.jsondata,
                [newVal]: ''
            };
        }
*/
    }
});
