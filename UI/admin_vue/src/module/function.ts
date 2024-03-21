import { GenericObject } from './type';

export class FUNCTION {
/*
    matchesPattern(str: string, prefix: string) {
        const pattern = new RegExp(`^${prefix}\\d+$`);
        return pattern.test(str);
    }

    replaceValuesWithFalse(obj: GenericObject) {
        if (typeof obj !== 'object' || obj === null) {
          return false;
        }
      
        for (const key in obj) {
          if (Object.prototype.hasOwnProperty.call(obj, key)) {
            obj[key] = this.replaceValuesWithFalse(obj[key]);
          }
        }
        return obj;
    }

    checkRegArr (key: string, prop: GenericObject) {
      const itemkeyPattern = key.replace(/[-/\\^$*+?.()|[\]{}]/g, '\\$&');
      let matchedValue = null;
      for (const key in prop) {
          if (Object.prototype.hasOwnProperty.call(prop, key)) {
              const value = prop[key];
              const regex = new RegExp(`.*${key}.*`);
              if (regex.test(itemkeyPattern)) {
                  matchedValue = value;
                  break;
              }
          }
      }
      return matchedValue;
    }
*/
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
