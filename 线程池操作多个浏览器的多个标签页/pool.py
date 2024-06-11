import concurrent.futures
from DrissionPage import ChromiumPage,ChromiumOptions
import time





# 定义一个函数，用于下载网页并返回其长度
def browser_open(port_url):
    port=port_url.split('+')[0]
    url=port_url.split('+')[1]

    co=ChromiumOptions()
    co.set_local_port(port)
    page = ChromiumPage(co)
    tab_pool.append(page.new_tab(url))
    return tab_pool[-1].title


# 定义需要下载的网页列表
port_urls = [
    "7979+https://www.bing.com",
    "7979+https://www.qq.com",
    "7980+https://www.baidu.com",
    "7980+https://www.qq.com",

]

# 创建一个线程池
pool=[]
tab_pool=[]

with concurrent.futures.ThreadPoolExecutor() as executor:
    for u in port_urls:
        xiancheng=executor.submit(browser_open, u)
        pool.append(xiancheng)
        time.sleep(1)

[print(i.result())   for i in pool ]    
[print(t.ele("t:img").link)   for t in tab_pool ]    






