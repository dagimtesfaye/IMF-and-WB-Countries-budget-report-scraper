import scrapy


class CrawlerSpider(scrapy.Spider):
    name = "crawler"
    allowed_domains = ["en.wikipedia.org"]

    start_urls = ["https://en.wikipedia.org/wiki/List_of_countries_by_GDP_(nominal)"]

    def parse(self, response):
        
        main_path = response.xpath('(//table[contains(@class, "wikitable")]/tbody/tr)[position() > 1]')
        for row in main_path:
            yield {
                'country': row.xpath('./td[1]/a/text()').get(),
                'IMF-estimated-GDP': row.xpath('./td[2]/text()').get(),
                'IMF-year': row.xpath('./td[3]/text()').get(),
                'WB-estimated-GDP': row.xpath('./td[4]/text()').get(),
                'WB-year': row.xpath('./td[5]/text()').get(),
                'UN-estimated-GDP': row.xpath('./td[6]/text()').get(),
                'UN-year': row.xpath('./td[7]/text()').get(),
            }