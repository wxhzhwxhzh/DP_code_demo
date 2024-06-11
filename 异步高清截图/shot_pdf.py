#!/usr/bin/env python
# -*- coding:utf-8 -*-

# DrissionPage 库 文档地址 http://g1879.gitee.io/drissionpagedocs/


#-导入库
import os
import sys
import asyncio

# 获取当前脚本的绝对路径
current_script_path = os.path.abspath(__file__)

# 获取当前脚本的父目录
parent_directory = os.path.dirname(os.path.dirname(current_script_path))

# 将父目录添加到 sys.path
if parent_directory not in sys.path:
    sys.path.insert(0, parent_directory)

from SaossionPage import Browser,Config
from DrissionPage.common import Keys, Actions


async def main():

    #-创建浏览器
    browser = Browser(config='忽略证书错误 端口7878 ')

    #-设置文件下载目录 默认是当前目录
    # page.set.download_path(".")




    url='https://www.jroneturbo.com/pdf/Actuators/index.html'
    tab=browser.page.new_tab(url)

    tab.wait(1)

    input('电脑必须安装谷歌浏览器，并且请手动调整浏览器到 下载资料的页面，按回车继续... ?')
    tab.wait(1)

    tab=browser.newest_tab

    download_path_name='img18'

    for i in  range(0,3):
        tab=browser.newest_tab

        div_tag=tab.ele(f't:div@@class=background',index=2)
        

        tab.set.download_path(f'./{download_path_name}')        
        img_blob=await browser.get_screenshot_by_js_asyc(div_tag,rename=f'shot{i}.png')   
        print(img_blob)    
        

        print(f'第{i}页')

        tab=browser.newest_tab

        Actions(tab).key_down(Keys.ARROW_RIGHT)

        tab.wait(2)


asyncio.run(main())
