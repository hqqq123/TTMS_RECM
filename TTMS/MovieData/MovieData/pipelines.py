# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import os

import pymysql

# from play.models import Play
import scrapy
from scrapy.pipelines.images import ImagesPipeline
from MovieData.settings import IMAGES_STORE as images_dir


class MoviedataPipeline(object):
    # def process_item(self, item, spider):
    #     # print(type(item),'===========')
    #     # 默认传过来的item是json格式
    #     with open('movie.json', 'a') as f:
    #         json.dump(dict(item), f, ensure_ascii=False, indent=4)
    #         f.write('\n')
    #     # 一定要加， 返回给调度器；
    #     return item

    def __init__(self):
        # 这样写就不会每次保存的时候覆盖上一次了
        self.f = open('movie.json', 'w')

    def process_item(self, item, spider):
        # 默认传过来的item是json格式
        import json
        # 读取item中的数据， 并转成json格式;
        line = json.dumps(dict(item), ensure_ascii=False)
        # line = json.dumps(str(item), ensure_ascii=False)

        self.f.write(line + '\n')
        # 一定要加， 返回给调度器；
        return item

    def open_spider(self, spider):
        """开启爬虫时执行的函数"""
        pass

    def close_spider(self, spider):
        """当爬虫全部爬取结束的时候执行的函数"""
        self.f.close()
class ImagePipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        # 返回一个request请求， 包含图片的url地址
        yield scrapy.Request(item['img'])

    # 当下载请求完成后执行的函数/方法
    def item_completed(self, results, item, info):

        #  获取下载的地址
        image_path = [x['path'] for ok, x in results if ok]
        print(image_path[0],'=================')
        os.rename(images_dir + image_path[0], images_dir + item['name'] + '.jpg')
        return item
