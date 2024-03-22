import { createStore } from 'vuex';
import { StoreState } from '../../module/type';

export const editMenuStore = createStore<StoreState>({
    state: {
    },
    mutations: {
        setTag(state, tag: string) {
            state.whichtag = tag;
        }
    }
});