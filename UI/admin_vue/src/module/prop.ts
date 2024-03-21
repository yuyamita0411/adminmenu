export class PROP {
    buttonsrc = '/img/openicon.png';
    homeicon = '/img/homeicon.png';
    pagelisticon = '/img/pagelisticon.png';
    openicon = '/img/openicon.png';
    closeicon = '/img/closeicon.png';
    closebutton = '/img/closebutton.png';
    trashicon = '/img/trashicon.png';
    addcontenticon = '/img/addcontenticon.png';

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
        if (/contentthirdttitle\d+/.test(itemKey)) {
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
            res = 'boxmenu'; // 'boxmenu' はHTML標準のタグではありません。カスタム要素や特定の処理に用いる場合が想定されます。
        }
        return res;
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
            "matchpattern": "contentthirdttitle"
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
        }
/*
        ,
        "boxmenu": {
            "matchpattern": "boxmenu"
        }
*/
    }
    bProp = {
        "contenttitle": "h2",
        "contentsecondtitle": "h3",
        "contentthirdttitle": "h4",
        "content": "p",
        "boxmenu": "boxmenu"
    }
}