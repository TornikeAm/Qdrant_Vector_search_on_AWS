# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class WebscrappingPipeline:
    def process_item(self, item, spider):
        # #
        # # print("ager itemebi pipelinedi")
        # keys = ["link", "image", "heading", "time"]
        # hrefs = item["hrefs"]
        # images = item["images"]
        # headings = item["headings"]
        # time = item["time"]
        # # /text = item["text"]
        # items_list = zip(hrefs, images, headings, time)
        # items = [dict(zip(keys, values)) for values in items_list]
        # # item = zip()
        return item
