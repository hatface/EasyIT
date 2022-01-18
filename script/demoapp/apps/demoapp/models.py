# Create your models here.
# coding:utf-8
from __future__ import unicode_literals
# Create your models here.
from bson import ObjectId
from config.mongodb_cfg import DBCONNECT

class {$upper_english_name$}Manager():
    def __init__(self,mDatabase=None):
        self.mDatabase = DBCONNECT if not mDatabase else mDatabase
        self.col = self.mDatabase.get_collection("{$upper_english_name$}Manage")
        self.__{$english_name$}_col = self.col['{$upper_english_name$}Data']

    def add_{$english_name$}_data(self, data):
        '''
        @see: 插入{$upper_english_name$}数据
        '''
        id_obj = ObjectId()
        data['_id'] = id_obj
        #if not data.has_key('id'):
        if 'id' not in data:
            data['id'] = str(data['_id'])
        return self.__{$english_name$}_col.insert_one(data),data

    def remove_{$english_name$}_data(self,id):
        return self.__{$english_name$}_col.remove({"id":id})

    def update_{$english_name$}_data(self,id,data):
        return self.__{$english_name$}_col.update({"id": id},{"$set": data})

    def get_{$english_name$}_data_by_id(self,id):
        return self.search_{$english_name$}_data({"id": id})[0]

    def search_{$english_name$}_data(self,filter_json={},offset=0,limit=0,sort_key="id",order="desc"):
        mfilter = {}
        if filter_json:
            for fkey in filter_json:
                regx = ".*" + filter_json[fkey] + ".*"
                mfilter[fkey] = {"$regex": regx}
        {$english_name$}_list = []
        ova = -1 if order=="desc" else 1
        for {$english_name$}_rec in self.__{$english_name$}_col.find(mfilter).sort(sort_key,ova).skip(offset).limit(limit):
            {$english_name$}_rec['_id'] = str({$english_name$}_rec['_id'])
            {$english_name$}_list.append({$english_name$}_rec)
        return {$english_name$}_list

    def get_{$english_name$}_data_count(self,filter_json={}):
        mfilter = {}
        if filter_json:
            for fkey in filter_json:
                regx = ".*" + filter_json[fkey] + ".*"
                mfilter[fkey] = {"$regex": regx}
        return self.__{$english_name$}_col.find(mfilter).count()


    def aggregate_search(self, cmd):
        return self.__{$english_name$}_col.aggregate(cmd)


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
{$english_name$}Manager = {$upper_english_name$}Manager()
