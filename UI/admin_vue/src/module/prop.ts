import { GenericObject } from "./type";

export class PATH {
    buttonsrc = '/img/openicon.png';
    homeicon = '/img/homeicon.png';
    pagelisticon = '/img/pagelisticon.png';
    openicon = '/img/openicon.png';
    closeicon = '/img/closeicon.png';
    closebutton = '/img/closebutton.png';
    trashicon = '/img/trashicon.png';
    addcontenticon = '/img/addcontenticon.png';
    categoryicon = '/img/category_icon.png';
    detailDirFormat (value: string) {
        return `/${value}/language/${process.env.VUE_APP_FromCode}`;
    }
}
export class TAG {
    notDisplayArr: string[] = [
        'ogImg', 'description', 'pageName', 'categoryID',
        'created', 'updated', 'thumbnail', 'ogImg',
        'description'
    ];
    getElementTag(itemKey: string) {
        let res = '';
        let display = true;

        this.notDisplayArr.forEach((obj: string) => {
            if (itemKey === obj) {
                display = false;
            }
        });

        if (!display) {
            return false;
        } 

        if (itemKey == 'pagetitle' ) {
            res = 'title';
        }
        if (/contenttitle\d+/.test(itemKey)) {
            res = 'h2';
        }
        if (/contentsecondtitle\d+/.test(itemKey)) {
            res = 'h3';
        }
        if (/contentthirdtitle\d+/.test(itemKey)) {
            res = 'h4';
        }
        if (/contentforthtitle\d+/.test(itemKey)) {
            res = 'h5';
        }
        if (/contentfifthtitle\d+/.test(itemKey)) {
            res = 'h6';
        }
        if (/content\d+/.test(itemKey)) {
            res = 'p';
        }
        if (/boxmenu\d+/.test(itemKey)) {
            res = 'boxmenu';
        }
        if (/articleFullImg\d+/.test(itemKey)) {
            res = 'full-img';
        }
        if (/articleMiddleImg\d+/.test(itemKey)) {
            res = 'middle-img';
        }
        if (/articleSmallImg\d+/.test(itemKey)) {
            res = 'small-img';
        }
        if (/articleTinyImg\d+/.test(itemKey)) {
            res = 'tiny-img';
        }
        if (/donutMeter\d+/.test(itemKey)) {
            res = 'donut-meter';
        }
        if (/topArticleTable\d+/.test(itemKey)) {
            res = 'top-article-table';
        }
        if (/purchaseButton\d+/.test(itemKey)) {
            res = 'purchase-button';
        }
        return res;
    }
    getTagLabel (key: string) {
        return `for-${key}`;
    }
    getElementTagLabel (key: string) {
        return `for-${this.getElementTag(key)}`;
    }

    tProp = {
        "h2": {
            "tagname": "h2",
            "tagfor": "for-h2",
            "matchpattern": "contenttitle"
        },
        "h3": {
            "tagname": "h3",
            "tagfor": "for-h3",
            "matchpattern": "contentsecondtitle"
        },
        "h4": {
            "tagname": "h4",
            "tagfor": "for-h4",
            "matchpattern": "contentthirdtitle"
        },
        "h5": {
            "tagname": "h5",
            "tagfor": "for-h5",
            "matchpattern": "contentforthtitle"
        },
        "h6": {
            "tagname": "h6",
            "tagfor": "for-h6",
            "matchpattern": "contentfifthtitle"
        },
        "p": {
            "tagname": "p",
            "tagfor": "for-p",
            "matchpattern": "content"
        },
        "fullimg": {
            "tagname": "img",
            "tagfor": "for-full-img",
            "matchpattern": "articleFullImg"
        },
        "middleimg": {
            "tagname": "img",
            "tagfor": "for-middle-img",
            "matchpattern": "articleMiddleImg"
        },
        "smallimg": {
            "tagname": "img",
            "tagfor": "for-small-img",
            "matchpattern": "articleSmallImg"
        },
        "tinyimg": {
            "tagname": "img",
            "tagfor": "for-tiny-img",
            "matchpattern": "articleTinyImg"
        },
        "boxmenu": {
            "tagname": "div",
            "tagfor": "for-boxmenu",
            "matchpattern": "boxmenu"
        },
        "donutMeter": {
            "tagname": "canvas",
            "tagfor": "donut-meter",
            "matchpattern": "donutMeter"
        },
        "topArticleTable": {
            "tagname": "table",
            "tagfor": "top-article-table",
            "matchpattern": "topArticleTable"
        },
        "purchaseButton": {
            "tagname": "button",
            "tagfor": "purchase-button",
            "matchpattern": "purchaseButton"
        },
    }
    tagjson: GenericObject = {
        "for-full-img": "w-100",
        "for-middle-img": "w-75",
        "for-small-img": "w-50",
        "for-tiny-img": "w-25"
    }
}

export const lnarr = {
    "アラビア語": "ar",
    "アゼルバイジャン語": "az",
    "ベラルーシ語": "be",
    "ブルガリア語": "bg",
    "ベンガル語": "bn",
    "英語": "en",
    "アフリカーンス語": "af",
    "アムハラ語": "am",
    "ボスニア語": "bs",
    "カタロニア語": "ca",
    "チェコ語": "cs",
    "ウェールズ語": "cy",
    "ドイツ語": "de",
    "ギリシャ語": "el",
    "エスペラント語": "eo",
    "スペイン語": "es",
    "エストニア語": "et",
    "バスク語": "eu",
    "ペルシャ語": "fa",
    "フィンランド語": "fi",
    "フランス語": "fr",
    "ガリシア語": "gl",
    "グジャラート語": "gu",
    "ヘブライ語": "he",
    "ヒンディー語": "hi",
    "クロアチア語": "hr",
    "ハンガリー語": "hu",
    "アルメニア語": "hy",
    "インドネシア語": "id",
    "アイスランド語": "is",
    "イタリア語": "it",
    "ジャワ語": "jv",
    "カザフ語": "kk",
    "クメール語": "km",
    "カンナダ語": "kn",
    "韓国語": "ko",
    "クルド語": "ku",
    "リトアニア語": "lt",
    "ラトビア語": "lv",
    "マケドニア語": "mk",
    "マラヤーラム語": "ml",
    "モンゴル語": "mn",
    "マラーティー語": "mr",
    "マレー語": "ms",
    "ミャンマー語": "my",
    "ネパール語": "ne",
    "オランダ語": "nl",
    "パンジャブ語": "pa",
    "ポーランド語": "pl",
    "ポルトガル語": "pt",
    "ルーマニア語": "ro",
    "ロシア語": "ru",
    "シンド語": "sd",
    "シンハラ語": "si",
    "スロバキア語": "sk",
    "スロベニア語": "sl",
    "アルバニア語": "sq",
    "スウェーデン語": "sv",
    "スワヒリ語": "sw",
    "タミル語": "ta",
    "テルグ語": "te",
    "タイ語": "th",
    "タガログ語": "tl",
    "トルコ語": "tr",
    "タヒチ語": "ty",
    "ウイグル語": "ug",
    "ウルドゥ語": "ur",
    "ウズベク語": "uz"
}
export const fullLinArr = {
    "ar": "Arabic",
    "az": "Azerbaijani",
    "be": "Belarusian",
    "bg": "Bulgarian",
    "bn": "Bengali",
    "en": "English",
    "af": "Afrikaans",
    "am": "Amharic",
    "bs": "Bosnian",
    "ca": "Catalan",
    "cs": "Czech",
    "cy": "Welsh",
    "de": "German",
    "el": "Greek",
    "eo": "Esperanto",
    "es": "Spanish",
    "et": "Estonian",
    "eu": "Basque",
    "fa": "Persian",
    "fi": "Finnish",
    "fr": "French",
    "gl": "Galician",
    "gu": "Gujarati",
    "he": "Hebrew",
    "hi": "Hindi",
    "hr": "Croatian",
    "hu": "Hungarian",
    "hy": "Armenian",
    "id": "Indonesian",
    "is": "Icelandic",
    "it": "Italian",
    "jv": "Javanese",
    "kk": "Kazakh",
    "km": "Khmer",
    "kn": "Kannada",
    "ko": "Korean",
    "ku": "Central Kurdish",
    "lt": "Lithuanian",
    "lv": "Latvian",
    "mk": "Macedonian",
    "ml": "Malayalam",
    "mn": "Mongolian",
    "mr": "Marathi",
    "ms": "Malay",
    "my": "Burmese",
    "ne": "Nepali",
    "nl": "Dutch",
    "pa": "Punjabi",
    "pl": "Polish",
    "pt": "Portuguese",
    "ro": "Romanian",
    "ru": "Russian",
    "sd": "Sindhi",
    "si": "Sinhala",
    "sk": "Slovak",
    "sl": "Slovenian",
    "sq": "Albanian",
    "sv": "Swedish",
    "sw": "Swahili",
    "ta": "Tamil",
    "te": "Telugu",
    "th": "Thai",
    "tl": "Tagalog",
    "tr": "Turkish",
    "ty": "Tahitian",
    "ug": "Uighur",
    "ur": "Urdu",
    "uz": "Uzbek"
}