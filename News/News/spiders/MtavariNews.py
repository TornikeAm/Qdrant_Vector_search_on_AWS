import scrapy
from ..items import WebscrappingItem

class NewsSpider(scrapy.Spider):
    name = "News"
    start_urls = ["https://mtavari.tv/news/archive"]

    def parse(self, response):
        title = response.css("title::text").extract_first()
        news = response.xpath("/html/body/div/div/div[4]/div/div/div/div/div[1]")

        for news_element in news:
            items = WebscrappingItem()

            items["hrefs"] = news_element.xpath(".//a/@href").extract()
            items["images"] = news_element.xpath(".//section[@class='NewsItem__Container-sc-4tbadf-8 dSSPDS']//img/@src").extract()
            items["headings"] = news_element.css(".gZyskT::text").extract()
            items["time"] = news_element.css("time::text").extract()

            # Initialize 'text' field as an empty list
            # items["text"] = []
            yield items
            # for href in items["hrefs"]:
            #     # Follow the link and parse the content inside
            #     # yield scrapy.Request(url=f"https://mtavari.tv{href}", callback=self.parse_inside_news, meta={'items': items.copy()})

    # def parse_inside_news(self, response):
    #     items = response.meta['items']
    #
    #     paragraphs = response.xpath('//div[@class="EditorContent__EditorContentWrapper-ygblm0-0 dzgBwY"]/p/text()').getall()
    #     text = " ".join(paragraphs)
    #
    #     # Append the new text as a separate element in the list
    #     items["text"].append(text)
    #
    #     # Yield the complete dictionary after processing the last text
    #     yield items
