import scrapy

class HomesSpider(scrapy.Spider):
	name="homes"
	start_urls = [
		'https://www.lankapropertyweb.com/sale/forsale-all-House.html'
	]

	def parse(self,response):
		for article_title in response.css('h4.listing-titles'):
			yield response.follow(article_title.css('a::attr(href)').extract_first(),callback=self.parse_item_page)

		next_page=response.css('li.pagination_arrows a::attr(href)')[1].extract()
		if next_page is not None:
			yield response.follow(next_page,callback=self.parse)


	def parse_item_page(self,response):
		yield{
			'title':response.css('div.details-heading.details-property h1::text').extract_first(),
			'location':response.css('span.details-location::text').extract_first(),
			'price':response.css('div.price-detail::text').extract_first().strip(),
			'property_details':response.css('div.details-heading p::text').extract(),
		
			'property_type': response.css('tr').extract()[0],
			'bedrooms': response.css('tr').extract()[1],
			'bathrooms/WCs':response.css('tr').extract()[2],
			'floor_area:':response.css('tr').extract()[3],
			'no_of_floors':response.css('tr').extract()[4],
			'area_of_land':response.css('tr').extract()[5],
			'availability':response.css('tr').extract()[6],
			'nearest_bus_stop':response.css('tr').extract()[7],
			'nearest_train_station':response.css('tr').extract()[8],

		}