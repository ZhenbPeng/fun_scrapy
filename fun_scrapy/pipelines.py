# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


# class FunScrapyPipeline(object):
#     def process_item(self, item, spider):
#         return item

import os
import settings
import requests
import logging

logger = logging.getLogger("MeiTu")


class MeiTuPipeline(object):

    def process_item(self, item, spider):
        if 'image_url' in item:
            images = []

            dir_path = '%s/%s' % (settings.MEITU_STORE_PATH, spider.name)

            if not os.path.exists(dir_path):
                os.makedirs(dir_path)

            for image_url in item['image_url']:
                magazine_path = [item['publisher'][-1], item['magazine_no'][0].split(" ")[-1]]
                magazine_path = "_".join(magazine_path)
                magazine_path = '%s/%s' % (dir_path, magazine_path)

                if not os.path.exists(magazine_path):
                    os.makedirs(magazine_path)

                image_file_name = image_url.split("/")[6]
                file_path = '%s/%s' % (magazine_path, image_file_name)
                images.append(file_path)
                if os.path.exists(file_path):
                    continue

                with open(file_path, 'wb') as handle:
                    logger.info("正在下载图片: %s ..." % image_url.encode('utf-8'))
                    response = requests.get(image_url, stream=True)
                    for block in response.iter_content(1024):
                        if not block:
                            break

                        handle.write(block)

                if os.path.exists('%s/%s' % (magazine_path, 'image_info.txt')):
                    with open('%s/%s' % (magazine_path, 'image_info.txt'), 'a') as info:
                        linetext = self.gen_linetext(item, image_file_name, image_url)
                        info.write(linetext)
                else:
                    with open('%s/%s' % (magazine_path, 'image_info.txt'), 'wb') as info:
                        linetext = self.gen_linetext(item, image_file_name, image_url, first=True)
                        info.write(linetext)

            item['file_path'] = images
        return item

    def gen_linetext(self, item, image_file_name, image_url, first=False):
        text = []
        if first:
            text.append(item['sort'][0] + '\n')
            text.append(''.join(item['publisher']) + '\n')
            text.append(item['publishtime'][0] + '\n')
            text.append(''.join(item['model_name']) + '\n')
            text.append(item['magazine_no'][0] + '\n')
            text.append(item['pic_qty'][0] + '\n')
            text.append(item['pixel'][0] + '\n')
            text.append(' '.join(item['tag']) + '\n')
            text.append(item['page_url'][0] + '\n')
            try:
                text.append(item['desc'][0] + '\n')
            except KeyError:
                pass
        text.append(image_url)
        text.append(image_file_name)
        text.append('\n')
        text = ''.join(text)
        return text.encode('utf-8')

