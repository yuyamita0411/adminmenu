import { createStore } from 'vuex';
import { StoreState } from '../../module/type';

export const articleListStore = createStore<StoreState>({
    state: {
        pagedirList:[]
    },
    mutations: {
        updatePagedirList(state, payload: { key: string; value: string }) {
            state.pagedirList[payload.key] = payload.value;
        }
    }
});
