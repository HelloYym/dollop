Spiders Framework Focus on Internet Finance
=======


## Description

* Used to crawl specific internet finance infomation related from thrid-party platforms.
* Offer raw data supports to [LAB Internet Finance Platform Demo](http://10.214.192.66:8080/businessfbi_id/index/home).
* Cover ['wangdaizhijia'](http://www.wdzj.com/), ['p2peye'](http://www.p2peye.com/), ['weidai'](https://www.weidai.com.cn/), ['yirendai'](https://www.yirendai.com/), ['renrendai'](http://www.we.com/), ['baidu_apistore'](http://apistore.baidu.com.cn/astore/index), 'AIF' data sources now.
* Mainly includes `stalk` and `bots` supporting as db adapter and spider entities.
* Called `blotus`, which can be explained as __Blue Lotus__. ;)

## Installation

1. Install python-django 1.9.0. [Here](https://docs.djangoproject.com) is official docs.
2. Install python-scrapy 1.0.3. [Here](http://doc.scrapy.org)  is official docs.
3. Install scrapyd 1.1.0. [Here](https://scrapyd.readthedocs.org) is official docs. 
4. Clone the code repository.
5. DB configuration and synchronization.
	* Modify DB related settings in `/path/to/blotus/core/settings.py`.
	* Accessing into `/path/to/blotus/` directory and run `python manage.py migrate`.
6. Set bash variables. Add `export PYTHONPATH=path/to/blotus` to `~/.profile` or else.
7. Set scrapyd configuration. Add following snippets to `~/.scrapyd.conf`.
```python
    [services]
    persistjobs.json     = utils.webservice.PersistJobs
    listdbjobs.json      = utils.webservice.ListDBJobs
```

## Directions

### About `'news'` Bot

1.  Spider for news from weiyangx.com

		Entry: wq_spiders/spiders/weiyang.py

		Description: Crawl news from weiyangx.com

		URL Reference:
			'http://www.weiyangx.com/category/tranditional-financial-institution',
        	'http://www.weiyangx.com/category/based-on-internet',
        	'http://www.weiyangx.com/category/new-modes',
        	'http://www.weiyangx.com/category/financial-information-service',
        	'http://www.weiyangx.com/category/internet-economy',
        	'http://www.weiyangx.com/category/macroscopic-monetary',
        	'http://www.weiyangx.com/category/investment-and-financing',
        	'http://www.weiyangx.com/category/block-chain'

		Parameters: 
			from_date(optional): a yyyy-mm-dd format string. If not specified, the default value will be "2016-12-01"

			to_date(optional): a yyyy-mm-dd format string. If not specified, the default value will be "2099-12-31"

			top_page_count(optional): a positive natural number, passed in as a string. If not specified, the default value will be "5"

		Rules:
			For each category of news, only the top_page_count pages will be checked.
			In the checked top_page_count pages of news, ONLY those whose date satisfies that from_date<=date<=to_date will be crawled.
			To reduce the running time, the default value of top_page_count is set to be 5, a experimental value, which I think matches the requirement to run it daily. If you forget to run it for a period, it is recommended to set top_page_count to a larger number.

2.  Spider for news from jrzj.com

		Entry: wq_spiders/spiders/jrzj.py

		Description: Crawl news from jrzj.com

		URL Reference:
			'http://www.jrzj.com/global/',
        	'http://www.jrzj.com/fund/',
        	'http://www.jrzj.com/p2p/',
        	'http://www.jrzj.com/insurance/',
        	'http://www.jrzj.com/vcpe/',
        	'http://www.jrzj.com/zhongchou/'


		Parameters: 
			from_date(optional): a yyyy-mm-dd format string. If not specified, the default value will be "2016-12-01"

			to_date(optional): a yyyy-mm-dd format string. If not specified, the default value will be "2099-12-31"

			top_page_count(optional): a positive natural number, passed in as a string. If not specified, the default value will be "10"

		Rules:
			For each category of news, only the top_page_count pages will be checked.
			In the checked top_page_count pages of news, ONLY those whose date satisfies that from_date<=date<=to_date will be crawled.
			To reduce the running time, the default value of top_page_count is set to be 10, a experimental value, which I think matches the requirement to run it daily. If you forget to run it for a period, it is recommended to set top_page_count to a larger number.

3.  Spider for news from paycircle.cn

		Entry: wq_spiders/spiders/paycircle.py

		Description: Crawl news from paycircle.cn

		URL Reference:
			'http://www.paycircle.cn/news/guoneizixun/1.html',


		Parameters: 
			from_date(optional): a yyyy-mm-dd format string. If not specified, the default value will be "2016-12-01"

			to_date(optional): a yyyy-mm-dd format string. If not specified, the default value will be "2099-12-31"

			top_page_count(optional): a positive natural number, passed in as a string. If not specified, the default value will be "5"

		Rules:
			For each category of news, only the top_page_count pages will be checked.
			In the checked top_page_count pages of news, ONLY those whose date satisfies that from_date<=date<=to_date will be crawled.
			To reduce the running time, the default value of top_page_count is set to be 5, a experimental value, which I think matches the requirement to run it daily. If you forget to run it for a period, it is recommended to set top_page_count to a larger number.

4.  Spider for reports from weiyangx.com

		Entry: wq_spiders/spiders/weiyang_report.py

		Description: Crawl reports from weiyangx.com

		URL Reference:
			'http://www.weiyangx.com/category/report',
        	'http://www.weiyangx.com/category/research'

		Parameters:
			top_page_count(optional): a positive natural number, passed in as a string. If not specified, the default value will be "5"

		Rules:
			For each category of report, only the top_page_count pages will be checked.
			To reduce the running time, the default value of top_page_count is set to be 5, a experimental value, which I think matches the requirement to run it daily or weekly. 

5.  Spider for detailed infomation of p2p platforms from wdzj.com

		Entry: wq_spiders/spiders/wdzj.py

		Description: Crawl detailed information of p2p platforms from wdzj.com

		URL Reference:
			'http://www.wdzj.com/wdzj/html/json/dangan_search.json'

		Parameters:
			None

6.  Spider for navigating infomation of p2p platforms from wdzj.com

		Entry: wq_spiders/spiders/wdzj_navigation.py

		Description: Crawl navigating information of p2p platforms from wdzj.com

		URL Reference:
			'http://www.wdzj.com/wdzj/html/json/dangan_search.json'

		Parameters:
			None

7.  Spider for feature infomation of p2p platforms from wdzj.com

		Entry: wq_spiders/spiders/wdzj_features.py

		Description: Crawl feature information of p2p platforms from wdzj.com.

		URL Reference:
			'http://www.wdzj.com/wdzj/html/json/dangan_search.json'

		Parameters:
			None


### About `'wangdaizhijia'` Bot

1.  Spider for navigation info

		Entry: wangjia/spiders/daohang.py

		Description: Get Navigation Info.

		URL Reference:
			1. http://www.wdzj.com/wdzj/html/json/nav_search.json
			2. http://www.wdzj.com/wdzj/html/json/dangan_search.json
			3. http://www.wdzj.com/front_navigation-query
			4. http://www.wdzj.com/daohang.html

		Parameters: None

2.  Spider for archive info

		Entry: wangjia/spiders/dangan.py

		Description: Get Plat Archive Info According To IDs FROM 'wangjia_navigation' Table.

		URL Reference: http://www.wdzj.com/dangan/{plat_pin}

		Parameters:
			from_id: Starting Plat ID
			to_id: Ending Plat ID

		Prerequisites:
			Completed job about navigation and make sure 'from_id' & 'to_id' in the range.

3.  Spider for problem plats info from data page

		Entry: wangjia/spiders/wenti.py

		Description: Get Problem Plat Info.

		URL Reference: http://shuju.wdzj.com/problem-1.html

		Parameters: None

4.  Spider for problem plats info from navigation page

		Entry: wangjia/wangjia/spiders/wenti2.py

		Description: Get Problem Plat Info.

		URL Reference: http://www.wdzj.com/daohang.html

		Parameters: None

5.  Spider for rating info from rating page

		Entry: wangjia/spiders/pingji.py

		Description: Get Rating Info For Specific Month. (page_id='' means current month)

		URL Reference: http://www.wdzj.com/pingji{page_id}.html

		Parameters:
			page_id: Page ID In URL
			timestamp: Corresponding Month Timestamp (FORMAT: yyyymm)

6.  Spider for rating info from archive page

		Entry: wangjia/spiders/pingji2.py

		Description: Get Rating Info According To URLs From Rating Page.

		URL Reference: http://www.wdzj.com/dangan/{plat_pin}

		Parameters:
			timestamp: Timestamp To Record
			cache: path to URL 'cache' file

		Prerequisites:
			Completed 'exporterHelper' job for getting cached rating urls. See more at entry 'exporterHelper/spiders/wangjia_rating_list.py'.

7.  Spider for data info

		Entry: wangjia/spiders/shuju.py

		Description: Get Data Info.

		URL Reference: http://shuju.wdzj.com/platdata-1.html

		Parameters:
			from_date: Starting Date (FORMAT: yyyymmdd)
			to_date: Ending Date (FORMAT: yyyymmdd)

8.  Spider for news info

		Entry: wangjia/spiders/xinwen.py

		Description: Get News Info.

		URL Reference: http://www.wdzj.com/news/category/yyyy.html

		Parameters:
			cache: path to URL 'cache' file

		Prerequisites:
			Completed 'exporterHelper' job for getting cached news urls. See more at entry 'exporterHelper/spiders/wangjia_news_list.py'.

9.  Spider for exposure info

		Entry: wangjia/spiders/baoguang.py

		Description: Get Exposure Info.

		URL Reference: http://bbs.wdzj.com/thread-xxxx-y-z.html

		Parameters:
			cache: path to URL 'cache' file

		Prerequisites:
			Completed 'exporterHelper' job for getting cached exposure urls. See more at entry 'exporterHelper/spiders/wangjia_exposure_list.py'.

10.	Spider for feature info(deprecated)

		Entry: wangjia/spiders/tedian.py

		Description: Get Plat Feature Info According To IDs From 'wangjia_navigation' Table.

		URL Reference: http://www.wdzj.com/dangan/{plat_pin}

		Parameters:
			from_id: Starting Plat ID
			to_id: Ending Plat ID

		Prerequisites:
			Completed job about navigation and make sure 'from_id' & 'to_id' in the range.

### About `'p2peye'` Bot
1. Spider for plat feature info

        Entry: p2peye/spiders/biaoqian.py

        Description: Get Feature Info.

		URL Reference:
		    http://licai.p2peye.com/search/
		    http://licai.p2peye.com/search/z0b0r0c0x0y0t0m0q0s0p{page_id}.html

		Parameters:
		    from_id: Starting Page ID
			to_id: Ending Page ID

### About `'weidai'` Bot(deprecated)

1.  Spider for tender info

		Entry: weidai/spiders/toubiao.py

		Description: Get Tender List Info.

		URL Reference: https://www.weidai.com.cn/bid/tenderList?searchFlag=search&typeCondition={bid_type}&page={page_id}&credit={credit}

		Parameters:
			bid_type: Bid Type
			credit: Credit Bid Or Not ('2' for yes)
			start_page_id: Starting Page ID
			end_page_id: Ending Page Id

2.  Spider for bid info

		Entry: weidai/spiders/biaodi.py

		Description: Get Bid Info According To IDs FROM 'weidai_tender' Table.

		URL Reference: https://www.weidai.com.cn/bid/showBorrowDetail?bid={bid}

		Parameters:
			from_id: Starting Bid ID
			to_id: Ending Bid ID

		Prerequisites:
			Completed job about tender list and make sure 'from_id' & 'to_id' in the range.

3.  Spider for bidder info from bid detail page

		Entry: weidai/spiders/biaoren.py

		Description: Get Bidder Info.

		URL Reference: https://www.weidai.com.cn/bid/tenderListPage?page=1&rows=100&bid={bid}

		Parameters:
			from_id: Starting Bid ID
			to_id: Ending Bid ID

		Prerequisites:
			Completed job about tender list and make sure 'from_id' & 'to_id' in the range.

### About `'yirendai'` Bot(deprecated)

1.  Spider for yirendai tender info

		Entry: yirendai/spiders/toubiao.py

		Description: Get Yirendai Tender List Info.

		URL Reference: http://www.yirendai.com/loan/list/{page_id}

		Parameters:
			from_page: Starting Page ID
			end_page: Ending Page ID

2.  Spider for yirendai bid info

		Entry: yirendai/spiders/biaodi.py

		Description: Get Yirendai Bid Info According To IDs From 'yirendai_tender' Table.

		URL Reference: https://www.yirendai.com/loan/view/{pin}?page=1&tabflag=0

		Parameters:
			from_id: Starting Bid ID
			to_id: Ending Bid ID

		Prerequisites:
			Completed job about yirendai tender list and make sure 'from_id' & 'to_list' in the range.

3.  Spider for yirendai bidder info

		Entry: yirendai/spiders/biaoren.py

		Description: Get Yirendai Bidder Info For Each Bid Detail.

		URL Reference: https://www.yirendai.com/loan/view/{pin}?page=1&tabflag=1

		Parameters:
			from_id: Starting Bid ID
			to_id: Ending Bid ID

		Prerequisites:
			Completed job about yirendai tender list and make sure 'from_id' & 'to_list' in the range.

### About `'renrendai'` Bot(deprecated)

1.  Spider for loan list info

			Entry: renrendai/spiders/loanid.py

			Description: Get Loan List Info

			URL Reference: http://www.we.com/lend/loanList!json.action?pageIndex={page_id}

			Parameters:
				start_page_id: Starting Page Index
				end_page_id: Ending Page Index

2.  Spider for invest record info

			Entry: renrendai/spiders/investrecord.py

			Description: Get Invest Record Info

			URL Reference: http://www.we.com/lend/getborrowerandlenderinfo.action?id=lenderRecords&loanId={loanId}

			Parameters:
				from_id: Starting Bid ID
				to_id: Ending Bid ID

			Prerequisites:
				Completed job about renrendai loan list and make sure 'from_id' & 'to_id' in the range.

3.  Spider for product and borrower info

			Entry: renrendai/spiders/product.py

			Description: Get Product and Borrower Info

			URL Reference: http://www.we.com/lend/detailPage.action?loanId={loanId}

			Parameters:
				from_id: Starting Bid ID
				to_id: Ending Bid ID
				jsessionid: Login in http://www.we.com and get JSESSIONID from Cookies, remember to remain logining status until finish crawling

			Prerequisites:
				Completed job about renrendai loan list and make sure 'from_id' & 'to_id' in the range.

			Cmdline Example:
				curl http://localhost:6800/schedule.json -d project=renrendai -d spider=product -d from_id=1 -d to_id=2 -d jsessionid='6C1C829649C22D8C48E5C86AF950E99AE7F30630E0CAEDD9D50A81CE35374ECD'

### About `'enterprise'` Bot(deprecated)

1.  Spider for enterprise loan info

			Entry: enterprise/spiders/jiekuan.py

			Description: Get Enterprise Loan Info

			URL Reference: http://www.xxx.com/api/loans (with hidden parameters)

			Parameters:
				plat_id: Plat ID
				plat_name: Plat Name
				need_token: Need Token Or Not
				formated_url: '/loans' API URL
				total_page: Total Page Count

			Prerequisites:
				Completed 'exporterHelper' job for getting enterprise token if need. See more at entry 'exporterHelper/spiders/enterprise_plat_login.py'.

2.  Spider for enterprise invest info

			Entry: enterprise/spiders/toubiao.py

			Description: Get Enterprise Invest Info

			URL Reference: http://www.xxx.com/api/invests (with hidden parameters)

			Parameters:
				plat_id: Plat ID
				plat_name: Plat Name
				need_token: Need Token Or Not
				formated_url: '/invests' API URL
				time_from: From Time (For Query)
				time_to: To Time (For Query)

			Prerequisites:
				Completed 'exporterHelper' job for getting enterprise token if need. See more at entry 'exporterHelper/spiders/enterprise_plat_login.py'.

3.  Spider for enterprise overdue info

			Entry: enterprise/spiders/yuqi.py

			Description: Get Enterprise Overdue Info

			URL Reference: http://www.xxx.com/api/overdues (with hidden parameters)

			Parameters:
				plat_id: Plat ID
				plat_name: Plat Name
				need_token: Need Token Or Not
				formated_url: '/overdues' API URL
				total_page: Total Page Count

			Prerequisites:
				Completed 'exporterHelper' job for getting enterprise token if need. See more at entry 'exporterHelper/spiders/enterprise_plat_login.py'.

### About `'aif'` Bot

1.  Spider for aif basic data

			Entry: aif/spiders/jiben.py

			Description: Get AIF Basic Data

			URL Reference: Varies From Different Company

			Parameters:
				plat_id: Plat ID
				method: '0' For Post and '1' For Get
				need_token: Need Token Or Not
				formated_url: '/Interface-basicdata' API URL
				password: Authenticated Password
				from_date: Starting Date (FORMAT: yyyymmdd)
			    to_date: Ending Date (FORMAT: yyyymmdd)
			    is_json: Posting Json Or Not
			    is_upper: Signature To Upper Or Not

			Prerequisites:
				Completed 'exporterHelper' job for getting aif token if need. See more at entry 'exporterHelper/spiders/aif_plat_login.py'.

2.  Spider for aif daily data

			Entry: aif/spiders/meiri.py

			Description: Get AIF Daily Data

			URL Reference: Varies From Different Company

			Parameters:
				plat_id: Plat ID
				method: '0' For Post and '1' For Get
				need_token: Need Token Or Not
				formated_url: '/Interface-basicdata' API URL
				password: Authenticated Password
				from_date: Starting Date (FORMAT: yyyymmdd)
			    to_date: Ending Date (FORMAT: yyyymmdd)
			    page_size: Requesting Page Size
			    page_index: Requesting Page Index
			    is_json: Posting Json Or Not
			    is_upper: Signature To Upper Or Not

			Prerequisites:
				Completed 'exporterHelper' job for getting aif token if need. See more at entry 'exporterHelper/spiders/aif_plat_login.py'.

1.  Spider for aif monthly data

			Entry: aif/spiders/meiyue.py

			Description: Get AIF Monthly Data

			URL Reference: Varies From Different Company

			Parameters:
				plat_id: Plat ID
				method: '0' For Post and '1' For Get
				need_token: Need Token Or Not
				formated_url: '/Interface-basicdata' API URL
				password: Authenticated Password
				month: Corresponding Month Timestamp (FORMAT: yyyymm)
			    is_json: Posting Json Or Not
			    is_upper: Signature To Upper Or Not

			Prerequisites:
				Completed 'exporterHelper' job for getting aif token if need. See more at entry 'exporterHelper/spiders/aif_plat_login.py'.

### About `'baidu_apistore'` Bot

1.  Spider for baidu apistore yiyuan finance news

			Entry: baidu_apistore/spiders/yiyuan_caijing.py

			Description: Get Baidu Apistore Yiyuan Finance News

		  URL Reference: http://apis.baidu.com/showapi_open_bus/channel_news/search_news (need apiKey by yourself)

			Parameters:
				channel_id: Channel ID
				api_key: Api Key
				page_count: Total Page Count

### About `'helpers'` Bot

#### About `'exporterHelper'` Bot

1.  Spider for 'wangdaizhijia' rating URLs.

		Entry: exporterHelper/spiders/wangjia_rating_list.py

		Description: Get 'wangdaizhjia' Rating URLs From Rating Page. (Just Current Month Only)

		URL Reference: http://www.wdzj.com/pingji.html

		Parameters: None

		Export File: 'items/cache/{job_id}.ch'

2.  Spider for 'wangdaizhijia' specific category news URLs.

		Entry: exporterHelper/spiders/wangjia_news_list.py

		Description: Get 'wangdaizhjia' News URLs From News Overview Page.

		URL Reference: http://www.wdzj.com/news/{category}/

		Parameters:
			from_id: Starting News Anchor
			to_id: Ending News Anchor
			category: Category ID

		Export File: 'items/cache/{job_id}.ch'

3.  Spider for 'wangdaizhijia' exposure URLs.

		Entry: exporterHelper/spiders/wangjia_exposure_list.py

		Description: Get 'wangdaizhjia' Exposure URLs From Exposure Overview Page.

		URL Reference: http://bbs.wdzj.com/comeing-guide-408.html

		Parameters:
			from_id: Starting News Anchor
			to_id: Ending News Anchor

		Export File: 'items/cache/{job_id}.ch'

4.  Spider for 'aif' login tokens.

		Entry: exporterHelper/spiders/aif_plat_login.py

		Description: Get 'aif' Tokens From '/Interface-login' API.

		URL Reference: 'http://api.xxx.com/Interface-login?username={username}&password={password}

		Parameters:
			plat_id: Plat ID
			login_url: '/Interface-login' API URL

5.  Spider for 'enterprise' login tokens.(deprecated)

		Entry: exporterHelper/spiders/enterprise_plat_login.py

		Description: Get 'enterprise' Tokens From '/login' API.

		URL Reference: 'http://www.xxx.com/login?username={username}&password={password}

		Parameters:
			plat_id: Enterprise Plat ID
			login_url: '/login' API URL

		Export File: 'items/tokens/{plat_id}.tk'

6. Spider for 'enterprise' count page.(deprecated)

		Entry: exporterHelper/spiders/enterprise_plat_count_page.py

		Description: Get 'enterprise' Page Count From Related Content API.

		URL Reference: http://www.xxx.com/api/xxx (with hidden parameters)

		Parameters:
			plat_id: Enterprise Plat ID
			need_token: Need Token Or Not(1 or 0)
			formated_url: '/api/xxx' API URL

		Export File: 'items/cache/{job_id}.tk'

7. Spider for 'baidu_apistore' count page.(deprecated)

		Entry: exporterHelper/spiders/baidu_apistore_yiyuan_count_page.py

		Description: Get 'baidu_apistore' Page Count From API.

		URL Reference: http://apis.baidu.com/showapi_open_bus/channel_news/search_news (need apiKey by yourself)

		Parameters:
			channel_id: Channel ID
			api_key: Api Key

		Export File: 'items/cache/{job_id}.tk'

#### About `'imageHelper'` Bot

1.  Spider for images

		Entry: imageHelper/spiders/grabber.py

		Description: Get Images From Tables According To Specific Field & Save To Specific Directory.

		URL Reference: None

		Parameters:
			from_id: Starting Record ID
			to_id: Ending Record ID
			category: DIR Name
			model: Model Name
			field: Field Name

		Prerequisites:
			Make sure 'from_id' & 'to_id' in the range.
			Make sure 'category' & 'models' & 'field' exsits.