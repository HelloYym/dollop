# -*- coding: utf-8 -*-
import scrapy
from utils.webpage import get_trunk, get_content
from baoxian.items import CompanyItem

class BjhCompanySpider(scrapy.Spider):
    name = "bjh_company"
    pipeline = ['UniqueItemPersistencePipeline']
    allowed_domains = ["http://www.circ.gov.cn/"]
    start_url = 'http://www.circ.gov.cn/tabid/6596/Default.aspx'

    def get_code_from_url(self, url):
        return url.split('/')[-2]

    def start_requests(self):
        yield scrapy.FormRequest(url=self.start_url,
                                 method='POST',
                                 headers={
                                     'Content-Type': '''multipart/form-data; boundary=----WebKitFormBoundaryEY8BJt0fGlt8Q7pK'''},
                                 body=self.get_request_body(),
                                 callback=self.parse_company_list,
                                 dont_filter=True
                                 )

    def parse_company_list(self, response):
        for company_item in response.xpath('//tr[@class="datagrid-Item" or @class="datagrid-Alter"]'):
            # name = get_content(company_item.xpath('td[1]/text()').extract())
            link = 'http://www.circ.gov.cn' + get_content(company_item.xpath('td[last()]/a/@onclick').re(r'OpenWin\(\'(.*?)\'\)'))

            yield scrapy.FormRequest(url=link,
                                     formdata={'ctlmode': 'none'},
                                     callback=self.parse_company_detail,
                                     dont_filter=True)

    def parse_company_detail(self, response):

        company = CompanyItem()
        company['code'] = self.get_code_from_url(response.url)
        company['link'] = response.url
        company['name'] = get_content(response.xpath('//span[contains(@id, "ComName")]/text()').extract())
        company['type'] = get_content(response.xpath('//span[contains(@id, "ComType")]/text()').extract())
        company['estab_date'] = get_content(response.xpath('//span[contains(@id, "OrgDate")]/text()').extract())
        company['address'] = get_content(response.xpath('//span[contains(@id, "Address")]/text()').extract())
        company['phone'] = get_content(response.xpath('//span[contains(@id, "Tel")]/text()').extract())
        company['principal'] = get_content(response.xpath('//span[contains(@id, "Principal")]/text()').extract())
        company['sw'] = get_content(response.xpath('//span[contains(@id, "SW")]/text()').extract())
        company['register_address'] = get_content(response.xpath('//span[contains(@id, "RegAddress")]/text()').extract())
        company['state'] = get_content(response.xpath('//span[contains(@id, "State")]/text()').extract())
        yield company




    def get_request_body(self):
        return '''------WebKitFormBoundaryEY8BJt0fGlt8Q7pK
Content-Disposition: form-data; name="__EVENTTARGET"

ess$ctr17198$SearchOrganization$wuPager$ddlPageSize
------WebKitFormBoundaryEY8BJt0fGlt8Q7pK
Content-Disposition: form-data; name="__EVENTARGUMENT"


------WebKitFormBoundaryEY8BJt0fGlt8Q7pK
Content-Disposition: form-data; name="__LASTFOCUS"


------WebKitFormBoundaryEY8BJt0fGlt8Q7pK
Content-Disposition: form-data; name="__VIEWSTATE"

/wEPDwUJNjcwNjk2ODMxD2QWBmYPFgIeBFRleHQFeTwhRE9DVFlQRSBodG1sIFBVQkxJQyAiLS8vVzNDLy9EVEQgWEhUTUwgMS4wIFRyYW5zaXRpb25hbC8vRU4iICJodHRwOi8vd3d3LnczLm9yZy9UUi94aHRtbDEvRFREL3hodG1sMS10cmFuc2l0aW9uYWwuZHRkIj5kAgEPZBYQAgUPFgIeB1Zpc2libGVoZAIGDxYCHgdjb250ZW50BQzmnLrmnoTmo4DntKJkAgcPFgIfAgUu5Lit5Zu95L+d6Zmp55uR552j566h55CG5aeU5ZGY5LyaLEVhc3lTaXRlLEVTU2QCCA8WAh8CBTlDb3B5cmlnaHQgMjAxMSBieSBIdWlsYW4gSW5mb3JtYXRpb24gVGVjaG5vbG9neSBDby4sIEx0ZC5kAgkPFgIfAgUJRWFzeVNpdGUgZAIKDxYCHwIFIeS4reWbveS/nemZqeebkeedo+euoeeQhuWnlOWRmOS8mmQCDQ8WAh8CBQ1JTkRFWCwgRk9MTE9XZAIRDxYCHglpbm5lcmh0bWwFvg8uZXNzX2Vzc21lbnVfY3RsZXNzbWVudV9zcG1iY3RyIHtib3JkZXItYm90dG9tOiBUcmFuc3BhcmVudCAwcHggc29saWQ7IGJvcmRlci1sZWZ0OiBUcmFuc3BhcmVudCAwcHggc29saWQ7IGJvcmRlci10b3A6IFRyYW5zcGFyZW50IDBweCBzb2xpZDsgYm9yZGVyLXJpZ2h0OiBUcmFuc3BhcmVudCAwcHggc29saWQ7ICBiYWNrZ3JvdW5kLWNvbG9yOiBUcmFuc3BhcmVudDt9DQouZXNzX2Vzc21lbnVfY3RsZXNzbWVudV9zcG1iYXIge2N1cnNvcjogcG9pbnRlcjsgY3Vyc29yOiBoYW5kOyBoZWlnaHQ6MDt9DQouZXNzX2Vzc21lbnVfY3RsZXNzbWVudV9zcG1pdG0ge2N1cnNvcjogcG9pbnRlcjsgY3Vyc29yOiBoYW5kOyBjb2xvcjogVHJhbnNwYXJlbnQ7IGZvbnQtc2l6ZTogMTJwdDsgZm9udC13ZWlnaHQ6IG5vcm1hbDsgZm9udC1zdHlsZTogbm9ybWFsOyBib3JkZXItbGVmdDogVHJhbnNwYXJlbnQgMHB4IHNvbGlkOyBib3JkZXItYm90dG9tOiBUcmFuc3BhcmVudCAwcHggc29saWQ7IGJvcmRlci10b3A6IFRyYW5zcGFyZW50IDBweCBzb2xpZDsgYm9yZGVyLXJpZ2h0OiBUcmFuc3BhcmVudCAwcHggc29saWQ7fQ0KLmVzc19lc3NtZW51X2N0bGVzc21lbnVfc3BtaWNuIHtjdXJzb3I6IHBvaW50ZXI7IGN1cnNvcjogaGFuZDsgYmFja2dyb3VuZC1jb2xvcjogVHJhbnNwYXJlbnQ7IGJvcmRlci1sZWZ0OiBUcmFuc3BhcmVudCAxcHggc29saWQ7IGJvcmRlci1ib3R0b206IFRyYW5zcGFyZW50IDFweCBzb2xpZDsgYm9yZGVyLXRvcDogVHJhbnNwYXJlbnQgMXB4IHNvbGlkOyB0ZXh0LWFsaWduOiBjZW50ZXI7IHdpZHRoOiA1O2hlaWdodDogMDtkaXNwbGF5Om5vbmU7fQ0KLmVzc19lc3NtZW51X2N0bGVzc21lbnVfc3Btc3ViIHt6LWluZGV4OiAxMDAwOyBjdXJzb3I6IHBvaW50ZXI7IGN1cnNvcjogaGFuZDsgYmFja2dyb3VuZC1jb2xvcjogVHJhbnNwYXJlbnQ7IGZpbHRlcjpwcm9naWQ6RFhJbWFnZVRyYW5zZm9ybS5NaWNyb3NvZnQuU2hhZG93KGNvbG9yPSdEaW1HcmF5JywgRGlyZWN0aW9uPTEzNSwgU3RyZW5ndGg9MykgO2JvcmRlci1ib3R0b206IFRyYW5zcGFyZW50IDBweCBzb2xpZDsgYm9yZGVyLWxlZnQ6IFRyYW5zcGFyZW50IDBweCBzb2xpZDsgYm9yZGVyLXRvcDogVHJhbnNwYXJlbnQgMHB4IHNvbGlkOyBib3JkZXItcmlnaHQ6IFRyYW5zcGFyZW50IDBweCBzb2xpZDt9DQouZXNzX2Vzc21lbnVfY3RsZXNzbWVudV9zcG1icmsge2JvcmRlci1ib3R0b206IFRyYW5zcGFyZW50IDBweCBzb2xpZDsgYm9yZGVyLWxlZnQ6IFRyYW5zcGFyZW50IDBweCBzb2xpZDsgYm9yZGVyLXRvcDogVHJhbnNwYXJlbnQgMHB4IHNvbGlkOyAgYm9yZGVyLXJpZ2h0OiBUcmFuc3BhcmVudCAwcHggc29saWQ7IGJhY2tncm91bmQtY29sb3I6IFdoaXRlOyBoZWlnaHQ6IDBweDt9DQouZXNzX2Vzc21lbnVfY3RsZXNzbWVudV9zcG1pdG1zZWwge2JhY2tncm91bmQtY29sb3I6IFRyYW5zcGFyZW50OyBjdXJzb3I6IHBvaW50ZXI7IGN1cnNvcjogaGFuZDsgY29sb3I6IFRyYW5zcGFyZW50OyBmb250LXNpemU6IDEycHQ7IGZvbnQtd2VpZ2h0OiBub3JtYWw7IGZvbnQtc3R5bGU6IG5vcm1hbDt9DQouZXNzX2Vzc21lbnVfY3RsZXNzbWVudV9zcG1hcncge2ZvbnQtZmFtaWx5OiB3ZWJkaW5nczsgZm9udC1zaXplOiAxMHB0OyBjdXJzb3I6IHBvaW50ZXI7IGN1cnNvcjogaGFuZDsgYm9yZGVyLXJpZ2h0OiBUcmFuc3BhcmVudCAxcHggc29saWQ7IGJvcmRlci1ib3R0b206IFRyYW5zcGFyZW50IDFweCBzb2xpZDsgYm9yZGVyLXRvcDogVHJhbnNwYXJlbnQgMHB4IHNvbGlkOyBkaXNwbGF5Om5vbmU7fQ0KLmVzc19lc3NtZW51X2N0bGVzc21lbnVfc3BtcmFydyB7Zm9udC1mYW1pbHk6IHdlYmRpbmdzOyBmb250LXNpemU6IDEwcHQ7IGN1cnNvcjogcG9pbnRlcjsgY3Vyc29yOiBoYW5kO30NCi5lc3NfZXNzbWVudV9jdGxlc3NtZW51X3NwbWl0bXNjciB7d2lkdGg6IDEwMCU7IGZvbnQtc2l6ZTogNnB0O30NCmQCAg9kFgICAQ9kFgZmD2QWAmYPFgIfAWgWBAIBD2QWBAIDDxBkZBYAZAIFDw8WAh8BaGRkAgMPZBYEZg8UKwACFCsAAg8WBh4NU2VsZWN0ZWRJbmRleGYeBFNraW4FB0RlZmF1bHQeE0VuYWJsZUVtYmVkZGVkU2tpbnNoZBAWBmYCAQICAgMCBAIFFgYUKwACZGQUKwACZGQUKwACDxYCHwFoZGQUKwACDxYCHwFoZGQUKwACZGQUKwACZGQPFgZmZmZmZmYWAQVuVGVsZXJpay5XZWIuVUkuUmFkVGFiLCBUZWxlcmlrLldlYi5VSSwgVmVyc2lvbj0yMDExLjEuNTE5LjM1LCBDdWx0dXJlPW5ldXRyYWwsIFB1Ymxp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
------WebKitFormBoundaryEY8BJt0fGlt8Q7pK
Content-Disposition: form-data; name="__VIEWSTATEGENERATOR"

CA0B0334
------WebKitFormBoundaryEY8BJt0fGlt8Q7pK
Content-Disposition: form-data; name="ScrollTop"


------WebKitFormBoundaryEY8BJt0fGlt8Q7pK
Content-Disposition: form-data; name="__essVariable"


------WebKitFormBoundaryEY8BJt0fGlt8Q7pK
Content-Disposition: form-data; name="ess$ctr17198$SearchOrganization$txtComName"


------WebKitFormBoundaryEY8BJt0fGlt8Q7pK
Content-Disposition: form-data; name="ess$ctr17198$SearchOrganization$ddlComType"

-1
------WebKitFormBoundaryEY8BJt0fGlt8Q7pK
Content-Disposition: form-data; name="ess$ctr17198$SearchOrganization$txtOrgDateS"


------WebKitFormBoundaryEY8BJt0fGlt8Q7pK
Content-Disposition: form-data; name="ess$ctr17198$SearchOrganization$txtOrgDateE"


------WebKitFormBoundaryEY8BJt0fGlt8Q7pK
Content-Disposition: form-data; name="ess$ctr17198$SearchOrganization$ddlState"

-1
------WebKitFormBoundaryEY8BJt0fGlt8Q7pK
Content-Disposition: form-data; name="ess$ctr17198$SearchOrganization$ddlSW"

-1
------WebKitFormBoundaryEY8BJt0fGlt8Q7pK
Content-Disposition: form-data; name="ess$ctr17198$SearchOrganization$ddlRegAddr"

-1
------WebKitFormBoundaryEY8BJt0fGlt8Q7pK
Content-Disposition: form-data; name="ess$ctr17198$SearchOrganization$wuPager$txtPageNum"


------WebKitFormBoundaryEY8BJt0fGlt8Q7pK
Content-Disposition: form-data; name="ess$ctr17198$SearchOrganization$wuPager$ddlPageSize"

-1
------WebKitFormBoundaryEY8BJt0fGlt8Q7pK--'''
