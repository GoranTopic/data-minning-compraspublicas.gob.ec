import requests
from lxml.html import fromstring


def get_proxies(count=10):
    proxies = set()
    #'https://free-proxy-list.net/'
    proxies.update(from_free_proxy_list(count))
    if(len(proxies) < count):
        #'https://advanced.name/freeproxy'
        proxies.update(advanced_free_proxy())
    return proxies

def from_free_proxy_list(count):
    # this website provides about 21 free proxies
    url = 'https://free-proxy-list.net/'
    max_proxies = 21
    limit = max_proxies if count > proxies else count
    proxies = set()
    while(len(proxies) < limit):
        response = requests.get(url)
        parser = fromstring(response.text)
        print(f"grabbing proxies: {len(proxies)} out of {count}");
        for i in parser.xpath('//tbody/tr'):
            if i.xpath('.//td[7][contains(text(),"yes")]'):
                # Grabbing IP and corresponding PORT
                proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
                proxies.add(proxy)
    return proxies

def advanced_free_proxy():
    url = 'https://advanced.name/freeproxy/6255013b47ba6'
    response = requests.get(url)
    proxies = set()
    # = fromstring(response.text)
    print(type(response.text))
    for line in response.text.splitlines():
        proxies.add(line)
    return proxies


proxies = get_proxies(100)
print(proxies)
