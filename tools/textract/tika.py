#!/usr/bin/env python
# -*- coding:utf-8 -*-
from tika import parser
from libs.regex import plain_text, html, js_css


def tikatext(filepath, encoding='gbk'):
    if plain_text.match(filepath) or html.match(filepath) or js_css.match(filepath):
        try:
            with open(filepath, encoding=encoding) as fopen:
                return fopen.read()
        except UnicodeDecodeError:
            with open(filepath, encoding='gbk' if encoding is 'utf-8' else 'utf-8') as fopen:
                return fopen.read()
        # gbk/utf-8均解码错误，使用tika解析
        except:
            parsed = parser.from_file(filepath)
            return parsed["content"]
    else:
        parsed = parser.from_file(filepath)
        return parsed["content"]



