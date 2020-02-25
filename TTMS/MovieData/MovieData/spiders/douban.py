# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request

from MovieData.items import MoviedataItem


class DoubanSpider(scrapy.Spider):
    name = 'douban'
    allowed_domains = ['movie.douban.com']
    start_urls = ['https://movie.douban.com/cinema/nowplaying/118378/']
    headers = {
        'User-Agent': "Mozilla/5.0 (iPad; CPU OS 5_0 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9A334 Safari/7534.48.3"
    }

    def start_requests(self):
        yield Request(self.start_urls[0], headers=self.headers)


    def parse(self, response):
        # movie = MoviedataItem()
        movieDetails = response.xpath('//li[@class="list-item"]')
        # print(movieDetails)
        for movieDetail in movieDetails:
            movie = MoviedataItem()
            url = movieDetail.xpath('./ul/li[@class="poster"]/a/@href')[0].extract()
            # name = movieDetail.xpath('./ul/li[2]/a/text()').extract_first().strip()
            score = movieDetail.xpath('./ul/li[3]/span[2]/text()').extract_first()
            img = movieDetail.xpath('./ul/li[1]/a/img/@src').extract_first()
            # print(score,img,'--------')

            movie['score'] = score
            movie['img'] = img
            yield scrapy.Request(url, meta={'item': movie}, callback=self.parse_movie)

    def parse_movie(self, response):
        movie = response.request.meta['item']
        director = response.xpath('//div[@class="article"]//div[@id="info"]/span[1]/span[2]/a/text()').extract()
        actor = response.xpath('//div[@class="article"]//div[@id="info"]/span[3]/span[2]/a/text()').extract()
        area = response.xpath('//div[@class="article"]//div[@id="info"]').re(r'</span> (.*)<br>\n')[1]
        type = response.xpath('//div[@class="article"]//div[@id="info"]/span[@property="v:genre"]/text()').extract()

        release_time = response.xpath('//div[@class="article"]//div[@id="info"]/span[@property="v:initialReleaseDate"][1]/text()').extract_first()
        length = response.xpath('//div[@class="article"]//div[@id="info"]/span[@property="v:runtime"]/text()').extract_first()
        # cover_link = response.xpath('//div[@class="article"]//div[@id="mainpic"]//img/@src').extract_first()
        summary = response.xpath('//div[@class="article"]//div[@id="link-report"]/span[1]/text()').extract_first().strip()
        name = response.xpath('//span[@property="v:itemreviewed"]/text()').extract_first()
        movie['director'] = director
        movie['name'] = name
        movie['actor'] = actor
        movie['area'] = area
        movie['type'] = type
        movie['release_date'] = release_time
        movie['length'] = length
        movie['brief'] = summary
        # print(director,actor,area,type,release_time,length,summary, '=======')
        yield movie
