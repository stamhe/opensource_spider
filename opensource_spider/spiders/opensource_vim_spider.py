#!/usr/bin/python
#coding=utf-8
# @hequan

from scrapy.spiders import Spider, Rule
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor
import re
from scrapy.spiders import CrawlSpider

import sys
reload(sys)
sys.setdefaultencoding('utf8')

from opensource_spider.items import OpensourceSpiderItem

class opensource_vim_spider(CrawlSpider):
    # 爬虫的识别名称，必须是唯一的，在不同的爬虫中你必须定义不同的名字
    name = "vim_spider"    # 设置爬虫名称

    # 搜索的域名范围，也就是爬虫的约束区域，规定爬虫只爬取这个域名下的网页
    # http://ftp.vim.org/pub/vim/unix/
    allowed_domains = ["ftp.vim.org"] # 设置允许的域名

    # 爬取的url列表，爬虫从这里开始抓取数据，所以，第一次下载的数据将会从这些urls开始，其他子url将会从这些起始url中继承性生成
    start_urls = [
        'http://ftp.vim.org/pub/vim/unix/'
    ]

    # 解析的方法，调用的时候传入从每一个url传回的response对象作为唯一参数，负责解析并获取抓取的数据(解析为item)，跟踪更多的url
    def parse(self, response):
        #print "text = " , response.text
        #sel = Selector(response)
        items = []
        pt1 = re.compile(r'<a\shref="([\d\w.-]*)">(.*)</a>(\s*)([\d\w-]*)(\s*)([\d:]*)(\s*)')
        ret1 = re.findall(pt1, response.text)
        for v in ret1:
            item = OpensourceSpiderItem()
            item['orginname']   = v[0]
            item['downurl']     = response.url + v[0]
            item['filesize']    = 0
            items.append(item)

        return items


