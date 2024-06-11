#!/usr/bin/env python
# -*- coding:utf-8 -*-
# 用这个代码导入需要的库    pip install DrissionPage   DataRecorder
#  代码版本低于4.0.0，请升级DP库，至少要4.0.0以上    pip install DrissionPage --upgrade


# 原DP库 使用文档地址 http://g1879.gitee.io/drissionpagedocs/whatsnew/4_0/


# ----------------导入库----------------
from datetime import datetime
import os,re
import random
import threading
import time

from DrissionPage import ChromiumPage
from DrissionPage import ChromiumOptions
from DrissionPage.common import Keys, Actions
from colorama import Fore, init

# --------------配置类---------------
from  Config import Config

# 数据类型判断
from DrissionPage.items import SessionElement
from DrissionPage.items import ChromiumElement
from DrissionPage.items import ShadowRoot
from DrissionPage.items import NoneElement
from DrissionPage.items import ChromiumTab
from DrissionPage.items import WebPageTab
from DrissionPage.items import ChromiumFrame


# -------------浏览器类 ----------
class Browser:

    def __init__(self, browser_path="", config="",plugin_path=''):
        self.browser_path = browser_path  

        self.config_browser(config)
        # 加载插件
        if len(plugin_path)>5:

            subfolders = [f.path for f in os.scandir(plugin_path) if f.is_dir()]
            for f in subfolders:
                self.co.add_extension(f)
                print('加载插件目录 ',f)
            # self.co.add_extension(plugin_path)

        self.page = ChromiumPage(addr_or_opts=self.co)

        self.tabs = []
        self.listen_all_list=[]

    def config_browser(self, config):
        self.co = ChromiumOptions()

        if len(self.browser_path)>3:
            self.co.set_browser_path(self.browser_path)
        self.co.set_argument("--hide-crash-restore-bubble")
        co_list = config.split(" ")
        if "多开" in config:
            self.co.auto_port()
        if "无头" in config:
            self.co.headless(True)
        if "无图" in config:
            self.co.no_imgs(True)
        if "无js" in config:
            self.co.no_js(True)
        if "静音" in config:
            self.co.mute(True)

        if "匿名" in config:
            self.co.incognito(True)
        if "安卓" in config:
            self.co.set_user_agent(Config.UA_Android)
        if "苹果" in config:
            self.co.set_user_agent(Config.UA_apple)
        if "忽略证书错误" in config:
            self.co.ignore_certificate_errors(True)
        if "最大化" in config:
            self.co.set_argument("--start-maximized")
        if "最小化" in config:
            self.co.set_argument("--start-minimized")
        for i in co_list:
            if i.startswith("超时"):
                self.co.set_timeouts(base=i[2:])
        for i in co_list:
            if i.startswith("端口"):
                self.co.set_local_port(i[2:])
                print("已连接端口为", i[2:])

        for i in co_list:
            if i.startswith("代理"):
                self.co.set_proxy(i[2:])

    def open(self, url):
        self.tabs.append(self.page.new_tab(url))
        return self

    def ac(self, ele: ChromiumElement):
        return Actions(ele)

    def upload(
        self,
        tag: str,
        file_path: str,
    ):
        """
        上传文件到指定标签页

        参数:
        tag (str): 标签的定位语法
        file_path (str): 上传文件的具体路径

        返回:
        self
        """
        tab = self.newest_page
        tab.set.upload_files(file_path)
        # 定位元素并点击
        tab.ele(tag).click()
        tab.wait.upload_paths_inputted()
        return self

    @property
    def newest_page(self):
        # t=self.page.get_tab[0]
        return self.page.get_tab(self.page.latest_tab)

    @property
    def newest_tab(self):

        return self.page.get_tab(self.page.latest_tab)

    def download_path(self, path):
        self.page.set.download_path(path)
        return self
    def load_js(self, js:str):
        js=Config.current_path()+'\\'+js
        self.newest_page.run_js(js,as_expr=True)
        return self

    def temporary_manual_mode(self):
        self.newest_page.add_ele(outerHTML=Config.add_button)
        self.load_js('Tool.js')
        self.newest_page.run_js('setHoverStyle();')
        while True:
            if not  self.newest_page.ele('#randomButton',timeout=0.2):
                break
            time.sleep(0.2)
        return self
    def god_button(self,name='test',onclick='random()'):
        tab=self.newest_page
        div=tab.ele('#god',timeout=0.3)
        if not div:
            tab.add_ele(outerHTML=Config.god_div)
            tab.add_ele(outerHTML=Config.god_css,insert_to=Config.head)
            div=tab.ele('#god',timeout=0.3)

        out_html=Config.god_button.replace('__按钮',name).replace('__onclick',onclick)
        tab.add_ele(outerHTML=out_html,insert_to=div)
        curr_path=os.path.dirname(os.path.abspath(__file__))
        print(curr_path)
        tab.run_js(curr_path+'\\Tool.js',as_expr=True)

        # tab.run_js('setHoverStyle();')

        return self
    def get_current_file_path(self):
        # 获取当前文件的绝对路径
        current_file = os.path.abspath(__file__)
        # 获取当前文件所在的目录路径
        current_dir = os.path.dirname(current_file)

        return current_dir

    def download(self, url):
        self.page.download(url)
        return self

    def show_title(self):
        print(self.tab.title)
        return self

    def max(self):
        self.page.set.window.max()
        return self

    def min(self):
        self.page.set.window.mini()
        return self

    def hide(self):
        self.page.set.window.hide()
        return self

    def show(self):
        self.page.set.window.show()
        return self

    def wait(self, num: int):
        time.sleep(num)
        return self
    def quit(self,close_all=False):

        if close_all:
            if 'y' in  input('当前模式会关闭所有浏览器进程，包括你自己手动打开的浏览器，是否继续？(y/n)?: '):
                Config.close_chrome()
            else:
                print('已取消')
        else:
            self.page.quit()

    def vip_open(self, url, port: int = 0):
        """
        打开vip页面

        :param url: 要访问的页面链接
        :param port: 端口号，默认为0,范围是0-12
        :return: 返回当前对象
        """
        self.page.get(Config.jiekou[port] + url)
        self.page.wait(2)
        if self.page.ele("/html/body"):
            self.page.ele("/html/body").click()

        return self

    def listen_and_download_file(self,tab:ChromiumTab,file_name='123',file_type='.mp3  ',download_path='.'):

        key=file_type.split(' ')
        print(key)

        tab.listen.start(key)
        tab.refresh()   

        # 开始监听
        for data_packet in tab.listen.steps(count=1):

            song_url=data_packet.url
            print(song_url)

        # 下载音乐
        tab.set.download_path(download_path)
        tab.download(song_url,rename=file_name)
        tab.wait(2)
        tab.close()

    def scan_files(self,tab:ChromiumTab,file_type=['.mp3'],count=10,timeout=100):

        def count_up():
            for i in range(count):
                yield i
        c=count_up()    

        url_list=[]

        key=file_type if type(file_type)==list  else file_type.split(' ')
        print(key)

        tab.listen.start(key)
        tab.refresh()   

        # 开始监听
        print(f'正在从{tab.title} 中扫描 {key} 文件 ...........')

        for data_packet in tab.listen.steps(count=count,timeout=timeout):

            file_url=data_packet.url
            print(next(c),' ',file_url)
        return url_list   

    def scan_files2(self,url,file_type=['mp3'],count=10,timeout=100):
        def count_up():
            i=0
            while True:
                i=i+1
                yield str(i).rjust(3)
        c=count_up()

        def  tihuan(string:str):

            for j in  file_type:
                string=string.replace(j,Fore.GREEN+j+Fore.RESET)
            return string 
        def current_time():
            # 获取当前时间
            current_time = datetime.now()

            # 将当前时间格式化为字符串形式
            time_string = current_time.strftime("%H:%M:%S")

            return Fore.BLUE+time_string+Fore.RESET         

        def _scan():   

            # 开始监听

            for data_packet in tab.listen.steps(count=count,timeout=timeout):

                file_url=data_packet.url

                url_list.append(file_url)
                # print(next(c),' ',file_url)
                print(f' {next(c)} {current_time()} {Fore.RED}{data_packet.resourceType.rjust(7)}{Fore.RESET}    {tihuan(file_url)}')

            print('\n 扫描结束 \n')    

        url_list=[]
        tab=self.page.new_tab(url)
        key=file_type if type(file_type)==list  else file_type.split(' ')
        tab.listen.start(targets=key)
        tab.refresh()   

        print(f'正在从{tab.title} 中扫描 {key} 文件 ...........\n')
        file_type=[ '.'+i   for  i  in  file_type ]

        # print(key)
        init()
        threading.Thread(target=_scan).start()  

    def listen_all(self,file_type=['mp3'],count=10,timeout=100):
        def count_up():
            i=0
            while True:
                i=i+1
                yield str(i).rjust(3)
        c=count_up()

        def  tihuan(string:str):

            for j in  file_type:
                string=string.replace(j,Fore.GREEN+j+Fore.RESET)
            return string[:25]+'...'+string[-25:] 
        def current_time():
            # 获取当前时间
            current_time = datetime.now()

            # 将当前时间格式化为字符串形式
            time_string = current_time.strftime("%H:%M:%S")

            return Fore.BLUE+time_string+Fore.RESET         

        def _scan(t:ChromiumTab,key): 
            t.listen.start(targets=key)
            t.refresh()  

            # 开始监听

            for data_packet in t.listen.steps(count=count,timeout=100):

                file_url=data_packet.url

                # ['序号','time','type','url','tab_url']
                data=[next(c),current_time(),data_packet.resourceType,data_packet.url,t.url]            

                self.listen_all_list.append(data)

                print(f' {data[0]}> [{data[1]}] {Fore.RED}{data[2].rjust(7)}{Fore.RESET}  {tihuan(data[3])}  {Fore.YELLOW+data[4]+Fore.RESET}')

            print(t.url+'\n 扫描结束 \n')    

        init()
        url_list=[]
        tabs=self.page.get_tabs()

        # file_type=[ '.'+i   for  i  in  file_type ]
        key=file_type if type(file_type)==list  else file_type.split(' ')

        print(f'正在扫描 {key} 文件 ...........\n')

        for tt in tabs:
            threading.Thread(target=_scan,args=(tt,key)).start()
            time.sleep(1)

    def load_html2canvas(self):
        js_file=Config.current_dir+'/js/html2canvas.min.js'
        print(f'正在载入js文件:{js_file}')
        self.newest_tab.run_js(js_file)

    def get_screenshot_by_js(self,ele:ChromiumElement,rename='shot.png'):

        shot_code = '''
                html2canvas(this).then(function(canvas) {
                        var img = canvas.toDataURL("image/png");
                        var link = document.createElement('a');
                        link.download = 'screenshot.png';
                        link.href = img;
                        link.id='img_shot';
                        
                        link.click();
                        return img;
                    });

        '''.replace('screenshot.png',rename)

        try:
            ele.run_js(shot_code)
        except:
            self.load_html2canvas()
            # self.newest_tab.ele(f'#su').run_js(shot_code)

            ele.run_js(shot_code)


    async def get_screenshot_by_js_asyc(self, ele: ChromiumElement, rename="shot.png"):

        shot_code = """ async function captureScreenshot() {
    try {
        const canvas = await html2canvas(this);
        
        // 等待一秒钟，确保 Canvas 完全渲染完成
        await new Promise(resolve => setTimeout(resolve, 1000));
        
        const img = await canvas.toDataURL("image/png");
        const link = document.createElement('a');
        link.download = 'screenshot.png';
        link.href = img;
        link.id = 'img_shot';

        return img;
    } catch (error) {
        console.error('Error capturing screenshot:', error);
        return 'error';
    }
}

        """.replace(
            "screenshot.png", rename
        )

        self.load_html2canvas()

        async def run_js_by_async( ele, code):
            return ele.run_js(code)

        img_blob = await run_js_by_async(ele, shot_code)
        return img_blob
    
        # try:
        #     self.load_html2canvas()
        #     aa = await run_js_by_async(ele, shot_code)
        #     return aa
        # except:
        #     self.load_html2canvas()
        #     aa = await run_js_by_async(ele, shot_code)
        #     print(aa)


    def get_screenshot_by_js2(self,ele:ChromiumElement,rename='shot.png'):

        shot_code = '''
        function captureElementScreenshot() {
    // 创建一个新的 SVG 元素
    const element = this;
    const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
    
    // 设置 SVG 的宽度和高度
    svg.setAttribute('width', element.offsetWidth);
    svg.setAttribute('height', element.offsetHeight);

    // 创建一个 foreignObject 元素，用于在 SVG 中嵌入 HTML 内容
    const foreignObject = document.createElementNS('http://www.w3.org/2000/svg', 'foreignObject');
    
    // 设置 foreignObject 的宽度和高度，以匹配目标元素的大小
    foreignObject.setAttribute('width', element.offsetWidth);
    foreignObject.setAttribute('height', element.offsetHeight);
    foreignObject.setAttribute('x', 0);
    foreignObject.setAttribute('y', 0);
    
    // 克隆目标元素，这样可以保留其内容和样式
    const cloneElement = element.cloneNode(true);
    
    // 将克隆的元素添加到 foreignObject 中
    foreignObject.appendChild(cloneElement);
    
    // 将 foreignObject 添加到 SVG 中
    svg.appendChild(foreignObject);
    
    // 序列化 SVG 数据
    const svgData = new XMLSerializer().serializeToString(svg);
    
    // 创建一个新的图像对象
    const img = new Image();

    // 当图像加载完成时，创建一个 canvas 元素并绘制图像
    img.onload = function() {
        const canvas = document.createElement('canvas');
        canvas.width = element.offsetWidth;
        canvas.height = element.offsetHeight;
        const ctx = canvas.getContext('2d');
        ctx.drawImage(img, 0, 0);

        // 将 Canvas 转换为 PNG 数据 URL
        const pngData = canvas.toDataURL('image/png');

        // 创建一个链接元素并触发下载
        const link = document.createElement('a');
        link.download = 'screenshot.png';
        link.href = pngData;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    };

    // 将 SVG 数据转换为 base64 编码，并设置为图像的 src
    img.src = 'data:image/svg+xml;base64,' + btoa(svgData);
    return  img;
}



           
        '''

        tupian:ChromiumElement=ele.run_js(shot_code)

        # self.page.download(src)
        return tupian

    def download_Blob(self,ele:ChromiumElement):

        shot_code = '''
                            
// 获取视频的 Blob URL
var blobUrl = this.src;
alert(blobUrl);

// 使用 Fetch API 获取 Blob 数据
fetch(blobUrl)
    .then(response => response.blob())
    .then(blobData => {
        // 创建一个临时链接
        var downloadLink = document.createElement("a");
        downloadLink.href = URL.createObjectURL(blobData);
        downloadLink.download = "video.ts"; // 下载的文件名

        // 触发点击下载链接的操作
        downloadLink.click();
    })
    .catch(error => {
        console.error("下载视频时出错：", error);
        alert("下载视频时出错：", error);
    });
           
        '''

        ele.run_js(shot_code)
        self.page.wait(10)

    @property
    def jquery(self):
        return Jquery(self)

    def elements(self, k: str, v: str):
        ele = self.tab.eles(f"@{k}={v}")
        return ele

    @staticmethod
    def read_file(file_name):
        with open(file_name, "r", encoding="utf-8") as file:
            content = file.read()
        return content

    def run(self, script_file: str):
        _page = self.newest_page
        _page.run_js(Browser.read_file(script_file))

    def loadjQuery(self):
        if self.newest_page.ele("#jq", timeout=0.2):
            print("jQuery 已经加载")
        else:
            self.newest_page.run_js(r'.\LoadJquery.js')
            print("jQuery 成功加载入页面...")

    def tab(self,n=0):  # 返回最新的标签页
        return self.page.get_tab(n)

    def download_all_img(self, tag):
        """
        从给定的标签中下载所有图片。

        参数:
        self: 当前对象
        tag: 包含要下载图片的标签对象

        返回值:
        self: 返回当前对象
        """
        for i in tag.eles("t:img"):
            for j in ["png", "jpg", "jpeg", "webp", "gif", "tiff"]:
                if j in i.link:
                    self.page.download(i.link)

        return self

    def get_plugin_list(self):
        tab=self.page.new_tab('chrome://extensions/')
        tab.ele('t:body').ele('t:extensions-manager').sr('#toolbar').sr('t:cr-toolbar').ele('t:div').ele('t:cr-toggle').click()

        plugin_list=[]
        for plugin  in  tab.ele('t:extensions-manager').sr('#container').ele('t:cr-view-manager').ele('t:extensions-item-list').sr('t:div@@class=items-container').eles('t:extensions-item'):
            ss=plugin.sr('#content').text.split('\n')[0:4]
            options=f'chrome-extension://{ss[3][3:]}/options.html'

            ss.append(options)

            plugin_list.append(ss)
        return plugin_list  

    def get_bookmarks_list(self):
        tab=self.page.new_tab('chrome://bookmarks/')

        bookmarks_list=[]
        for shu_qian  in  tab.ele('t:bookmarks-app').sr('tag:bookmarks-list').sr('#list').eles('tag:bookmarks-item'):
            ss=shu_qian.sr('#website-text').text

            bookmarks_list.append(ss)
        return bookmarks_list    

# ----------------------截图类


# ----------------jQuery 类----------------
class Jquery:
    cmd2 = """

                    $('.m_slider').css({ 'left': '266px', 'pointer-events': 'none' });
                    $('.flx_v_sildbobx').css({ 'background-color': '#EAFCE4', });
                    $('.m_t_txt').css('display', 'none');
                    $('.m_t_txt_sucess').css('display', 'inline-block');
                    sliderFlag = true;
                    """

    def __init__(self, browser: Browser):
        self.b = browser
        self.cmd = r"""
                    function loadjQuery() {
                  // 创建一个 script 元素
                  var script = document.createElement('script');
                
                  // 设置 script 元素的 src 属性为 jQuery 的 CDN 地址
                  script.src = 'https://code.jquery.com/jquery-3.6.0.min.js';
                  script.id = 'jq';
                
                  // 将 script 元素添加到文档的头部或 body 中
                  document.head.appendChild(script);
                  // 或者使用 document.body.appendChild(script);
                }
                loadjQuery();
                """

        self.load_jquery()

    def load_jquery(self):
        if self.b.newest_page.ele("#jq"):
            print("jQuery 已经加载")
        else:
            self.run(self.cmd)
            print("jQuery 成功加载入页面...")

    def run(self, js_str: str):
        self.b.newest_page.run_js(js_str)
        return self

    def exe(self, js_str: str):  # 有返回值
        return self.b.newest_page.run_js(js_str)


# ------------工具类----------
class Tool:
    @staticmethod
    def get_random_element(input_list) -> ChromiumElement:
        """
        从输入列表中随机选择一个元素并返回。

        :param input_list: 输入的列表
        :return: 随机选择的元素
        """
        if not input_list:
            return None  # 返回 None，如果列表为空

        return random.choice(input_list)

    @staticmethod
    def sniff_and_download_video(
        page, kw: str = 'x://*[@id="post"]/article/div[3]/div'
    ):
        player = page.ele(kw)
        page.actions.wait(2).click(player)
        player.drag(50, 50, 2)
        player.click.at(40, 70)
        print("视频下载中.......")

    @staticmethod
    def sniff_and_download_videos(ele: ChromiumElement):
        # 执行嗅探并下载视频
        player = ele  # 定义变量player，表示ChromiumElement对象

        time.sleep(2)  # 等待2秒
        player.drag(50, 50, 2)  # 拖动player对象到坐标(50, 50)并移动2像素
        player.click.at(40, 70)  # 在坐标(40, 70)处单击player对象
        print("视频下载中.......")  # 打印提示信息"视频下载中......."

    @staticmethod
    def download_img(page):
        for picture in page("@itemprop=articleBody").eles("t:img"):
            picture.save(path=page.title)
            print("saving the picture..." + str(picture.tag))

    @staticmethod
    def click_next(page):
        page.ele("text:下一篇").click()
        time.sleep(3)

    @staticmethod
    def screenshot(ele, name="viewer"):
        ele.get_screenshot(name=name, scroll_to_center=True)

    @staticmethod
    def trees(ele_or_page):
        """把页面或元素对象DOM结构打印出来
        :param ele_or_page: 页面或元素对象
        :return: None
        """
        def _tree(obj, last_one=True, body=''):
            list_ele = obj.children()
            length = len(list_ele)
            body_unit = '    ' if last_one else '│   '
            tail = '├───'
            new_body = body + body_unit

            if length > 0:
                new_last_one = False
                for i in range(length):
                    if i == length - 1:
                        tail = '└───'
                        new_last_one = True
                    e = list_ele[i]

                    attrs = ' '.join([f"{k}='{v}'" for k, v in e.attrs.items()])
                    print(f'{new_body}{tail}<{e.tag} {attrs}>'.replace('\n', ' '))

                    _tree(e, new_last_one, new_body)

        ele = ele_or_page.s_ele()
        attrs = ' '.join([f"{k}='{v}'" for k, v in ele.attrs.items()])
        print(f'<{ele.tag} {attrs}>'.replace('\n', ' '))
        _tree(ele)
    

    @staticmethod
    def tree(ele):
        init()
        e = ele
        print(f"{Fore.BLUE}{Fore.CYAN}<{e.tag}>  {Fore.RESET}{e.attrs}")
        Tool.__tree(e)

    @staticmethod
    def __tree(ele: any, layer=7, has_next_brother=True, body=""):
        if ele.tag == "iframe":
            # ele = page.get_frame(ele)
            ele = ele("x:/html")
            # print(ele.html)
            # print(ele.children())
        try:
            list_ele = ele.children(timeout=0.1)
        except:
            list_ele = []
            print(ele)
            print("无法获取该元素子元素")

        length = len(list_ele)
        body_unit = "│   " if has_next_brother else "    "
        tail = "├───"
        new_body = body + body_unit

        if length > 0 and layer >= 1:
            has_next_brother2 = True
            for i in range(length):
                if i == length - 1:
                    tail = "└───"
                    has_next_brother2 = False
                e = list_ele[i]
                all_body = f"{Fore.BLUE}{new_body}{tail}{Fore.RESET}"

                print(f"{all_body}{Fore.CYAN}<{e.tag}>{Fore.RESET} ")
                Tool.tree_attr(e, all_body, has_next_brother2, layer)

                Tool.__tree(e, layer - 1, has_next_brother2, new_body)

    @staticmethod
    def tree_attr(ele, body, has_next_brother=True, layer=3):
        e: dict = ele.attrs
        has_child = True if ele.tag == "iframe" or ele.child(timeout=0.2) else False

        if layer == 1:
            has_child = False

        part1 = "│" if has_next_brother else " "
        part2 = "│" if has_child else " "
        replace_part = part1 + "   " + part2
        new_body = body.replace("├───", replace_part).replace("└───", replace_part)

        text = "" if ele.tag == "iframe" else ele.text.split("\n")[0]
        if len(text) >= 1:
            e["inner_txt"] = text if len(text) < 150 else text[0:150] + "......"

        if len(e) > 0:
            e["xpath"] = ele.xpath

            max_k_len = max([len(key) for key in e.keys()])
            head = "┌" + "─" * max_k_len + "┐"
            tail = "└" + "─" * max_k_len + "┘"
            print(new_body, head)

            for k, v in e.items():
                key = Fore.GREEN + str(k).ljust(max_k_len) + Fore.RESET + "│"
                content = f"{key}: {v}"

                print(new_body, "│" + key, v)

            print(new_body, tail)


# -----------动作链类----------------------------
class Actions:
    def __init__(self, ele: ChromiumElement) -> None:
        self.e = ele
        pass

    def go_right(self, kw, duration=2, mode="0"):
        if "%" in kw:
            for i in range(20):
                self.e.run_js(
                    rf' this.style.left="{i*5*self.__percentage_to_float(kw)}%" '
                )
                time.sleep(duration / 20)
        else:
            for i in range(20):
                self.e.run_js(rf' this.style.left="{int(kw)/20*i}px" ')
                time.sleep(duration / 20)

        return self

    def go_left(self, kw, duration=2):
        if "%" in kw:
            for i in range(20):
                self.e.run_js(
                    rf' this.style.right="{i*5*self.__percentage_to_float(kw)}%" '
                )
                time.sleep(duration / 20)
        else:
            for i in range(20):
                self.e.run_js(rf' this.style.right="{int(kw)/20*i}px" ')
                time.sleep(duration / 20)

        return self

    def __percentage_to_float(self, percentage):
        value = float(percentage.strip("%")) / 100
        return value


# 工具类

class Use:
    @staticmethod
    def extract_text(s):
        # 直接使用正则表达式提取并返回结果
        return ''.join(re.findall(r'(?<=>)(.+?)(?=<)', s))

    @staticmethod
    def extract_attrs_value(input_string):
        # 直接返回匹配结果
        return re.findall(r'"[^"]+"', input_string)

    @staticmethod
    def extract_attrs_name(input_string):
        # 改进正则表达式以更精确地匹配属性名
        return re.findall(r'\b\w+(?==")', input_string)

    @staticmethod
    def extract_innertext(input_string):
        # 使用正则表达式简化内部文本提取
        match = re.search(r'>(.*?)<', input_string)
        return match.group(1) if match else ''

    @staticmethod
    def raw(input_str):
        input_str = input_str.strip()
        tag_name_match = re.match(r'<(\w+)', input_str)
        tag_name = tag_name_match.group(1) if tag_name_match else ''
        
        tag_attr_values = Use.extract_attrs_value(input_str)
        tag_attr_names = Use.extract_attrs_name(input_str)
        
        attr_all = ''.join([f'@@{name}={value}' for name, value in zip(tag_attr_names, tag_attr_values)])
        attr_all = attr_all.replace('"', '')
        
        txt = Use.extract_text(input_str)
        tag_txt = f'@@text()={txt}' if txt else ''
        
        transformed_str = f'tag:{tag_name}{attr_all}{tag_txt}'
        print(transformed_str)
        return transformed_str

# ---------------- 下面的是测试代码-------------------
if __name__ == '__main__':
    browser1 = Browser(config=' 忽略证书错误  多开   ')
    browser1.open("http://www.baidu.com")
    browser1.page.set.window.location(0,0)


    browser2 = Browser(config=' 忽略证书错误  多开   ')
    browser2.open("https://gitee.com/about_us")
    browser2.page.set.window.location(400,200)

    #退出所有浏览器
    browser1.quit(close_all=True)
