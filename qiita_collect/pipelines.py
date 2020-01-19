# -*- coding: utf-8 -*-
from sqlalchemy.orm import sessionmaker
from qiita_collect.models import QiitaCollectDatabase, db_connect, create_table

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


class QiitaCollectPipeline(object):
    def __init__(self):
        engine = db_connect()
        create_table(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        session = self.Session()
        qiitacollectdb = QiitaCollectDatabase()
        qiitacollectdb.keyword = item['keyword']
        qiitacollectdb.title = item['title']
        qiitacollectdb.url = item['url']

        try:
            session.add(qiitacollectdb)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

        return item
