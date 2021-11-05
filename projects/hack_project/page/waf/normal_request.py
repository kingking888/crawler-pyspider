import uuid

from hack_project.config import def_headers
from hack_project.page.waf.central_attack import CentralAttack
from pyspider.libs.base_crawl import *


class NormalRequest(BaseCrawl):

    def __init__(self, url, crawl_next=False):
        super(NormalRequest, self).__init__()
        self.url = url
        self.crawl_next = crawl_next

    def crawl_builder(self):
        builder = CrawlBuilder() \
            .set_url(self.url + "#NormalRequest") \
            .set_headers(def_headers) \
            .set_task_id(uuid.uuid4())
        return builder

    def parse_response(self, response, task):
        print("response:{}".format(response.text))
        status_code = response.status_code
        redirect_url = response.url

        if self.crawl_next:
            self.crawl_next_page({
                "normal_request": {
                    "headers": "",
                    "content": response.text,
                }
            })

        return {
            'status_code': status_code,
            'redirect_url': redirect_url,
            'content': response.text[:500],
            'content size': len(response.text),
        }

    def crawl_next_page(self, meta_data: dict):
        self.crawl_handler_page(CentralAttack(self.url, meta_data=meta_data))


if __name__ == '__main__':
    NormalRequest("www.baidu.com").get_result()
