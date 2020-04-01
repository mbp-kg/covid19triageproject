# -*- coding: utf-8 -*-

def add_kyrgyz_lang_info():
    from django.conf.locale import LANG_INFO

    LANG_INFO["ky"] = {
        "bidi": False,
        "code": "ky",
        "name": "Kyrgyz",
        "name_local": "Кыргызча",
    }

add_kyrgyz_lang_info()
