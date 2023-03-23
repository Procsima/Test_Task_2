import scrapy
from newspaper import Article
import playwright


class TestSpider(scrapy.Spider):
    name = "test"
    start_urls = [
        'https://moxie.foxnews.com/google-publisher/latest.xml'
    ]
    flag = False

    def parse(self, response):
        request = scrapy.Request('http://www.example.com/index.html',
                                 callback=self.parse_page2,
                                 cb_kwargs=dict(main_url=response.url))
        request.cb_kwargs['foo'] = 'bar'  # add more arguments for the callback
        yield request
        yield dict(
            text='hello'
        )

    def parse_page2(self, response, main_url, foo):
        yield dict(
            main_url=main_url,
            other_url=response.url,
            foo=foo,
        )
