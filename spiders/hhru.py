# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem


class HhruSpider(scrapy.Spider):
    name = 'hhru'
    allowed_domains = ['hh.ru']
    start_urls = ['https://hh.ru/search/vacancy?area=&st=searchVacancy&text=python']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath("//*/a[@data-qa='pager-next']/@href").extract_first()
        #print(next_page)
        yield response.follow(next_page, callback=self.parse)

        vacansy = response.css(
            'div.vacancy-serp div.vacancy-serp-item div.vacancy-serp-item__row_header a.bloko-link::attr(href)').extract()

        #for link in vacansy:
        #    yield response.follow(link, callback=self.vacansy_parse)
        for i in range(0, 3):
            yield response.follow(vacansy[i], callback=self.vacansy_parse)

    def vacansy_parse(self, response: HtmlResponse):
        name = response.xpath("//*/div/div/h1/text()").extract_first()
        salary = response.xpath("//*/p/span[@class='bloko-header-2 bloko-header-2_lite']/text()").extract_first()
        sal_from = 0
        sal_to = 0

        if "договор" in salary:
            sal_from = '-'
            sal_to = '-'
        elif ("от" in salary) and ("до" in salary):
            sal_from = salary[3:salary.find("до")].replace('\xa0', '')
            sal_to = salary[salary.find("до") + 3:salary.find("руб") - 1].replace('\xa0', '')
        elif "до" in salary:
            sal_from = '-'
            sal_to = salary[salary.find("до") + 3:salary.find("руб") - 1].replace('\xa0', '')
        elif "от" in salary:
            sal_from = salary[salary.find("от") + 3:salary.find("руб") - 1].replace('\xa0', '')
            sal_to = '-'
        url = response.request.url;
        site = 'hh.ru';
        # print(name, salary)
        yield JobparserItem(name=name, sal_from=sal_from, sal_to=sal_to, url=url, site=site)
