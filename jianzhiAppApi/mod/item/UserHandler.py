# -*- coding: utf-8 -*-
#!/usr/bin/env python
# @Date    : 2015-11-18 21:20:05
# @Author  : jerry.liangj@qq.com
from ..Basehandler import BaseHandler
import traceback
from ..databases.tables import Item,Record
from time import time

class GetItemListHandler(BaseHandler):
    def options(self):
        retjson = {'code':200}
        self.set_header('Access-Control-Allow-Methods','GET')
        self.set_header('Access-Control-Allow-Headers','token')
        self.write_back(retjson)

    def post(self):
        """
        state:
            8:不可预约
            9:可预约
        """
        retjson = {'code':200,'content':'ok'}
        pagenum = int(self.get_argument('pagenumber',default=1))
        pagesize = int(self.get_argument('pagesize',default=10))
        token = self.get_current_user()
        try:
            item_id=[]
            if token:
                item = self.db.query(Item).filter(Item.end_time>int(time()),Item.state==9).order_by(Item.end_time.desc()).\
                    offset((pagenum-1)*pagesize).limit(pagesize).all()
                record = self.db.query(Record).filter(Record.phone==token.phone).all()
                for i in record:
                    item_id.append(i.iid)
            else:
                item = self.db.query(Item).filter(Item.end_time>int(time()),Item.state==9).order_by(Item.end_time.desc()).offset((pagenum-1)*pagesize).\
                    limit(pagesize).all()
            content = []
            for i in item:
                if token:
                    if i.iid in item_id:
                        i.state=8
                    else:
                        i.state=9
                else:
                    i.state=9
                temp = {
                    'iid':i.iid,
                    'name':i.name,
                    'price':i.price,
                    'wanted_number':i.wanted_number,
                    'reg_number':i.reg_number,
                    'detail':i.detail,
                    'location':i.location,
                    'state':i.state,
                    'create_time':self.change_time(i.create_time,1),
                    'start_time':self.change_time(i.start_time,1),
                    'end_time':self.change_time(i.end_time,1)
                }
                content.append(temp)
            retjson['content'] = content
        except Exception,e:
            retjson['code'] = 500
            retjson['content'] = u'系统错误'
        self.write_back(retjson)

class GetMyItemListHandler(BaseHandler):
    def options(self):
        retjson = {'code':200}
        self.set_header('Access-Control-Allow-Methods','GET')
        self.set_header('Access-Control-Allow-Headers','token')
        self.write_back(retjson)

    def post(self):
        """
        state:
            3:用户已预约，未处理
            1:已处理，拒绝
            2：已处理，成功
        """
        retjson = {'code':200,'content':'ok'}
        pagenum = int(self.get_argument('pagenumber',default=1))
        pagesize = int(self.get_argument('pagesize',default=10))
        token = self.get_current_user()
        try:
            if not token:
                retjson['code'] = 400
                retjson['content'] = u'请先登录'
            else:
                item = self.db.query(Record,Item).filter(Record.phone==token.phone).order_by(Record.create_time).\
                    outerjoin(Item,Record.iid==Item.iid).offset((pagenum-1)*pagesize).limit(pagesize).all()
                content = []
                for i in item:
                    state = i[0].state
                    rid = i[0].rid
                    i = i[1]
                    i.state = state
                    i.rid = rid
                    temp = {
                        'iid':i.iid,
                        'name':i.name,
                        'price':i.price,
                        'wanted_number':i.wanted_number,
                        'reg_number':i.reg_number,
                        'detail':i.detail,
                        'location':i.location,
                        'state':i.state,
                        'rid':i.rid,
                        'create_time':self.change_time(i.create_time,1),
                        'start_time':self.change_time(i.start_time,1),
                        'end_time':self.change_time(i.end_time,1)
                    }
                    content.append(temp)
                retjson['content'] = content
        except Exception,e:
            retjson['code'] = 500
            retjson['content'] = u'系统错误'
        self.write_back(retjson)
