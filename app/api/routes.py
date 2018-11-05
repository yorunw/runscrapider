# -*-coding: utf8-*-

from . import api
from scrapy.crawler import CrawlerProcess, CrawlerRunner
from scrapy.utils.project import get_project_settings
from work.spiders.year_2018.month_9.date_13.test import TestSpider
from twisted.internet import reactor


def task():
    process = CrawlerProcess(get_project_settings())
    try:
        process.crawl(TestSpider)
        process.start()
    except:
        process.stop()


def task2():
    runner = CrawlerRunner()

    d = runner.crawl(TestSpider)
    # d.addBoth(lambda _: reactor.stop())
    reactor.run()


@api.route('/spider/run')
def run():
    # t = threading.Thread(target=task)
    # t.start()
    # t.join()

    # task()
    task2()

    return 'spider start'
