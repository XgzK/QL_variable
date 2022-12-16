import re
import time

import requests


class Lottery:
    def __init__(self):
        self.headers = [
            {
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,"
                          "application/signed-exchange;v=b3;q=0.9",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": "zh-CN,zh;q=0.9",
                "Connection": "keep-alive",
                "Cookie": "unionuuid=V2_ZgUbCkdeRBQnCkQBfhpcUW4HRV1GVUYccF1CUnwRXgIIABNeQVdDFn0IQ1d6G1xqZwoRQkJXSgp2CkVLexhZ; "
                          "language=zh_CN; __jda=123.16697028320441614753532.1669702832.1669702832.1669702832.2; __jdc=123; "
                          "mba_muid=16697028320441614753532; share_cpin=; share_open_id=; share_gpin=; channel=; source_module=; "
                          "erp=; visitkey=86254801803499; "
                          "CSID=HT06HnkCWFpTT1ZeWRReT1A0IH10KAUKEApVA0wJDFZqeHZ4dHx3chxTUi1TWlRXWnZnYA5fRBRqZBhxXFtZOkdbXENHX09GZ3V6antWWg%3d%3d; unpl=JF8EAK9jNSttWx8BV0lXHkEXHFUGW10KSh8LbWcGUQoIGVcMGwJMEhR7XlVdXhRLFx9sbxRUWFNIXQ4fASsSEHteVVxcD0sUA2tgNVJdX0xXBxgyGxMRSlVXWlwIQicAb1cEZF1fTFwDGgESEBNKWFFeWghOEQdtYwdXbVl7VA0cMisiEXtdV1tYCXsWMy4JBVdbWU9QBxNPGxUXQ1tVXVQKSBYGamcCVFheT1YBGQErEyBI; CCC_SE=ADC_5n%2bm8fzTbtjP5EQGzzCLf1tPCxuHgOnfLUTk5TYAuKgeAoVQnchfuynZh7ySu8G%2f2t%2flp8CEEs%2fPdD4uET8DHxc8Zy4ic5n6zs5ZMl3zDVrXjC%2bsJySLO7M0Rc%2fUrHuroduCAoOzNka6wfkOMLAFQtZyoS0NmnH785mdxDIQgYSAp6KNUOsKlpC4IASx2VLYie%2f50ZbHZkrdTcOU50yeOJpAuQHqhjbZOSg4JQDP9dlwIbRnhKm%2bLDG1Hhvj%2bo2aO62iUjfonivy6yY%2bPtUuUSbZD9Bl%2fGzX5YBQAJj831npTmd224SWLbpqaWN8A%2fXRcGBdscyWjpHR0sCttBET6HOrB52ugRJ7Qy11wXNrflDP8724dYIramxnlPrg2dXAvLIJ1CmxxHHznB00CY5hhaP2fhAXHr6wMKAoLk2tq2SOslF5v39B3N5nwtO%2fhJLRMcBABrjcqdEMycbCShYSZ2DtKBOlAG8lK6OXoU5OlzOfA9Bbras5jRaZposGFIubSRwy4FiJYftFSIKenQ3Yfw%3d%3d; __jdb=123.4.16697028320441614753532|2.1669702832; __jdv=123%7Ckong%7Ct_2030612156_7166232%7Cjingfen%7C2edccd4b6f9c4130993124fac2811f15%7C1669703333218; PPRD_P=LOGID.1669703333358.69622262; mba_sid=16697028329705207265371209400.4; __jd_ref_cls=MDownLoadFloat_TopOldExpo",
                "sec-ch-ua": '"Microsoft Edge";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
                "sec-ch-ua-mobile": "?0",
                "sec-ch-ua-platform": "Windows",
                "Sec-Fetch-Dest": "document",
                "Sec-Fetch-Mode": "navigate",
                "Sec-Fetch-Site": "none",
                "Sec-Fetch-User": "?1",
                "Upgrade-Insecure-Requests": "1",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 "
                              "Safari/537.36 Edg/107.0.1418.56 "
            },
            {
                "accept": "*/*",
                "accept-encoding": "gzip, deflate, br",
                "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
                "Cookie": "unionuuid=V2_ZgUbCkdeRBQnCkQBfhpcUW4HRV1GVUYccF1CUnwRXgIIABNeQVdDFn0IQ1d6G1xqZwoRQkJXSgp2CkVLexhZ; language=zh_CN; __jda=123.16697028320441614753532.1669702832.1669702832.1669702832.2; __jdc=123; mba_muid=16697028320441614753532; share_cpin=; share_open_id=; share_gpin=; channel=; source_module=; erp=; visitkey=86254801803499; CSID=HT06HnkCWFpTT1ZeWRReT1A0IH10KAUKEApVA0wJDFZqeHZ4dHx3chxTUi1TWlRXWnZnYA5fRBRqZBhxXFtZOkdbXENHX09GZ3V6antWWg%3d%3d; unpl=JF8EAK9jNSttWx8BV0lXHkEXHFUGW10KSh8LbWcGUQoIGVcMGwJMEhR7XlVdXhRLFx9sbxRUWFNIXQ4fASsSEHteVVxcD0sUA2tgNVJdX0xXBxgyGxMRSlVXWlwIQicAb1cEZF1fTFwDGgESEBNKWFFeWghOEQdtYwdXbVl7VA0cMisiEXtdV1tYCXsWMy4JBVdbWU9QBxNPGxUXQ1tVXVQKSBYGamcCVFheT1YBGQErEyBI; CCC_SE=ADC_5n%2bm8fzTbtjP5EQGzzCLf1tPCxuHgOnfLUTk5TYAuKgeAoVQnchfuynZh7ySu8G%2f2t%2flp8CEEs%2fPdD4uET8DHxc8Zy4ic5n6zs5ZMl3zDVrXjC%2bsJySLO7M0Rc%2fUrHuroduCAoOzNka6wfkOMLAFQtZyoS0NmnH785mdxDIQgYSAp6KNUOsKlpC4IASx2VLYie%2f50ZbHZkrdTcOU50yeOJpAuQHqhjbZOSg4JQDP9dlwIbRnhKm%2bLDG1Hhvj%2bo2aO62iUjfonivy6yY%2bPtUuUSbZD9Bl%2fGzX5YBQAJj831npTmd224SWLbpqaWN8A%2fXRcGBdscyWjpHR0sCttBET6HOrB52ugRJ7Qy11wXNrflDP8724dYIramxnlPrg2dXAvLIJ1CmxxHHznB00CY5hhaP2fhAXHr6wMKAoLk2tq2SOslF5v39B3N5nwtO%2fhJLRMcBABrjcqdEMycbCShYSZ2DtKBOlAG8lK6OXoU5OlzOfA9Bbras5jRaZposGFIubSRwy4FiJYftFSIKenQ3Yfw%3d%3d; __jdb=123.4.16697028320441614753532|2.1669702832; __jdv=123%7Ckong%7Ct_2030612156_7166232%7Cjingfen%7C2edccd4b6f9c4130993124fac2811f15%7C1669703333218; PPRD_P=LOGID.1669703333358.69622262; mba_sid=16697028329705207265371209400.4; __jd_ref_cls=MDownLoadFloat_TopOldExpo",
                "dnt": "1",
                "origin": "https://shop.m.jd.com",
                "referer": "https://shop.m.jd.com/",
                "sec-ch-ua-mobile": "?0",
                "sec-ch-ua-platform": "Windows",
                "sec-fetch-dest": "empty",
                "sec-fetch-mode": "cors",
                "sec-fetch-site": "same-site",
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
            }
        ]

    def urlJump(self, url) -> list:
        """
        短URL获取跳转后的长URL
        :param url: https://u.jd.com/odnXBMw
        :return: URL
        """
        try:
            jump = requests.get(url=url, headers=self.headers[0], allow_redirects=False)
            jump.close()
            if jump.status_code == 200:
                return re.findall("hrl='(.*?)'", jump.text)
            else:
                return []
        except Exception as e:
            print(f"短URL获取跳转后的长URL异常 {e}")
            return []

    def url302(self, url) -> list:
        """
        302跳转获取店铺 shopId
        :param url:
        :return: [json] []
        """
        try:
            getId = requests.get(url=url, headers=self.headers[0], allow_redirects=False)
            if getId.status_code == 302:
                location = getId.headers['location'].replace("https://shop.m.jd.com/?", "")
                if location:
                    cc = {}
                    for i in location.split('&'):
                        a = i.split('=')
                        cc.setdefault(a[0], a[1])
                    return [cc]
                else:
                    return []
        except Exception as e:
            print(f"短URL获取跳转后的长URL异常 {e}")
            return []

    def getvenderId(self, js) -> str:
        """
        获取店铺的 venderId
        :param js: URL中部分参数
        :return:
        """
        try:
            url = 'https://api.m.jd.com/client.action?functionId=whx_getMShopOutlineInfo&body={"cu":"true",' + f'"shopId":"{js["shopId"]}","utm_campaign":"{js["utm_campaign"]}","utm_medium":"{js["utm_medium"]}","utm_source":"{js["utm_source"]}","utm_term":"{js["utm_term"]}","source":"m-shop"' + '}&' + f't={int(time.time())}337&appid=shop_view&clientVersion=11.0.0&client=wh5&area=1_72_2799_0&uuid="{int(time.time()) - 12121355344}360960026"'
            vender = requests.get(url, headers=self.headers[1], allow_redirects=False)
            if vender.status_code == 200:
                venderId = vender.json()['data']['shopInfo']['venderId']
                shopId = vender.json()['data']['shopInfo']['shopId']
                return f"https://shop.m.jd.com/shop/lottery?shopId={shopId}&venderId={venderId}"
            else:
                return ''
        except Exception as e:
            print(f"获取店铺的 venderId 异常 {e}")
            return ""

    def main_lottery(self, url) -> str:
        """
        执行这个类的方法
        :param url: https://u.jd.com/odnXBMw
        :return: https://shop.m.jd.com/shop/lottery?shopId=10183543&venderId=10327499
        """
        jump = self.urlJump(url)
        if not jump:
            return ''
        ur302 = self.url302(jump[0])
        if not ur302:
            return ''
        return self.getvenderId(ur302[0])