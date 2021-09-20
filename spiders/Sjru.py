import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem


class SjruSpider(scrapy.Spider):
    name = 'superjobru'
    allowed_domains = ['superjob.ru']
    start_urls = ['https://russia.superjob.ru/vacancy/search/?keywords=python']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath(
            "//*/a[@class='icMQ_ bs_sM _3ze9n _2EmPY f-test-button-dalshe f-test-link-Dalshe']/@href").extract_first()
        # print(next_page)
        yield response.follow(next_page, callback=self.parse)

        vacansy = response.xpath("//*/div[@class='_1h3Zg _2rfUm _2hCDz _21a7u']/a/@href").extract()

        #for link in vacansy:
        #yield response.follow(link, callback=self.vacansy_parse)
        for i in range(0, 3):
            yield response.follow(vacansy[i], callback=self.vacansy_parse)

    def vacansy_parse(self, response: HtmlResponse):
        name = response.xpath("//*/h1[@class='_1h3Zg rFbjy _2dazi _2hCDz']/text()").extract_first()
        salary = response.xpath("//*/span[@class='_1h3Zg _2Wp8I _2rfUm _2hCDz']/text()").extract()
        sal_from = 0
        sal_to = 0
        salary = ' '.join(salary).replace('\xa0', '')
        #print(salary)
        if "договор" in salary:
            sal_from = "-"
            sal_to = "-"
        elif "до" in salary:
            sal_from = "-"
            sal_to = salary[salary.find("до") + 3:salary.find("руб")].replace(' ', '')
        elif "от" in salary:
            sal_from = salary[salary.find("от") + 3:salary.find("руб")].replace(' ', '')
            sal_to = "-"
        elif " " in salary:
            sal_from = salary[:salary.find(" ")].replace(' ', '')
            sal_to = salary[salary.find(" ") + 1:salary.find("руб") - 1].replace(' ', '')
        else:
            sal_from = salary
            sal_to = salary

        url = response.request.url
        site = 'superjob.ru'
        # print(name, salary)
        yield JobparserItem(name=name, sal_from=sal_from, sal_to=sal_to, url=url, site=site)
