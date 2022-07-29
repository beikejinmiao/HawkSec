#!/usr/bin/env python
# -*- coding:utf-8 -*-
from peewee import *
import datetime
from conf.paths import DB_PATH

db = None
# db = SqliteDatabase(DB_PATH)


class AbstractModel(Model):
    class Meta:
        database = db


class CrawlStat(AbstractModel):
    id = IntegerField()
    origin = TextField()
    resp_code = IntegerField()
    desc = TextField()
    created_time = DateTimeField(default=datetime.datetime.now)


class Extractor(AbstractModel):
    id = IntegerField()
    origin = TextField()
    sensitive_type = IntegerField()
    sensitive_name = CharField(128)
    content = TextField()
    count = IntegerField()
    desc = TextField()
    created_time = DateTimeField(default=datetime.datetime.now)


class Sensitives(AbstractModel):
    id = IntegerField()
    content = TextField()
    sensitive_type = IntegerField()
    sensitive_name = CharField(128)
    origin = TextField()
    desc = TextField()
    created_time = DateTimeField(default=datetime.datetime.now)


class WhiteList(AbstractModel):
    id = IntegerField()
    white_type = IntegerField()
    ioc = TextField()
    desc = TextField()
    created_time = DateTimeField(default=datetime.datetime.now)


class FileType(AbstractModel):
    id = IntegerField()
    category = CharField(32)
    suffix = CharField(32)
    mime_type = TextField()
    created_time = DateTimeField(default=datetime.datetime.now)

