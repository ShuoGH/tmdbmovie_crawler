import requests
from bs4 import BeautifulSoup
import json


class GetIp(object):
    '''
    Scrape the proxies 代理ip 
    抓取的是国内的高匿代理
    '''

    def __init__(self):
        '''
        self.url is the website which we have the proxies
        self.check_url is the website which we are going to scrape
        '''
        self.url = 'http://www.xicidaili.com/nn/'
        self.check_url = 'https://www.themoviedb.org/movie'
        self.ip_list = []

    @staticmethod
    def get_html(url):
        '''
        Sometimes, you should have a proxies to access the xicidaili.com...
        '''
        proxies = {
            "http": "http://185.233.94.184:53281"
        }
        header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
            'Referer': 'https://www.xicidaili.com/'
        }
        # request = requests.get(url=url, headers=header)
        request = requests.get(url=url, headers=header, proxies=proxies)
        print("The status of getting the proxies:{}".format(request))
        request.encoding = 'utf-8'
        html = request.text
        # print(html)
        return html

    def get_available_ip(self, ip_address, ip_port):
        '''
        check whether the proxies are available
        '''
        header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
            # 'Referer': 'https://www.mzitu.com/'
        }
        ip_url_next = '://' + ip_address + ':' + ip_port
        proxies = {'http': 'http' + ip_url_next}
        try:
            r = requests.get(self.check_url, headers=header,
                             proxies=proxies)
            print("success-{}".format(ip_address))
            ip_info = {'address': ip_address, 'port': ip_port}
            self.ip_list.append(ip_info)
        except:
            print('fail-{}'.format(ip_address))

    def main(self):
        web_html = self.get_html(self.url)
        soup = BeautifulSoup(web_html, 'lxml')
        ip_list = soup.find(id='ip_list').find_all('tr')
        print("the number of the ip: {}".format(len(ip_list)))

        for ip_info in ip_list:
            td_list = ip_info.find_all('td')
            if len(td_list) > 0:
                ip_address = td_list[1].text
                ip_port = td_list[2].text
                # check the availability of the ip
                self.get_available_ip(ip_address, ip_port)

        # write to the file
        with open('ip_movie.txt', 'w') as file:
            json.dump(self.ip_list, file)
        print(self.ip_list)


if __name__ == '__main__':
    get_ip = GetIp()
    get_ip.main()
