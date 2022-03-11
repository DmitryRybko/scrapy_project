import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem


class SuperjobSpider(scrapy.Spider):
    name = 'superjob'
    allowed_domains = ['www.superjob.ru']
    start_urls = ['https://www.superjob.ru/vacancy/search/?keywords=python&geo%5Bt%5D%5B0%5D=4&click_from=facet']

    # custom_settings = {}

    def parse(self, response: HtmlResponse):
        next_page = response.xpath("//a[@data-qa='pager-next']/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        vacancies = response.xpath("//div[contains(@class, 'vacancy-item')]")
        for vacancy in vacancies:
            name = vacancy.xpath(".//a/text()").get()
            salary = vacancy.xpath(".//span[contains(@class, 'item-salary')]//span[1]/text()").getall()
            print(salary)
            url = vacancy.xpath(".//a/@href").get()
            yield JobparserItem(name=name, salary=salary, url=url)
