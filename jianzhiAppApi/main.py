# -*- coding: utf-8 -*-
#!/usr/bin/env python
import tornado.httpserver
import tornado.ioloop
import tornado.web
import os,json
from tornado.options import define, options

from sqlalchemy.orm import scoped_session, sessionmaker
from mod.auth.login import LoginHandler
from mod.auth.registerHandler import RegisterHandler
from mod.auth.adminLogin import AdminLoginHandler

from mod.info.handler import GetInfoHandler,ChangeInfoHandler
from mod.info.changePicture import ChangePictureHandler

from mod.item.UserHandler import GetItemListHandler,GetMyItemListHandler
from mod.item.AdminHandler import NewItemHandler,GetAllItemHandler,DownItemHandler

from mod.record.UserNewHandler import NewRecordHandler
from mod.record.UserDeleteHandler import DeleteRecordHandler
from mod.record.AdminGetListHandler import GetRecordHandler
from mod.record.AdminDealHandler import AdminDealHandler

from mod.file.upload import UploadHandler

from mod.databases.db import engine

define("port", default=8000, help="run on the given port", type=int)

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/jianzhi/api/v1/auth/login',LoginHandler),
            (r'/jianzhi/api/v1/auth/reg',RegisterHandler),
            (r'/jianzhi/api/v1/admin/login',AdminLoginHandler),
            (r'/jianzhi/api/v1/info/get',GetInfoHandler),
            (r'/jianzhi/api/v1/info/update',ChangeInfoHandler),
            (r'/jianzhi/api/v1/info/picture',ChangePictureHandler),
            (r'/jianzhi/api/v1/item/list',GetItemListHandler),
            (r'/jianzhi/api/v1/item/mylist',GetMyItemListHandler),
            (r'/jianzhi/api/v1/item/admin/list',GetAllItemHandler),
            (r'/jianzhi/api/v1/item/admin/new',NewItemHandler),
            (r'/jianzhi/api/v1/item/admin/down',DownItemHandler),
            (r'/jianzhi/api/v1/record/new',NewRecordHandler),
            (r'/jianzhi/api/v1/record/delete',DeleteRecordHandler),
            (r'/jianzhi/api/v1/record/admin/list',GetRecordHandler),
            (r'/jianzhi/api/v1/record/admin/change',AdminDealHandler),
            (r'/jianzhi/api/v1/upload',UploadHandler),
            (r'/jianzhi/.*', PageNotFoundHandler)
            ]
        settings = dict(
            cookie_secret="8DB90KLP8371B5AEAC5E64C6042415EE",
            template_path=os.path.join(os.path.dirname(__file__), 'templates'),
            debug=False,
            autoload=False,
            # autoescape=None
        )
        tornado.web.Application.__init__(self, handlers,**settings)
        self.db = scoped_session(sessionmaker(bind=engine,
                                              autocommit=False, autoflush=True,
                                              expire_on_commit=False))

class PageNotFoundHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('404.html')
    def post(self):
        self.render('404.html')

if __name__ == "__main__":
    tornado.options.parse_command_line()
    Application().listen(options.port)
    try:
        tornado.ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        tornado.ioloop.IOLoop.instance().stop()
