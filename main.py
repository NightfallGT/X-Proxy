from os import system
from colorama import Fore, init, Style
import requests
import re
import time
import threading
from proxy_checker import ProxyChecker
from sys import stdout

lock = threading.Lock()
class UI:
    @staticmethod
    def banner():
        banner = f'''
    \t\t\t    ██╗  ██╗     ██████╗ ██████╗  ██████╗ ██╗  ██╗██╗   ██╗
    \t\t\t    ╚██╗██╔╝     ██╔══██╗██╔══██╗██╔═══██╗╚██╗██╔╝╚██╗ ██╔╝
    \t\t\t     ╚███╔╝█████╗██████╔╝██████╔╝██║   ██║ ╚███╔╝  ╚████╔╝ 
    \t\t\t     ██╔██╗╚════╝██╔═══╝ ██╔══██╗██║   ██║ ██╔██╗   ╚██╔╝  
    \t\t\t    ██╔╝ ██╗     ██║     ██║  ██║╚██████╔╝██╔╝ ██╗   ██║   
    \t\t\t    ╚═╝  ╚═╝     ╚═╝     ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝   ╚═╝  
    \t\t\t                                            {Fore.LIGHTBLACK_EX}by Nightfall#2512{Style.RESET_ALL}
    '''
        return banner

    @staticmethod
    def menu():
        menu = f'''
        [{Fore.RED}1{Style.RESET_ALL}] Proxy Scrape
        [{Fore.RED}2{Style.RESET_ALL}] Proxy Check
        [{Fore.RED}3{Style.RESET_ALL}] Exit
        '''
        return menu

    @staticmethod
    def menu2():
        menu = f'''
        Select proxy check method.
        [{Fore.RED}1{Style.RESET_ALL}] Standard
        [{Fore.RED}2{Style.RESET_ALL}] Proxy Judge
        [{Fore.RED}3{Style.RESET_ALL}] Back
        '''
        return menu

def write(arg):
    lock.acquire()
    stdout.flush()
    print(arg)
    lock.release()

class XProxy:
    proxy_w_regex = [
    ["http://spys.me/proxy.txt","%ip%:%port% "],
    ["http://www.httptunnel.ge/ProxyListForFree.aspx"," target=\"_new\">%ip%:%port%</a>"],
    ["https://raw.githubusercontent.com/sunny9577/proxy-scraper/master/proxies.json", "\"ip\":\"%ip%\",\"port\":\"%port%\","],
    ["https://raw.githubusercontent.com/fate0/proxylist/master/proxy.list", '"host": "%ip%".*?"country": "(.*?){2}",.*?"port": %port%'],
    ["https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list.txt", '%ip%:%port% (.*?){2}-.-S \\+'],
    ["https://www.us-proxy.org/", "<tr><td>%ip%<\\/td><td>%port%<\\/td><td>(.*?){2}<\\/td><td class='hm'>.*?<\\/td><td>.*?<\\/td><td class='hm'>.*?<\\/td><td class='hx'>(.*?)<\\/td><td class='hm'>.*?<\\/td><\\/tr>"],
    ["https://free-proxy-list.net/", "<tr><td>%ip%<\\/td><td>%port%<\\/td><td>(.*?){2}<\\/td><td class='hm'>.*?<\\/td><td>.*?<\\/td><td class='hm'>.*?<\\/td><td class='hx'>(.*?)<\\/td><td class='hm'>.*?<\\/td><\\/tr>"],
    ["https://www.sslproxies.org/", "<tr><td>%ip%<\\/td><td>%port%<\\/td><td>(.*?){2}<\\/td><td class='hm'>.*?<\\/td><td>.*?<\\/td><td class='hm'>.*?<\\/td><td class='hx'>(.*?)<\\/td><td class='hm'>.*?<\\/td><\\/tr>"],
    ['https://www.socks-proxy.net/', "%ip%:%port%"],
    ['https://free-proxy-list.net/uk-proxy.html', "<tr><td>%ip%<\\/td><td>%port%<\\/td><td>(.*?){2}<\\/td><td class='hm'>.*?<\\/td><td>.*?<\\/td><td class='hm'>.*?<\\/td><td class='hx'>(.*?)<\\/td><td class='hm'>.*?<\\/td><\\/tr>"],
    ['https://free-proxy-list.net/anonymous-proxy.html', "<tr><td>%ip%<\\/td><td>%port%<\\/td><td>(.*?){2}<\\/td><td class='hm'>.*?<\\/td><td>.*?<\\/td><td class='hm'>.*?<\\/td><td class='hx'>(.*?)<\\/td><td class='hm'>.*?<\\/td><\\/tr>"],
    ["https://www.proxy-list.download/api/v0/get?l=en&t=https", '"IP": "%ip%", "PORT": "%port%",'],
    ["https://api.proxyscrape.com/?request=getproxies&proxytype=http&timeout=6000&country=all&ssl=yes&anonymity=all", "%ip%:%port%"],
    ["https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/http.txt", "%ip%:%port%"],
    ["https://raw.githubusercontent.com/shiftytr/proxy-list/master/proxy.txt", "%ip%:%port%"],
    ["https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/socks5.txt", "%ip%:%port%"],
    ["https://www.hide-my-ip.com/proxylist.shtml", '"i":"%ip%","p":"%port%",'],
    ["https://raw.githubusercontent.com/scidam/proxy-list/master/proxy.json", '"ip": "%ip%",\n.*?"port": "%port%",'],
    ['https://www.freeproxychecker.com/result/socks4_proxies.txt', "%ip%:%port%"],
    ['https://proxy50-50.blogspot.com/', '%ip%</a></td><td>%port%</td>'], 
    ['http://free-fresh-proxy-daily.blogspot.com/feeds/posts/default', "%ip%:%port%"],
    ['http://free-fresh-proxy-daily.blogspot.com/feeds/posts/default', "%ip%:%port%"],
    ['http://www.live-socks.net/feeds/posts/default', "%ip%:%port%"],
    ['http://www.socks24.org/feeds/posts/default', "%ip%:%port%"],
    ['http://www.proxyserverlist24.top/feeds/posts/default',"%ip%:%port%" ] ,
    ['http://proxysearcher.sourceforge.net/Proxy%20List.php?type=http',"%ip%:%port%"],
    ['http://proxysearcher.sourceforge.net/Proxy%20List.php?type=socks', "%ip%:%port%"],
    ['http://proxysearcher.sourceforge.net/Proxy%20List.php?type=socks', "%ip%:%port%"], 
    ['https://www.my-proxy.com/free-anonymous-proxy.html', '%ip%:%port%'],
    ['https://www.my-proxy.com/free-transparent-proxy.html', '%ip%:%port%'],
    ['https://www.my-proxy.com/free-socks-4-proxy.html', '%ip%:%port%'],
    ['https://www.my-proxy.com/free-socks-5-proxy.html','%ip%:%port%'],
    ['https://www.my-proxy.com/free-proxy-list.html','%ip%:%port%'],
    ['https://www.my-proxy.com/free-proxy-list-2.html','%ip%:%port%'],
    ['https://www.my-proxy.com/free-proxy-list-3.html','%ip%:%port%'],
    ['https://www.my-proxy.com/free-proxy-list-4.html', '%ip%:%port%'],
    ['https://www.my-proxy.com/free-proxy-list-5.html','%ip%:%port%'],
    ['https://www.my-proxy.com/free-proxy-list-6.html','%ip%:%port%'],
    ['https://www.my-proxy.com/free-proxy-list-7.html','%ip%:%port%'],
    ['https://www.my-proxy.com/free-proxy-list-8.html','%ip%:%port%'],
    ['https://www.my-proxy.com/free-proxy-list-9.html','%ip%:%port%'],
    ['https://www.my-proxy.com/free-proxy-list-10.html','%ip%:%port%'],
    ]

    proxy_direct = [
        'https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=5000&country=all&ssl=all&anonymity=all',
        'https://api.proxyscrape.com/v2/?request=getproxies&protocol=socks4&timeout=5000&country=all&ssl=all&anonymity=all',
        'https://api.proxyscrape.com/v2/?request=getproxies&protocol=socks5&timeout=5000&country=all&ssl=all&anonymity=all',         
        'https://www.proxyscan.io/download?type=http',
        'https://www.proxyscan.io/download?type=https',
        'https://www.proxyscan.io/download?type=socks4',
        'https://www.proxyscan.io/download?type=socks5',
        'https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt',
        'https://github.com/TheSpeedX/PROXY-List/blob/master/socks4.txt',
        'https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks5.txt',
        'https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt',
        'https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/socks4.txt',
        'https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/socks5.txt',
        'https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/https.txt',
        'https://raw.githubusercontent.com/hookzof/socks5_list/master/proxy.txt',
        'https://multiproxy.org/txt_all/proxy.txt',
        'http://rootjazz.com/proxies/proxies.txt',
        'http://ab57.ru/downloads/proxyold.txt',
        'https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt',
        'https://proxy-spider.com/api/proxies.example.txt',
        'https://raw.githubusercontent.com/opsxcq/proxy-list/master/list.txt',
        'https://www.proxy-list.download/api/v1/get?type=socks4'
        'https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/socks4.txt'
        ]
                       

    headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36"}

    def __init__(self):
        self.proxy_output = []
        self.scrape_counter = 0
        self.checked_counter= 0

    def _update_title(self):
        while True:
            elapsed = time.strftime('%H:%M:%S', time.gmtime(time.time() - self.start))
            system('title X-Proxy - Elapsed: %s ^| Scraped: %s ^| Checked :%s'% (elapsed, self.scrape_counter, self.checked_counter))
            time.sleep(0.4)

    def file_read(self, name):
        with open(name, 'r', encoding='UTF-8') as f:
            text = [line.strip('\n') for line in f]
            return text

    def file_write(self, name, contents):
        with open(name, 'w', encoding='UTF-8' ) as f:
            for x in contents:
                f.write(x + '\n')

    def background_task(self):
        self.start = time.time()
        threading.Thread(target = self._update_title, daemon=True).start()


    def get_proxies(self):
        return self.proxy_output

class ProxyScrape(XProxy):
    def _scrape(self, url, custom_regex):
        try:
            proxylist = requests.get(url, timeout=5, headers=self.headers).text
            custom_regex = custom_regex.replace('%ip%', '([0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3})')
            custom_regex = custom_regex.replace('%port%', '([0-9]{1,5})')

            for proxy in re.findall(re.compile(custom_regex), proxylist):
                self.proxy_output.append(proxy[0] + ":" + proxy[1])
                write(' > '+proxy[0] + ":" + proxy[1])
                self.scrape_counter += 1

        except requests.exceptions.RequestException:
            write('Requests related error occured.')

    def scrape_regex(self):
        for source in self.proxy_w_regex:
            self._scrape(source[0], source[1])

    def scrape_direct(self):
        for source in self.proxy_direct:
            try:
                page = requests.get(source, timeout=5, headers=self.headers).text
                for proxy in re.findall(re.compile('([0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}):([0-9]{1,5})'), page):
                    self.proxy_output.append(proxy[0] + ':' + proxy[1])
                    write(' > '  + proxy[0] + ':' + proxy[1])

            except requests.exceptions.RequestException:
                write('Requests related error occured.')
        

class ProxyCheck(XProxy):
    def __init__(self):
        XProxy.__init__(self)
        print('Loading..')
        self.checker = ProxyChecker()
        system('cls')


    def check(self, list_, timeout=5):
        for x in list_:
            c = self.checker.check_proxy(x)
            if c:
                write(Fore.GREEN + '[ALIVE] '+ x + ' | ' + c['anonymity'] + ' | ' + 'Timeout:'+ str(c['timeout']) + ' ' +c['country_code'] + Style.RESET_ALL + c['protocols'][0])
                with open('alive_checked.txt', 'a', encoding='UTF-8') as f:
                    f.write(x + '\n')
                self.checked_counter += 1
   
            else:
                write(Fore.RED + '[DEAD] ' + x + Style.RESET_ALL)
                with open('dead_checked.txt', 'a', encoding='UTF-8') as f:
                    f.write(x + '\n')
                self.checked_counter += 1


def main():
    x = UI()
    p = ProxyScrape()
    system('title X-Proxy by Nightfall#2512 ^| AIO Proxy Tool')
    system('cls')

    print(x.banner())
    print(x.menu())

    print('\n')

    try:
        user_input = int(input(f'[{Fore.RED}>{Style.RESET_ALL}] > '))
        if user_input == 1:
            system('cls')
            print(x.banner())
            p.background_task()
            print('Scraping proxies...')
            p.scrape_regex()
            p.scrape_direct()

            output = p.get_proxies()

            print('\nChecking for duplicates..')
            print('Current length:', len(output))
            clean_output = list(set(output))
            print('Length after removing duplicates:', len(clean_output))

            print('Writing to scraped.txt..')
            p.file_write('scraped.txt', clean_output)
            print('Finished.')
            system('pause>nul')

        elif user_input == 2:
            pc = ProxyCheck()

            system('cls')
            print(x.banner())

            path = input('Path: ')

            new_path = path.replace('"','')

            proxy_list = pc.file_read(new_path)

            thread_count = int(input('Enter number of threads [e.g 200] : '))
            print('Loading..')
            threads = []
            system('cls')
            print(x.banner())
            
            pc.background_task()

            for i in range(thread_count):
                t = threading.Thread(target=pc.check, args= (proxy_list[int(len(proxy_list) / thread_count * i): int(len(proxy_list)/ thread_count* (i+1))],))
                threads.append(t)
                t.start()

            for t in threads:
                t.join()

            print('Finished.')
            system('pause>nul')
            
        else:
            print('Invalid!')
            main()


    except ValueError:
        main()


if __name__ == '__main__':
    main()
