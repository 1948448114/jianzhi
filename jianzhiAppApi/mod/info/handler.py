# -*- coding: utf-8 -*-
#!/usr/bin/env python
# @Date    : 2015-11-18 21:20:05
# @Author  : jerry.liangj@qq.com
import hashlib
import json
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import IntegrityError
from ..Basehandler import BaseHandler
import traceback
from ..databases.tables import Users,Access_Token

class GetInfoHandler(BaseHandler):
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
                user = self.db.query(Users).filter(Users.phone == token.phone).one()
                retjson['content'] = {
                    'name':user.name,
                    'picture':user.picture,
                    'course':user.course,
                    'qq':user.qq,
                    'intention':user.intention,
                    'experience':user.experience,
                    'phone':token.phone,
                    'cardnum':user.cardnum
                }
            except NoResultFound:
                retjson['code'] = 301
                retjson['content'] = u'用户不存在'
            except:
                retjson['code'] = 500
                retjson['content'] = u'系统错误'

        self.write_back(retjson)

class ChangeInfoHandler(BaseHandler):
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
                name = self.get_argument('name',default=None)
                cardnum = self.get_argument('cardnum',default=None)
                course = self.get_argument('course',default=None)
                qq = self.get_argument('qq',default=None)
                intention = self.get_argument('intention',default=None)
                experience = self.get_argument('experience',default=None)
                if not(name and cardnum and course and qq ):
                    retjson['code'] = 401
                    retjson['content'] = u'参数缺少 '
                user = self.db.query(Users).filter(Users.phone == token.phone).one()
                user.name = name
                user.cardnum = cardnum
                user.course = course
                user.qq = qq
                user.intention = intention
                user.experience = experience
                self.db.add(user)
                self.db.commit()
            except NoResultFound:
                retjson['code'] = 301
                retjson['content'] = u'用户不存在'
            except IntegrityError:
                retjson['code'] = 301
                retjson['content'] = u'一卡通已经绑定'
            except:
                self.db.rollback()
                retjson['code'] = 500
                retjson['content'] = u'系统错误'

        self.write_back(retjson)

