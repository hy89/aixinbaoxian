# -*- coding: utf-8 -*-
import logging
import re
import scrapy
from copy import deepcopy
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError, TCPTimedOutError
from baoxian.items import BaoxianItem

logger = logging.getLogger(__name__)


class AgentSpider(scrapy.Spider):
    name = "agent"
    allowed_domains = ["axbxw.com"]
    start_urls = ['http://m.axbxw.com/agent/']
    first_url = 'http://m.axbxw.com/case.php?p={}&proid={}&t=moreagent'
    pattern = re.compile(r'.*sf(\d+).*')

    def parse(self, response):
        """响应中包含所有的省市信息，提取有效信息"""
        a_list = response.xpath('//div[@id="sort-third"]/ul/li/ul/li[1]/a')  # 包含所有省的a标签
        for a in a_list:
            item = BaoxianItem()
            # 从a标签中提取出省信息
            province = a.xpath('./text()').extract_first()
            item['province'] = province.replace('(全部)', '') if province else None
            # 提取出href以及sf后的数字（用于请求人员信息时的proid参数）
            href = a.xpath('./@href').extract_first()  # /agent/sf1-cs1-gs
            ret = self.pattern.search(href)
            if ret:
                proid = ret.group(1)
                page = 1
                url = self.first_url.format(page, proid)
                yield scrapy.Request(
                    url=url,
                    callback=self.crawl_info,
                    meta={'item': item, 'page': page, 'proid': proid},  # 仅保存有省份信息
                    errback=self.parse_err,
                )
            else:
                logger.warning('省份信息无法获取')
                # break

    def crawl_info(self, response):
        """从响应中提取信息，同时递归请求下一页，另外发送详情页请求"""
        item = response.meta.get('item')
        # if response.text != "":  # 空字符串，说明正好最后一页有五条信息，然后没了这里就不再执行
        li_list = response.xpath('//li')
        item['info_url'] = response.url
        for li in li_list:
            item = deepcopy(item)  # 这里遍历的是每个人的信息，因此每个人一个item
            h3 = li.xpath('.//h3/text()').extract_first()
            name_position = h3.strip().split(' ', maxsplit=1)
            if len(name_position) == 2:
                item['name'], item['position'] = name_position[0], name_position[1]
            else:
                item['name'], item['position'] = name_position[0], None

            item['phone'] = li.xpath('.//em[@class="mobile"]/text()').extract_first()

            span = li.xpath('.//a/p[1]/span/text()').extract_first()
            city_company = span.strip().split(' ', maxsplit=1)
            if len(city_company) == 2:
                item['city'], item['company'] = city_company[0], city_company[1]
            else:
                item['city'], item['company'] = city_company[0], None

            href = li.xpath('./a/@href').extract_first()  # 得到的是完整url
            yield scrapy.Request(
                url=href,
                callback=self.crawl_code,
                meta={'item': item},
                errback=self.parse_err,
            )
            # break  # 一个人
        # 翻页处理
        page = response.meta.get('page')
        proid = response.meta.get('proid')

        if len(li_list) == 5:  # 小于5条，没有下一页
            page += 1
            url = self.first_url.format(page, proid)
            yield scrapy.Request(
                url=url,
                callback=self.crawl_info,
                meta={'item': item, 'page': page, 'proid': proid},  # 仅保存有省份信息
                errback=self.parse_err,
            )
        else:
            logger.warning('没有下一页了--%s' % response.url)  # 有可能此url打开是空字符串，因为上一页就是最后一页了

    def crawl_code(self, response):
        """获取资格代码"""
        item = response.meta.get('item')  # 针对每个人的item
        # 有可能重定向
        code_before = response.xpath('//div[@class="f14 fgray2"]/div[2]/text()').extract_first()
        if len(response.url) > 19:
            item['code_url'] = response.url
        else:
            item['code_url'] = None  # 表示重定向了
        if code_before:
            code_split = code_before.split('：')
            if len(code_split) == 2:
                item['code'] = code_split[1]  # 可能是空字符串,也可能是null字符串,也可能是存在真实的
            else:
                item['code'] = None
            yield item
        else:
            # 说明这个人的信息点击后重定向到了首页,所以就没有资格证号,直接yield
            item['code'] = None
            logger.warning('被重定向了--%s' % ('*' * 30))
            yield item
        print(item)

    def parse_err(self, failure):
        """处理非正常请求"""
        self.logger.error(repr(failure))
        if failure.check(HttpError):
            response = failure.value.response
            logger.error(
                'HttpError on %s' % response.url)  # HttpError on https://3g.ganji.com/zz_jzchuandanpaifa/2984061273x?ifid=seo_company_detail

        elif failure.check(DNSLookupError):
            request = failure.request
            logger.error('DNSLookupError on %s' % request.url)

        elif failure.check(TimeoutError, TCPTimedOutError):
            request = failure.request
            logger.error('TimeoutError on %s' % request.url)
