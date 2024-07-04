import { createStore } from 'vuex';
import { StoreState, GenericObject, updateVariableStatePayload } from '../../module/type';

export const store = createStore<StoreState>({
    state: {
        jsondata: {},
        pageinfo: {},
        categoryinfo: {},
        EditingTargetIndex: {},
        modalStatus: {},
        HoverTargetIndex: {},
        nexttagNum: 0,
        isLoading: false,
        targetTagInfo: {order: 0, setTargetTagNow: '', setTargetTagDetail: ''},
    },
    mutations: {
        updateStoreObj(state, payload: GenericObject) {
            const { key, value, target } = payload;
            if (target === 'pagedirList' && Array.isArray(state[target])) {
                state[target][key] = value;
            } else if (typeof state[target] === 'object') {
                state[target][key] = value;
            } else {
                console.warn(`Target ${target} is not a valid state property`);
            }
        },
        updateVariableState(state, payload: updateVariableStatePayload) {
            const { key, value } = payload;
            if (key in state) {
                state[key] = value;
            }
        },
        setJsonData(state, data: GenericObject) {
            state.jsondata = data;
        },
        setCategoryData(state, data: GenericObject) {
            state.categoryinfo = data;
        },
        changeJsonData(state, payload: { key: string; value: string }) {
            state.jsondata[payload.key] = payload.value;
        }
    }
});
