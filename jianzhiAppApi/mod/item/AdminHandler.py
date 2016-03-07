# -*- coding: utf-8 -*-
#!/usr/bin/env python
# @Date    : 2015-11-18 21:20:05
# @Author  : jerry.liangj@qq.com
import json
from ..Basehandler import BaseHandler
import traceback
from ..databases.tables import Item
from sqlalchemy.orm.exc import NoResultFound
from time import time

class NewItemHandler(BaseHandler):
    """
        新建兼职
    """
    def options(self):
        retjson = {'code':200}
        self.set_header('Access-Control-Allow-Methods','GET')
        self.set_header('Access-Control-Allow-Headers','admin')
        self.write_back(retjson)

    def post(self):
        retjson = {'code':200,'content':'ok'}
        name = self.get_argument('name',default=None)
        price = self.get_argument('price',default=None)
        wanted_number = self.get_argument('wanted_number',default=None)
        location = self.get_argument('location',default=None)
        detail = self.get_argument('detail',default=None)
        start_time = self.get_argument('start_time',default=None)
        end_time = self.get_argument('end_time',default=None)
        create_time = int(time())
        try:
            if not(name and price and wanted_number and location and detail and start_time and end_time):
                retjson['code'] = 400
                retjson['content'] = u'参数缺少'
            else:
                admin = self.get_current_admin()
                if admin:
                    start_time = self.change_time(start_time,0)
                    end_time = self.change_time(end_time,0)
                    item = Item(state=9,name=name,price=float(price),wanted_number=int(wanted_number),\
                                location=location,detail=detail,start_time=start_time,end_time=end_time,create_time=create_time,\
                                reg_number=0)
                    self.db.add(item)
                    self.db.commit()
                else:
                    retjson['code'] = 401
                    retjson['content'] = u'请先登录'
        except Exception,e:
            self.db.rollback()
            retjson['code'] = 500
            retjson['content'] = u'系统错误'
        self.write_back(retjson)


class GetAllItemHandler(BaseHandler):
    """
        获取所有兼职
    """
    def options(self):
        retjson = {'code':200}
        self.set_header('Access-Control-Allow-Methods','GET')
        self.set_header('Access-Control-Allow-Headers','admin')
        self.write_back(retjson)

    def post(self):
        """
        state:
            8:不可预约
            9:可预约
        """
        retjson = {'code':200,'content':'ok'}

        token = self.get_current_admin()
        if not token:
            retjson['code'] = 401
            retjson['content'] = u'请先登录'
        else:
            try:
                pagenum = int(self.get_argument('pagenumber',default=1))
                pagesize = int(self.get_argument('pagesize',default=10))
                item = self.db.query(Item).filter(Item.state==9).order_by(Item.end_time.desc()).offset((pagenum-1)*pagesize).limit(pagesize).all()
                content = []
                for i in item:
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

class DownItemHandler(BaseHandler):
    """
        下架兼职
    """
    """
    """
    def options(self):
        retjson = {'code':200}
        self.set_header('Access-Control-Allow-Methods','GET')
        self.set_header('Access-Control-Allow-Headers','admin')
        self.write_back(retjson)

    def post(self):
        """
        state:
            8:不可预约
            9:可预约
        """
        retjson = {'code':200,'content':'ok'}
        iid = self.get_argument('iid',default=None)
        token = self.get_current_admin()
        if not token:
            retjson['code'] = 401
            retjson['content'] = u'请先登录'
        else:
            if not iid:
                retjson['code'] = 400
                retjson['content'] = u'参数缺少'
            else:
                try:
                    result = self.db.query(Item).filter(Item.iid==int(iid)).one()
                    self.db.delete(result)
                    self.db.commit()
                except NoResultFound:
                    retjson['code'] = 403
                    retjson['content'] = u'该兼职不存在'
                except:
                    self.db.rollback()
                    retjson['code'] = 500
                    retjson['content'] = u'系统错误'

        self.write_back(retjson)