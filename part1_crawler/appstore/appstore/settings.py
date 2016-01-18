# -*- coding: utf-8 -*-

# Scrapy settings for appstore project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'appstore'

SPIDER_MODULES = ['appstore.spiders']
NEWSPIDER_MODULE = 'appstore.spiders'

ITEM_PIPELINES = {
   'appstore.pipelines.AppstorePipeline': 300,
}
DOWNLOAD_DELAY=5

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'appstore (+http://www.yourdomain.com)'
