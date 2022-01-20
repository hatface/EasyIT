# Create your models here.
# coding:utf-8
from __future__ import unicode_literals
# Create your models here.
from bson import ObjectId
from config.mongodb_cfg import DBCONNECT

class CapabilityFilingManager():
    def __init__(self,mDatabase=None):
        self.mDatabase = DBCONNECT if not mDatabase else mDatabase
        self.col = self.mDatabase.get_collection("CapabilityFilingManage")
        self.__capabilityFiling_col = self.col['CapabilityFilingData']

    def add_capabilityFiling_data(self, data):
        '''
        @see: 插入CapabilityFiling数据
        '''
        id_obj = ObjectId()
        data['_id'] = id_obj
        #if not data.has_key('id'):
        if 'id' not in data:
            data['id'] = str(data['_id'])
        return self.__capabilityFiling_col.insert_one(data),data

    def remove_capabilityFiling_data(self,id):
        return self.__capabilityFiling_col.remove({"id":id})

    def update_capabilityFiling_data(self,id,data):
        return self.__capabilityFiling_col.update({"id": id},{"$set": data})

    def get_capabilityFiling_data_by_id(self,id):
        return self.search_capabilityFiling_data({"id": id})[0]

    def search_capabilityFiling_data(self,filter_json={},offset=0,limit=0,sort_key="id",order="desc"):
        mfilter = {}
        if filter_json:
            for fkey in filter_json:
                regx = ".*" + filter_json[fkey] + ".*"
                mfilter[fkey] = {"$regex": regx}
        capabilityFiling_list = []
        ova = -1 if order=="desc" else 1
        for capabilityFiling_rec in self.__capabilityFiling_col.find(mfilter).sort(sort_key,ova).skip(offset).limit(limit):
            capabilityFiling_rec['_id'] = str(capabilityFiling_rec['_id'])
            capabilityFiling_list.append(capabilityFiling_rec)
        return capabilityFiling_list

    def get_capabilityFiling_data_count(self,filter_json={}):
        mfilter = {}
        if filter_json:
            for fkey in filter_json:
                regx = ".*" + filter_json[fkey] + ".*"
                mfilter[fkey] = {"$regex": regx}
        return self.__capabilityFiling_col.find(mfilter).count()


    def aggregate_search(self, cmd):
        return self.__capabilityFiling_col.aggregate(cmd)


    def custom_group_search(self, key, limit=None, split=True,filter_json=None):
        mfilter = {}
        if filter_json:
            for fkey in filter_json:
                regx = ".*" + filter_json[fkey] + ".*"
                mfilter[fkey] = {"$regex":regx}
        cmd = [
            {'$match': mfilter},
            {'$project': {"name": "$" + key}},
            {"$group": {"_id": "$name", "number": {"$sum": 1}}},
            {"$sort": {"number": -1}},
        ]
        if limit:
            cmd.append({"$limit": limit})

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
                item = {}
                item['name'] = rec['_id']
                item['value'] = rec['number']
                result.append(item)
            return result

    def close(self):
        '''
        @see: 关闭Mongo连接
        '''
        self.mDatabase.close()
#单例模式
capabilityFilingManager = CapabilityFilingManager()
