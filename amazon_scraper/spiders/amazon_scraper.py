import scrapy
from ..items import Mobile

class AmazonScraper(scrapy.Spider):
    name = "amazon_scraper"

    # How many pages you want to scrape
    no_of_pages = 1

    # Headers to fix 503 service unavailable error
    # Spoof headers to force servers to think that request coming from browser ;)
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.2840.71 Safari/539.36'}

    def start_requests(self):
        # starting urls for scraping
        urls = ["https://www.amazon.sg/s?k=baby+%26+kids&ref=nb_sb_noss_2"]

        for url in urls: yield scrapy.Request(url = url, callback = self.parse, headers = self.headers)

    def parse(self, response):

        self.no_of_pages -= 1

        # print(response.text)

        mobiles = response.xpath("//a[@class='a-link-normal a-text-normal']").xpath("@href").getall()
        
        # print(len(mobiles))

        for mobile in mobiles:
            final_url = response.urljoin(mobile)
            yield scrapy.Request(url=final_url, callback = self.parse_mobile, headers = self.headers)
            # break
            # print(final_url)

        # print(response.body)
        # title = response.xpath("//span[@class='a-size-medium a-color-base a-text-normal']//text()").getall()
        # title = response.css('span').getall()
        # print(title)
        
        if(self.no_of_pages > 0):
            next_page_url = response.xpath("//ul[@class='a-pagination']/li[@class='a-last']/a").xpath("@href").get()
            final_url = response.urljoin(next_page_url)
            yield scrapy.Request(url = final_url, callback = self.parse, headers = self.headers)

    def parse_mobile(self, response):
        title = response.xpath("//span[@id='productTitle']//text()").get() or response.xpath("//h1[@id='title']//text()").get()

        print(title)

        yield Mobile(title = title.strip())
