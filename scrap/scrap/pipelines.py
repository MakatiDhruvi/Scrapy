# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import psycopg2
from scrapy.exceptions import DropItem

# class ScrapPipeline:
#     def process_item(self, item, spider):

#         print("Pipeline :" + item['title'][0])
#         return item



class TutorialPipeline(object):
    

    def __init__(self):
        self.items = set()

    def open_spider(self, spider):
        hostname = 'localhost'
        username = 'postgres'
        password = 'Dhruvi@2001' 
        database = 'quotes'
        self.connection = psycopg2.connect(host=hostname, user=username, password=password, dbname=database)
        self.cur = self.connection.cursor()

    def close_spider(self, spider):
        self.cur.close()
        self.connection.close()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        self.cur.execute("select * from quotes where title = '" + str(adapter['title'][0][1:-1]).replace("'", "''") + "'")
        quote = self.cur.fetchall()
        if len(quote) > 0:
            return "Quote already exists in database"
        else:
            self.cur.execute("insert into quotes(title,author,tags) values(%s,%s,%s)",(item['title'][0][1:-1],item['author'][0],item['tag']))
            self.connection.commit()
            return item