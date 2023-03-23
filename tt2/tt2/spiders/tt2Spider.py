import scrapy
from newspaper import Article, ArticleException
from ..items import ArticleItem
import nltk
import json

nltk.download('punkt')


class tt2Spider(scrapy.Spider):
    name = "tt2"
    start_urls = [
        'https://moxie.foxnews.com/google-publisher/latest.xml'
    ]
    flag = False
    r_art = Article('')
    art_item = ArticleItem()

    def compare(self, response, art2: Article):
        art = Article('')
        art.download(response.text)
        art.parse()
        art.nlp()
        self.flag = True if len(art.title) > len(art2.title) or len(art.authors) > len(art2.authors) or len(art.summary) > len(
            art2.summary) or len(art.text) > len(art2.text) or len(art.images) > len(art2.images) else False
        # yield {'need_render': self.flag}

        json_object = json.dumps({'need_render': self.flag}, indent=4)
        with open("source_state.json", "w") as outfile:
            outfile.write(json_object)

        # yield {'titles': [art.title, art2.title], 'authors': [art.authors, art2.authors],
        #        'summaries': [art.summary, art2.summary], 'images': [art.images, art2.images]}

    def hbreq(self, response):
        self.r_art = Article('')
        self.r_art.download(response.text)
        self.r_art.parse()
        self.r_art.nlp()

    def parse(self, response):
        items = response.css('item')
        links = []
        for item in items:
            link = item.css('guid::text').extract_first()
            links.append(link)

        # check link => set flag
        art = Article(links[0])
        art.download()
        art.parse()
        art.nlp()

        req = scrapy.Request(links[0], meta={'playwright': True}, callback=self.compare, headers={
            'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'})
        req.cb_kwargs['art2'] = art
        yield req

        for link in links:
            if self.flag:
                req = scrapy.Request(link, meta={'playwright': True}, callback=self.hbreq, headers={
                    'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'})
                yield req
            else:
                self.r_art = Article(link)
                self.r_art.download()
                self.r_art.parse()
                self.r_art.nlp()
            self.art_item['title'] = self.r_art.title
            self.art_item['authors'] = self.r_art.authors
            self.art_item['summary'] = self.r_art.summary
            self.art_item['text'] = self.r_art.text
            self.art_item['images'] = self.r_art.images
            yield self.art_item
