# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
from qiita_collect.items import QiitaCollectItem


class Bs4Parser(object):
    def __init__(self, html):
        self._soup = BeautifulSoup(html, 'html.parser')

    def parse_posts(self):
        class_name = 'searchResult_itemTitle'
        return self._soup.find_all('h1', attrs={'class': class_name})

    def parse_postTitle(self, post):
        return post.a.get_text(strip=True)

    def parse_postUrl(self, post):
        return post.a.get('href')


class CollectPostSpider(scrapy.Spider):
    name = 'collect_post'
    allowed_domains = ['qiita.com']

    def __init__(self, query='', *args, **kwargs):
        super(CollectPostSpider, self).__init__(*args, **kwargs)
        self.query = query
        self.start_urls = ['https://qiita.com/search?q={}'.format(self.query)]

    def parse(self, response):
        parser = Bs4Parser(response.text)

        for post in parser.parse_posts():
            yield QiitaCollectItem(
                keyword=self.query,
                title=parser.parse_postTitle(post),
                url=response.urljoin(parser.parse_postUrl(post)),
            )

        next_page_link = response.css(
            '.js-next-page-link::attr(href)').extract_first()
        if next_page_link is None:
            return

        next_page_link = response.urljoin(next_page_link)
        yield scrapy.Request(next_page_link, callback=self.parse)
