import requests
from lxml.html import fromstring


def get_proxies(count=10):
    proxies = set()
    #'https://free-proxy-list.net/'
    proxies.update(from_free_proxy_list(count))

    if(len(proxies) < count):
        #'https://advanced.name/freeproxy'
        proxies.update(advanced_free_proxy(
            count - len(proxies) 
            ))

    if(len(proxies) < count):
        proxies.update(
                read_proxi_from_file(
                    'assets/proxy_list/Free proxies.txt', 
                    count - len(proxies)))

    if(len(proxies) < count):
        proxies.update(
                read_proxi_from_file(
                    'assets/proxy_list/Free proxies for 05-04-2022.txt',
                    count - len(proxies)))

    if(len(proxies) < count):
        proxies.update(
                read_proxi_from_file(
                    'assets/proxy_list/Free proxies for 2022-04-04.txt',
                    count - len(proxies)))

    return proxies

def from_free_proxy_list(count):
    # this website provides about 21 free proxies
    url = 'https://free-proxy-list.net/'
    max_proxies = 21
    limit = max_proxies if count > max_proxies else count
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

def advanced_free_proxy(count):
    url = 'https://advanced.name/freeproxy/6255013b47ba6'
    response = requests.get(url)
    proxies = set()
    # = fromstring(response.text)
    print(type(response.text))
    for line in response.text.splitlines():
        proxies.add(line)
        if len(proxies) < count:
            break
    return proxies

def read_proxi_from_file(filename, count):
    # Using readlines()
    file = open(filename, 'r')
    lines = file.readlines();
    proxies = set()
    count = 0
    # Strips the newline character
    for line in lines:
        proxies.add(line.strip())
        if len(proxies) < count:
            break
    return proxies

# debug
#proxies = get_proxies(10000)
#print(proxies)
