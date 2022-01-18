# Create your models here.
# coding:utf-8
from __future__ import unicode_literals

from django.db import models
from django.conf import settings
import datetime

# Create your models here.
from bson import ObjectId
from config.mongodb_cfg import DBCONNECT
import os
class VisitManager():
    def __init__(self,mDatabase=None):
        self.mDatabase = DBCONNECT if not mDatabase else mDatabase
        self.col = self.mDatabase.get_collection("VisitManager")
        self.__visit_col = self.col['VisitData']

    def add_visit_data(self, data):
        '''
        @see: 插入Visit数据
        '''
        id_obj = ObjectId()
        data['_id'] = id_obj
        data['id'] = str(data['_id'])
        data['visitTime'] = datetime.datetime.now().strftime("%Y-%m-%d")
        return self.__visit_col.insert_one(data)

    def search_visit_data(self,filter={},offset=0,limit=0,sort_key="id",order="desc"):
        visit_list = []
        ova = -1 if order=="desc" else 1
        for visit_rec in self.__visit_col.find(filter).sort(sort_key,ova).skip(offset).limit(limit):
            visit_rec['_id'] = str(visit_rec['_id'])
            visit_list.append(visit_rec)
        return visit_list

    def get_visit_data_count(self,filter={}):
        return self.__visit_col.find(filter).count()

    def aggregate_search(self,cmd):
        return self.__visit_col.aggregate(cmd)

    def custom_group_search(self,key,limit=None,split=True):
        cmd = [
            {'$project': {"name": "$"+key}},
            {"$group": {"_id": "$name", "number": {"$sum": 1}}},
            {"$sort": {"number": -1}},
        ]
        if limit:
            cmd.append( {   "$limit": limit})

        if split:
            item = []
            value = []
            for rec in self.aggregate_search(cmd):
                if rec['_id']:
                    item.append(rec["_id"])
                    value.append(rec['number'])
            return {"item": item, "value": value}
        else:
            result = []
            for rec in self.aggregate_search(cmd):
                result.append(rec)
            return result

    def close(self):
        '''
        @see: 关闭Mongo连接
        '''
        self.mDatabase.close()
#单例模式
visitManager = VisitManager()

def add_visit(app,name,request):
    data = {'app':app.split(os.path.sep)[-2],'name':name}
    data['remote_addr'] = request.META['REMOTE_ADDR']
    visitManager.add_visit_data(data)

def get_daily_visit():
    result = visitManager.custom_group_search("visitTime",split=False)
    res_di = {}
    for item in result:
        res_di[item['_id']] = item['number']
    key_li = sorted(res_di.keys())
    item_li = []
    for key in key_li:
        item_li.append(res_di[key])
    return {'item':key_li,'value':item_li}

if __name__ == "__main__":
    print(get_daily_visit())
