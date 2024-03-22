import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import {store} from './store/common/index';

createApp(App).use(store).use(router).mount('#app')

router.afterEach(() => {
    store.commit('setJsonData', {});
});