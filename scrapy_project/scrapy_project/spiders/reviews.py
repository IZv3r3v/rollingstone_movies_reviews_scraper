import scrapy
from scrapy.loader import ItemLoader
from scrapy_project.items import ReviewItem

class ReviewsSpider(scrapy.Spider):
    name = 'reviews'
    allowed_domains = ['rollingstone.com']

    def start_requests(self):
        yield scrapy.Request(url='http://www.rollingstone.com/movies/reviews', callback=self.parse_index)

    # Parser for index pages. e.g. http://www.rollingstone.com/movies/reviews?page=2
    def parse_index(self, response):
        # get other index pages
        index_urls = response.css('section.pagination a::attr(href)').extract()
        index_urls = [response.urljoin(u) for u in index_urls]
        for url in index_urls:
            yield scrapy.Request(url=url, callback=self.parse_index)
        # get articles pages
        articles_urls = response.css('section.hub-content-feed article.content-card a.content-card-link::attr(href)').extract()
        articles_urls = [response.urljoin(u) for u in articles_urls]
        for url in articles_urls:
            yield scrapy.Request(url=url, callback=self.parse_article)

    # Parser for articles pages. e.g. http://www.rollingstone.com/movies/reviews/peter-travers-logan-movie-review-w469327
    def parse_article(self, response):
        loader = ItemLoader(item=ReviewItem(), response=response)
        loader.add_css('title', 'article.article-main h1.content-title')
        loader.add_xpath('content', '//article[@class="article-main"]//div[@class="article-content"]/p')
        loader.add_css('date', 'article.article-main div.content-info time.content-published-date')
        item = loader.load_item()
        return item
