import asyncio
from DrissionPage import ChromiumPage
from DataRecorder import Recorder


async def collect_data(tab, recorder,title, num=1):
      
    # 遍历所有标题元素
    for i in tab.eles('.title project-namespace-path'):
        # 获取某页所有库名称，记录到记录器
        recorder.add_data((title, i.text,title, num))

    # 查找下一页按钮
    btn = tab('@rel=next', timeout=2)
    if btn:
        # 如果有下一页，点击翻页
        btn.click(by_js=True)
        await asyncio.sleep(0.2)                
        await collect_data(tab, recorder,title, num + 1)

async def main():
    # 新建页面对象
    page = ChromiumPage()
    
    # 获取第一个标签页对象
    tab1 = page.new_tab('https://gitee.com/explore/ai')
    # 新建一个标签页并访问另一个网址
    tab2 = page.new_tab('https://gitee.com/explore/machine-learning')
    # 新建记录器对象
    recorder = Recorder('data.csv')
 
    task1=asyncio.create_task(collect_data(tab1, recorder, 'ai'))
    task2=asyncio.create_task(collect_data(tab2, recorder, '机器学习'))

    await task1
    await task2

if __name__ == '__main__':
    asyncio.run(main())
