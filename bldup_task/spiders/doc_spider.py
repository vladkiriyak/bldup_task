import scrapy
from scrapy import FormRequest

from bldup_task.spiders.form_data.deed_data import form_data, headers
from .utils import filter_empty, parse_description

from scrapy.http.response.html import HtmlResponse
from scrapy.selector.unified import SelectorList


class DocSpider(scrapy.spiders.Spider):
    name = 'doc_sp'
    start_urls = ['http://www.tauntondeeds.com/Searches/ImageSearch.aspx']

    def parse(self, response: HtmlResponse):
        yield FormRequest(
            self.start_urls[0],
            method='POST', formdata=form_data,
            headers=headers,
            callback=self.finish
        )

    @staticmethod
    def finish(response: HtmlResponse):
        table: SelectorList = response.xpath('//table[@id="ctl00_cphMainContent_gvSearchResults"]/tr')

        for i in range(2, 20):
            yield {
                'data': filter_empty(table[i].css("td")[1].css("::text").get()),
                'type': filter_empty(table[i].css("td")[2].css("::text").get()),
                'book': filter_empty(table[i].css("td")[3].css("::text").get()),
                'page_num': filter_empty(table[i].css("td")[4].css("::text").get()),
                'doc_num': filter_empty(table[i].css("td")[5].css("::text").get()),
                'city': filter_empty(table[i].css("td")[6].css("::text").get()),
                'description': filter_empty(table[i].css("span::text").get()),
                'cost': filter_empty(parse_description(table[i].css("span::text").get())['cost']),
                'street_address': filter_empty(parse_description(table[i].css("span::text").get())['street_address']),
            }
