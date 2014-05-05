# Scrapy settings for gommadiretto project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'gommadiretto'

SPIDER_MODULES = ['gommadiretto.spiders']
NEWSPIDER_MODULE = 'gommadiretto.spiders'

REDIRECT_MAX_TIMES = 3

COOKIES_ENABLED = False
AUTOTHROTTLE_ENABLED = True

CONCURRENT_REQUESTS = 600

RETRY_ENABLED = False
DOWNLOAD_TIMEOUT = 10
DOWNLOAD_DELAY = 0.50

#FEED_EXPORTERS ={'json': 'gommadiretto.pipelines.UnicodeJsonLinesItemExporter'}

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'gommadiretto (+http://www.yourdomain.com)'
DOWNLOADER_MIDDLEWARES = {
        'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware' : None,
        'gommadiretto.rotate_useragent.RotateUserAgentMiddleware' :400
}

#ITEM_PIPELINES = {'scrapy.contrib.pipeline.images.ImagesPipeline': 1}
ITEM_PIPELINES = {'scrapy.contrib.pipeline.images.ImagesPipeline': 1,
				  'gommadiretto.pipelines.GommadirettoPipeline': 2}
IMAGES_STORE = 'images/'
#IMAGES_EXPIRES = 90
IMAGES_THUMBS = {
    'small': (50, 50),
    'big': (270, 270),
}