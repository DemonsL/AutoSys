# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import json
import logging
import datetime
import redis
from .settings import REDIS_HOST, REDIS_PORT, REDIS_PASS
from .db_models import DBSession, ApbBestSeller

logger = logging.getLogger(__name__)

class CrawlsPipeline(object):

    conn = None
    item_key = 'item_list'
    snap_data = datetime.datetime.today().date()

    def open_spider(self, spider):
        self.conn = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASS, decode_responses=True)

    def process_item(self, item, spider):
        self.conn.lpush(self.item_key, json.dumps(dict(item)))
        return item

    def close_spider(self, spider):
        self.save_items()

    def save_items(self):
        self.del_best_seller()
        if self.conn.llen(self.item_key):
            self.add_best_seller()


    # ------ 数据库处理方法 -------

    def add_best_seller(self):
        session = DBSession()
        try:
            while self.conn.llen(self.item_key):
                data = json.loads(self.conn.lpop(self.item_key))
                session.add(ApbBestSeller(self.snap_data, data))
            session.commit()
        except Exception as e:
            logger.info('AddBestSellerError: %s' % e)
        finally:
            session.close()

    def del_best_seller(self):
        session = DBSession()
        try:
            session.query(ApbBestSeller).filter(ApbBestSeller.SnapDate == self.snap_data) \
                                        .delete(synchronize_session=False)
            session.commit()
        except Exception as e:
            logger.info('DeleteBestSellerError: %s' % e)
        finally:
            session.close()

    # def update_best_seller(self):
    #     session = DBSession()
    #     try:
    #         while self.conn.llen(self.up_key):
    #             data = json.loads(self.conn.lpop(self.up_key))
    #             session.query(ApbBestSeller).filter(and_(and_(and_(
    #                                                 ApbBestSeller.SnapDate == self.snap_data,
    #                                                 ApbBestSeller.Country == data.get('Country')),
    #                                                 ApbBestSeller.CategoryID == data.get('CategoryID')),
    #                                                 ApbBestSeller.Rank == data.get('Rank'))) \
    #                                         .update(update_best_seller(data))
    #         session.commit()
    #     except Exception as e:
    #         logger.info('UpdateBestSellerError: %s' % e)
    #     finally:
    #         session.close()





