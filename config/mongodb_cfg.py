# -*-coding:utf-8-*-
# @Time    : 2018/3/17 14:12
# @Author  : x00293437
import pymongo

MONGODB_HOST = "172.16.136.157"
DATABASE_NAME = "EasyIT"
DBCONNECT = pymongo.MongoClient(host=MONGODB_HOST, port=27017).get_database(DATABASE_NAME)
