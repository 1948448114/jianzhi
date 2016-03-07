# -*- coding: utf-8 -*-
#!/usr/bin/env python
# @Date    : 2015-11-18 21:20:05
# @Author  : jerry.liangj@qq.com
import hashlib
import json
from sqlalchemy.orm.exc import NoResultFound
from ..Basehandler import BaseHandler
import traceback
from ..databases.tables import Users,Access_Token

class ChangePictureHandler(BaseHandler):
    def options(self):
        retjson = {'code':200}
        self.set_header('Access-Control-Allow-Methods','GET')
        self.set_header('Access-Control-Allow-Headers','token')
        self.write_back(retjson)

    def post(self):
        retjson = {'code':200,'content':'ok'}
        token = self.get_current_user()
        if not token:
            retjson['code'] = 400
            retjson['content'] = u'请先登录'
        else:
            try:
                picture = self.get_argument('picture',default=None)
                if not(picture):
                    retjson['code'] = 401
                    retjson['content'] = u'参数缺少 '
                user = self.db.query(Users).filter(Users.phone == token.phone).one()
                user.picture = picture
                self.db.add(user)
                self.db.commit()
            except NoResultFound:
                retjson['code'] = 301
                retjson['content'] = u'用户不存在'
            except:
                print traceback.print_exc()
                self.db.rollback()
                retjson['code'] = 500
                retjson['content'] = u'系统错误'

        self.write_back(retjson)

