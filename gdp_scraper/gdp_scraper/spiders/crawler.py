import scrapy


class CrawlerSpider(scrapy.Spider):
    name = "crawler"
    allowed_domains = ["en.wikipedia.org"]
    start_urls = ["https://en.wikipedia.org/wiki/List_of_countries_by_GDP_(nominal)"]

    def parse(self, response):
        rows = response.xpath('(//table[contains(@class, "wikitable")]/tbody/tr)[position() > 1]')

        for row in rows:
            country_name = row.xpath('./td[1]/a/text()').get()
            country_link = row.xpath('./td[1]/a/@href').get()

            item = {
                'country': country_name,
                'IMF-estimated-GDP': row.xpath('./td[2]/text()').get(),
                'IMF-year': row.xpath('./td[3]/text()').get(),
                'WB-estimated-GDP': row.xpath('./td[4]/text()').get(),
                'WB-year': row.xpath('./td[5]/text()').get(),
                'UN-estimated-GDP': row.xpath('./td[6]/text()').get(),
                'UN-year': row.xpath('./td[7]/text()').get(),
            }

            if country_link:
                full_url = response.urljoin(country_link)
                yield response.follow(full_url, callback=self.parse_country_page, meta={'item': item})
            else:
                yield item

    def parse_country_page(self, response):
        item = response.meta['item']
        official_name = response.xpath('//table[contains(@class, "infobox")]//th[contains(text(), "Official")]/following-sibling::td//text()').get()
        
        if official_name:
            official_name = official_name.strip()

        item['official_name'] = official_name or "N/A"
        yield item
