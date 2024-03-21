import { GenericObject, APIFunc } from './type';
import axios from 'axios';

export class FUNCTION {
    postAPI (endpoint: string, params: GenericObject, func: APIFunc) {
        axios.post(endpoint,params)
        .then((response) => {
            func(response);
        })
        .catch((error) => {
            console.error(error);
        });
    }
    addNewObjectVal (jsondata: GenericObject, nexttagNum: number, itemkey: string) {
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
