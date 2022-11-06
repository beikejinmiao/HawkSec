#!/usr/bin/env python
# -*- coding:utf-8 -*-

# https://stackoverflow.com/questions/4212861/what-is-a-correct-mime-type-for-docx-pptx-etc
office_mime = {
    'application/pdf': 'pdf',
    'application/msword': 'doc',
    'application/vnd.ms-excel': 'xls',
    'application/vnd.ms-powerpoint': 'ppt',
    'application/x-xls': 'xls',
    'application/x-ppt': 'ppt',
    'application/x-ppm': 'ppt',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document': 'docx',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.template': 'dotx',
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': 'xlsx',
    'application/vnd.openxmlformats-officedocument.spreadsheetml.template': 'xltx',
    'application/vnd.openxmlformats-officedocument.presentationml.presentation': 'pptx',
    'application/vnd.openxmlformats-officedocument.presentationml.template': 'potx',
    'application/vnd.openxmlformats-officedocument.presentationml.slideshow': 'ppsx',
    # ......
}


def is_office_mime(content_type):
    if not isinstance(content_type, str):
        return False
    content_type = content_type.lower()
    if content_type.startswith('application/vnd.ms-word'):
        return True
    if content_type.startswith('application/vnd.ms-excel'):
        return True
    if content_type.startswith('application/vnd.ms-powerpoint'):
        return True
    if content_type.startswith('application/vnd.openxmlformats-officedocument'):
        return True
    if content_type in office_mime:
        return True
    return False


zip_mime = {
    'application/zip': 'zip',
    'application/gzip': 'gz',
    'application/x-7z-compressed': '7z',
    'application/vnd.rar': 'rar',
    'application/x-tar': 'tar',
    'application/x-bzip': 'bz',
    'application/x-bzip2': 'bz2',
    'application/x-gzip': 'tar.gz',
    'application/tar+gzip': 'tar.gz',
}


def is_zip_mime(content_type):
    if not isinstance(content_type, str):
        return False
    return content_type.lower() in zip_mime

