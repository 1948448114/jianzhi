# -*- coding: utf-8 -*-
#!/usr/bin/env python
# @Date    : 2015-11-18 21:20:05
# @Author  : jerry.liangj@qq.com
from ..Basehandler import BaseHandler
import traceback
from ..databases.tables import Record,Item
from time import time
from sqlalchemy.exc import IntegrityError

class NewRecordHandler(BaseHandler):
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
        token = self.get_current_user()
        if not token:
            retjson['code'] = 400
            retjson['content'] = u'请先登录'
        else:
            try:
                phone = token.phone
                iid = self.get_argument("iid",default=None)
                if not iid:
                    retjson['code'] = 401
                    retjson['content'] = u'缺少参数'
                else:
                    result = self.db.query(Record,Item).filter(Record.phone==phone,Record.iid==iid).all()
                    if len(result)<1:
                        record = Record(phone=phone,iid=iid,state=3,create_time=int(time()))
                        self.db.add(record)
                        self.db.commit()
                    else:
                        retjson['code'] = 402
                        retjson['content'] = u'不能重复预约'
            except IntegrityError:
                retjson['code'] = 403
                retjson['content'] = u'兼职不存在'
            except Exception,e:
                print traeback.print_exc()
                retjson['code'] = 500
                retjson['content'] = u'系统错误'
        self.write_back(retjson)
