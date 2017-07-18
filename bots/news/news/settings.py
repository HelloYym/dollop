# -*- coding: utf-8 -*-

# Scrapy settings for news project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html


from bots import setup_django_env
setup_django_env()

BOT_NAME = 'news'

SPIDER_MODULES = ['news.spiders']
NEWSPIDER_MODULE = 'news.spiders'

#####WEBAPP的绝对路径名，爬下来的图片和文件要放在其中

#WEBAPP_ABSOLUTE_PATH_SERVER='/home/apache-tomcat-7.0.63/webapps/businessfbi/WEB-INF/'

#WEBAPP_ABSOLUTE_PATH_SERVER='/home/JustForNewsImages/'
#WEBAPP_ABSOLUTE_PATH_LOCAL='/Users/ousen/news/'

#WEBAPP_IMAGEPATH_SERVER=WEBAPP_ABSOLUTE_PATH_SERVER+'static/image/'
#WEBAPP_IMAGEPATH_LOCAL=WEBAPP_ABSOLUTE_PATH_LOCAL+'static/image/'

#底下这个路径要新建，每次部署的时候要注意
#WEBAPP_IMAGE_DOWNLOADPATH_SERVER=WEBAPP_IMAGEPATH_SERVER+"newsimages/"
#WEBAPP_IMAGE_DOWNLOADPATH_LOCAL=WEBAPP_IMAGEPATH_LOCAL+"newsimages/"
WEBAPP_IMAGE_DOWNLOADPATHS={
	"aliyun":"/mnt/JustForNewsImages/",
	"test":"/Users/ousen/news/static/image/newsimages/",
	"server":"/home/apache-tomcat-7.0.63/webapps/businessfbi/WEB-INF/static/images/newsimages",
	"aliyunrds":"/mnt/JustForNewsImages/"
}

'''注意，如果在settings.py内有语法错误，则scrapyd上传时也会提示syntax error
如
WEBAPP_IMAGE_DOWNLOADPATHS={
	"aliyun":"/home/JustForNewsImages/",
	"test":"/Users/ousen/news/static/newsimages/",
	"server":"/home/apache-tomcat-7.0.63/webapps/businessfbi/WEB-INF/static/images/newsimages"
}
若写成
WEBAPP_IMAGE_DOWNLOADPATHS=
{ #不应换行，左花括号应该写到上面一行
	"aliyun":"/home/JustForNewsImages/",
	"test":"/Users/ousen/news/static/newsimages/",
	"server":"/home/apache-tomcat-7.0.63/webapps/businessfbi/WEB-INF/static/images/newsimages"
}

'''

WEBAPP_IMAGE_PATH_PREFIX_IN_HTML='/businessfbi/static/images/newsimages/'

START_DATE="2016-12-01"
##############


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'news (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'news.middlewares.MyCustomSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'news.middlewares.MyCustomDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    #'news.pipelines.NewsPipeline': 300,
    'news.pipelines.CacheFileExporterPersistencePipeline':300,
    'news.pipelines.UniqueItemPersistencePipeline':300
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'


##############

DEFAULT_ON_WHICH="aliyunrds"

serverDBParams={
	"addr":"10.214.192.66",
	"username":"root",
	"password":"zju302",
	"dbname":"business"
}

testDBParams={
	"addr":"localhost",
	"username":"root",
	"password":"",
	"dbname":"businessfbi"
}

aliyunDBParams={
	"addr":"localhost",
	"username":"root",
	"password":"Zju302hz",
	"dbname":"jinzhita_spider"
}

aliyunRemoteTestDBParams={
	"addr":"121.40.156.206",
	"username":"root",
	"password":"Zju302hz",
	"dbname":"forTest"
}

aliyunRDSDBParams={
	"addr":"rm-bp18kezd2z20ro156.mysql.rds.aliyuncs.com",
	"username":"spider",
	"password":"Zju302hz",
	"dbname":"jinzhita_spider"
}

serverTableNames={
	"paycircle_news":"paycircle_news_v2",
	"jrzj_news":"jrzj_news_v2",
	"weiyang_news":"weiyang_news_v2",
	"wdzj_news":"wdzj_news_v2",
	"wdzj_archive":"wdzj_archive_v2",
	"wdzj_features":"wdzj_features_v2",
	"wdzj_navigation":"wdzj_navigation",
	"weiyang_report":"weiyang_report"
}

aliyunTableNames={
	"paycircle_news":"paycircle_news",
	"jrzj_news":"jrzj_news",
	"weiyang_news":"weiyang_news",
	"wdzj_news":"wdzj_news",
	"wdzj_archive":"wdzj_archive",
	"wdzj_features":"wdzj_features",
	"wdzj_navigation":"wdzj_navigation",
	"weiyang_report":"weiyang_report"
}

aliyunRemoteTestTableNames={
	"paycircle_news":"paycircle_news",
	"jrzj_news":"jrzj_news",
	"weiyang_news":"weiyang_news",
	"wdzj_news":"wdzj_news",
	"wdzj_archive":"wdzj_archive",
	"wdzj_features":"wdzj_features",
	"wdzj_navigation":"wdzj_navigation",
	"weiyang_report":"weiyang_report"
}

aliyunRDSTableNames={
	"paycircle_news":"paycircle_news",
	"jrzj_news":"jrzj_news",
	"weiyang_news":"weiyang_news",
	"wdzj_news":"wdzj_news",
	"wdzj_archive":"wdzj_archive",
	"wdzj_features":"wdzj_features",
	"wdzj_navigation":"wdzj_navigation",
	"weiyang_report":"weiyang_report"
}

testTableNames={
	"paycircle_news":"paycircle_news",
	"jrzj_news":"jrzj_news",
	"weiyang_news":"weiyang_news",
	"wdzj_news":"wdzj_news",
	"wdzj_archive":"wdzj_archive",
	"wdzj_features":"wdzj_features",
	"wdzj_navigation":"wdzj_navigation",
	"weiyang_report":"weiyang_report"
}

INSERT_OR_REPLACE={
	"paycircle_news":"INSERT",
	"jrzj_news":"INSERT",
	"weiyang_news":"INSERT",
	"wdzj_news":"INSERT",
	"wdzj_archive":"REPLACE",
	"wdzj_features":"REPLACE",
	"wdzj_navigation":"REPLACE",
	"weiyang_report":"INSERT"
}

allTableNames={"aliyunrds":aliyunRDSTableNames,"test":testTableNames,"aliyun":aliyunTableNames,"aliyun_remote":aliyunRemoteTestTableNames,"server":serverTableNames}
allDBParams={"aliyunrds":aliyunRDSDBParams,"test":testDBParams,"aliyun":aliyunDBParams,"aliyun_remote":aliyunRemoteTestDBParams,"server":serverDBParams}
