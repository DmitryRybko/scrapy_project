import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem


class HhruSpider(scrapy.Spider):
    name = 'hhru'
    allowed_domains = ['hh.ru']
    start_urls = ['https://hh.ru/search/vacancy?area=1&search_field=name&search_field=company_name&search_field'
                  '=description&salary=580000&only_with_salary=true&text=python&order_by=relevance&search_period=0'
                  '&items_on_page=20&no_magic=true&L_save_area=true&customDomain=1',]

    # custom_settings = {}

    def parse(self, response: HtmlResponse):
        next_page = response.xpath("//a[@data-qa='pager-next']/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        links = response.xpath("//a[@data-qa='vacancy-serp__vacancy-title']/@href").getall()
        for link in links:
            yield response.follow(link, callback=self.vacancy_parse)

    def vacancy_parse(self, response: HtmlResponse):
        name = response.xpath("//h1//text()").get()
        salary = response.xpath("//div[@data-qa='vacancy-salary']/span/text()").getall()
        url = response.url
        yield JobparserItem(name=name, salary=salary, url=url)
