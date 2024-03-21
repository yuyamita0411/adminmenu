type JsonValue = string | number | boolean | null | JsonArray | JsonObject;
type JsonArray = JsonValue[];
interface JsonObject {
    [key: string]: JsonValue;
}

type NestedObject<T, Depth extends number> = Depth extends 0 
  ? T 
  : { [K in keyof T]: NestedObject<T[K], Depth extends 1 ? 0 : Depth extends 2 ? 1 : Depth extends 3 ? 2 : Depth extends 4 ? 3 : never> };

type MyNestedObject = NestedObject<JsonObject, 4>;

export { JsonValue, JsonArray, JsonObject, NestedObject, MyNestedObject};
interface StoreState {
  [key: string]: any; // 任意のキーと値を持つことができる
}
/*
interface StoreState {
  modaldisplaystatus: string;
  targetTagInfo: TargetTagInfo;//今ターゲットになってるタグの詳細情報を更新する
  EditingTargetIndex: { [key: number]: any };//今ターゲットになってるタグは何番目なのかを記録する
  targetTagNow: string;
  targetTagDetail: string;
  addtag: string;
  nexttagNum: number;

  whichtag: string;
  additemkey: string;
  jsondata: any;
}*/
interface TargetTagInfo {
  order: number,
  setTargetTagNow: string,
  setTargetTagDetail: string
}
interface State {
  targetTagNow: string;
  targetTagDetail: string;
  whichtag: string;
  additemkey: string;
  jsondata: any;
}
interface UpdateStatePayload {
  key: keyof State;
  value: State[keyof State];
}
interface GenericObject {
  [key: string]: any;
}
export { StoreState, TargetTagInfo, State, UpdateStatePayload, GenericObject }