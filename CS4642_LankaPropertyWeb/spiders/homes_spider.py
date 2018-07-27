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

		pricestr=response.css('div.price-detail::text').extract_first().strip().replace(",","")
		price=[int(s) for s in pricestr.split() if s.isdigit()][0]

		yield{
			'title':response.css('div.details-heading.details-property h1::text').extract_first(),
			'location':response.css('span.details-location::text').extract_first(),
			'price':price,
			'property_details':[item.strip() for item in response.css('div.details-heading p::text').extract()],
		
			'property_type': response.css('tr').extract()[0].split('<tr>\n<td class="left">Property Type:</td>\n<td class="right">')[1].split('</td>\n</tr>')[0],
			'bedrooms':response.css('tr').extract()[1].split('<tr>\n<td class="left">Bedrooms:</td>\n<td class="right">')[1].split('</td>\n</tr>')[0],
			'bathrooms/WCs':response.css('tr').extract()[2].split('<tr>\n<td class="left">Bathrooms/WCs:</td>\n<td class="right">')[1].split('</td>\n</tr>')[0],
			'floor_area':response.css('tr').extract()[3].split('<tr>\n<td class="left">Floor area:</td>\n<td class="right">')[1].split('</td>\n</tr>')[0],
			'no_of_floors':response.css('tr').extract()[4].split('<tr>\n<td class="left">No. of floors:</td>\n<td class="right">')[1].split('</td>\n</tr>')[0],
			'area_of_land':response.css('tr').extract()[5].split('<tr>\n<td class="left">Area of land:</td>\n<td class="right">')[1].split('</td>\n</tr>')[0],
			'availability':response.css('tr').extract()[6].split('<tr>\n<td class="left">Availability:</td>\n<td class="right">\n<font color="black"><b>')[1].split('</b></font> </td>\n</tr>')[0],
			'nearest_bus_stop':response.css('tr').extract()[7].split('<tr>\n<td class="left">Nearest bus stop:</td>\n<td class="right">')[1].split('</td>\n</tr>')[0],
			'nearest_train_station':response.css('tr').extract()[8].split('<tr>\n<td class="left">Nearest train station:</td>\n<td class="right">')[1].split('</td>\n</tr>')[0],

		}