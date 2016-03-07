#!/usr/bin/python
#-*- encoding:utf-8 -*-
import traceback
import tornado.ioloop
import tornado.web
import shutil
import os
import hashlib
import json
from ..Basehandler import BaseHandler
import hashlib,json

class UploadHandler(BaseHandler):
    def options(self):
        retjson = {'code':200}
        self.set_header('Access-Control-Allow-Methods','GET')
        self.set_header('Access-Control-Allow-Headers','admin')
        self.write_back(retjson)

    def post(self):
        save_path = '../jianzhiApp/static/img'
        retjson = {'code':200,'content':'portrait upload success!'}
        try:
            file_metas=self.request.files['file']   #提取表单中‘name’为‘file’的文件元数据
            if file_metas:
                for meta in file_metas:
                    filename=meta['filename']
                    houzhui = filename.split('.')[-1:][0]
                    sha1obj = hashlib.md5()
                    sha1obj.update(meta['body'])
                    hash = sha1obj.hexdigest()
                    filepath = save_path +'/'+ sha1obj.hexdigest() + '.' + houzhui
                    with open(filepath,'wb') as up:      #有些文件需要已二进制的形式存储，实际中可以更改
                        up.write(meta['body'])
                    retjson['path'] = sha1obj.hexdigest() + '.' + houzhui
            else:
                retjson = {'code':400,'content':'failed to upload portrait'}

        except:
            print traceback.print_exc()
            retjson['code'] = 500
            retjson['content'] = u'系统错误'
        self.write_back(retjson)
