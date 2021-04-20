import scrapy

from scrapy.loader import ItemLoader

from ..items import NeximbankngItem
from itemloaders.processors import TakeFirst


class NeximbankngSpider(scrapy.Spider):
	name = 'neximbankng'
	start_urls = ['https://neximbank.com.ng/news/']

	def parse(self, response):
		post_links = response.xpath('//h2/a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

		next_page = response.xpath('//a[@class="next_page"]/@href').getall()
		yield from response.follow_all(next_page, self.parse)

	def parse_post(self, response):
		title = response.xpath('//h4[@class="title"]/text()').get()
		description = response.xpath('//div[@class="the_content_wrapper"]//text()[normalize-space()]|//div[@class="column mcb-column mcb-item-oqgerhs39 three-fifth column_column"]//text()[normalize-space()]').getall()
		description = [p.strip() for p in description if '{' not in p]
		description = ' '.join(description).strip()
		date = response.xpath('//meta[@property="article:published_time"]/@content').get()

		item = ItemLoader(item=NeximbankngItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
