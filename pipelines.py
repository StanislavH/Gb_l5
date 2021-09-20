from pymongo import MongoClient


class JobparserPipeline(object):
    def __init__(self):
        client = MongoClient('localhost', 27017)#['gb_3_mongo']
        self.mongobase = client.vacansy_les5
        #for x in client.vacancy_collection.find({"min_sal": {"$gt": str(sal)}}):
        #    print(x)


    def process_item(self, item, spider):
        collection = self.mongobase[spider.name]
        collection.insert_one(item)
        #print(item['sal_from'])

        return item
