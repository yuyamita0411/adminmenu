import {store} from '../store/common/index';
import { GenericObject, APIFunc } from './type';
import axios from 'axios';

export class API {
    static post (endpoint: string, params: GenericObject, func: APIFunc) {
        store.commit('updateVariableState', { key: 'isLoading', value: true });
        axios.post(endpoint,params)
        .then((response) => {
            func(response);
            store.commit('updateVariableState', { key: 'isLoading', value: false });
        })
        .catch((error) => {
            console.error(error);
        });
    }
}

export class JSON {
    static addNewObjectVal (jsondata: GenericObject, nexttagNum: number, itemkey: string) {
        const keys = Object.keys(jsondata);
        if (!itemkey) {
            return;
        }
        // 新しいキーを指定された位置に挿入
        keys.splice(nexttagNum, 0, itemkey);
        const regex = new RegExp(itemkey + "\\d*$");

        // 新しいオブジェクトを構築
        const updated: GenericObject = {};
        let countReg = 0;
        keys.forEach((key, index) => {
            if (regex.test(key)) {
                countReg += 1;
                const newKey = `${itemkey}${countReg}`;
                if (index === nexttagNum+1) {
                    updated[newKey] = "";
                } else {
                    updated[newKey] = jsondata[key] || "";
                }
            }
            else {
                updated[key] = jsondata[key];
            }
        });
        return updated;
    }
}
