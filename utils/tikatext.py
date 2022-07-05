#!/usr/bin/env python
# -*- coding:utf-8 -*-
from tika import parser
from libs.regex import plain_text, html, js_css


def plaintext(path, encoding='gbk'):
    if plain_text.match(path) or html.match(path) or js_css.match(path):
        try:
            with open(path, encoding=encoding) as fopen:
                return fopen.read()
        except UnicodeDecodeError:
            with open(path, encoding='gbk' if encoding is 'utf-8' else 'utf-8') as fopen:
                return fopen.read()
        # gbk/utf-8均解码错误，使用tika解析
        except:
            parsed = parser.from_file(path)
            return parsed["content"]
    else:
        parsed = parser.from_file(path)
        return parsed["content"]



