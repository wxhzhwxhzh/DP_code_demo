#!/usr/bin/env python
# -*- coding:utf-8 -*-

# DrissionPage 库 文档地址 http://g1879.gitee.io/drissionpagedocs/
# 骚神库网址 https://gitee.com/haiyang0726/SaossionPage

#-导入库
from DrissionPage import ChromiumPage,ChromiumOptions

from Tool import Tool

#-配置类
class Config:
    UA_android="Mozilla/5.0 (Linux; Android 11; Pixel 5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.62 Mobile Safari/537.36"
    UA_apple="Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1"
    url='https://www.douyin.com/video/7321937742974291238'
    port=7878
    listen='ali-safety-video.acfun.cn'
    url_kw='video_mp4'
    标题='t:div@@data-e2e=video-desc'
    下载文件夹='./douyin6'
    点赞评论收藏分享='x://*[@id="douyin-right-container"]/div[2]/div/div[1]/div[3]/div/div[2]/div[1]'

class Tag:
    评论内容='t:div@@data-e2e=comment-list'
#-创建配置对象
co=ChromiumOptions()

#-启动配置
co.set_local_port(Config.port)
co.ignore_certificate_errors(True)

#-创建浏览器
page = ChromiumPage(addr_or_opts=co)
tab=page.new_tab()



#-打开网址

tab.listen.start(targets='-web.douyinvod.com')
tab.get(Config.url)
tab.wait(3)

info={}
info['链接']=Config.url
info['标题']=tab.title

temp_ele= tab.ele(Config.点赞评论收藏分享)

for ii,vv in enumerate(['点赞数','评论数','收藏数 ','分享数']):
    info[vv]=temp_ele.ele('t:span',index=ii).text



info['评论内容']=tab.tab.ele(Tag.评论内容).text



for k,v in info.items():
    print(k,' ',v)





url_list=[]
title_list=[]

if input('继续抓视频  y/n?')=='y':
    for packet in tab.listen.steps():
        r_url=packet.url
        # Tool.packet_tree(packet)
        # input('1222122')
        
        if 'video_mp4' in  r_url:
            print(r_url)
            url_list.append(r_url)
            
            print(tab.title)
            title_list.append(tab.title)
            print('----------------')
            break




    tab.set.download_path(Config.下载文件夹)

    for i,v in  enumerate(url_list):    
        tab.download(v,rename=f'{title_list[i]}video{i}',suffix='mp4')




input('go on ?')
  