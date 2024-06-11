#!/usr/bin/env python
# -*- coding:utf-8 -*-
# 用这个代码导入需要的库    # pip install  natsort    PyMuPDF  PySimpleGUI



import os
from threading import Thread
import time
from natsort import natsorted
import fitz  # PyMuPDF
import PySimpleGUI as sg
from natsort import natsorted
from colorama import Fore, init
import time



class Tool:   
  

    @staticmethod
    def convert_images_to_pdf(imgdir, output_pdf_name):
        """
        将指定文件夹内的所有图片转换成一个PDF文件。
        
        参数:
        - imgdir: 存放图片的文件夹路径。
        - output_pdf_name: 输出PDF文件的路径。
        """
        doc = fitz.open()  # 创建一个新的空PDF文档
        imglist = os.listdir(imgdir)  # 获取该文件夹内所有文件的列表
        imglist = natsorted(imglist)  # 使用natsorted模块对文件列表进行自然排序
        imgcount = len(imglist)  # 计算文件夹内文件的数量，即图片的数量

        for i, f in enumerate(imglist):
            img = fitz.open(os.path.join(imgdir, f))  # 以文档的形式打开每张图片
            rect = img[0].rect  # 获取图片的尺寸
            pdfbytes = img.convert_to_pdf()  # 将图片转换成PDF格式的字节流
            img.close()  # 关闭图片文档，释放资源
            imgPDF = fitz.open("pdf", pdfbytes)  # 将字节流作为PDF打开
            page = doc.new_page(width=rect.width, height=rect.height)  # 在新PDF中创建一个与图片尺寸相同的新页面
            page.show_pdf_page(rect, imgPDF, 0)  # 将转换得到的PDF内容填充到新页面中

            print(f"导入PDF {f} {i+1}/{imgcount}...")
            
            # 使用PySimpleGUI显示当前的进度
            if not sg.OneLineProgressMeter("导入PDF进度", i+1, imgcount, 'key '+f, orientation='h'):
                print("用户取消操作")
                break  # 如果用户关闭进度条窗口，则退出循环

        doc.save(output_pdf_name)  # 保存PDF文件
        print(f"PDF文件已保存到 {output_pdf_name}") 

    @staticmethod
    def popup_yes_no(info='是否继续？'):
        return sg.popup_yes_no(info)   
    ##  消息提示框
    @staticmethod
    def popup(info='消息提示框！'):
        return sg.popup(info)   
    
    ##  自动消失
    @staticmethod
    def popup_auto_close(info='自动消失的消息提示框！'):
        return sg.popup_auto_close(info,auto_close_duration=5,button_type='POPUP_BUTTONS_YES_NO') 
      
    ##  
    @staticmethod
    def popup_get_text(info='文本输入框！'):
        return sg.popup_get_text(info)   
    ##
    ##  文件选择对话框
    @staticmethod
    def popup_get_file(info='文件选择对话框：'):
        return sg.popup_get_file(info)   
    ##

    ##  强制跳转新标签页
    @staticmethod
    def click_by_force(ele):
        ele.run_js('this.setAttribute("target", "_blank");')   
        ele.run_js('this.click();')   
    ##
        
    ##  命令行线程进度条
    @staticmethod
    def loading_animation():
        n=0
        def thread_progress(t:Thread):
            nonlocal n    
            while t.is_alive():
                for char in "|/-\\":
                    if n==25:
                        n=0
                    dian='#'*n
                    dian2=dian.ljust(25)
                    
                    print(f" Downloading {char} [{dian2}]", end="\r")
                    time.sleep(0.1)

                n=n+1
                
               

        return thread_progress
    ## 树形 监听
    @staticmethod    
    def packet_tree(packet,to_expand='response'):

        def _tree(obj, last_one=True, body='', level=0):
            if obj is None:
                return 1
            
            obj = obj[0] if isinstance(obj, list) and len(obj) !=0 else obj
            if type(obj).__name__=='CaseInsensitiveDict':
                obj=dict(obj)
                pass


            is_dict = isinstance(obj, (dict,))
            not_dict = not is_dict  

            
            show_len = 150
            list_ele = [i for i in dir(obj) if not i.startswith('_')]  if not_dict else obj.keys()

            length = len(list_ele)
            body_unit = '    ' if last_one else '│   '
            tail = '├───'
            new_body = body + body_unit

            if length > 0:
                new_last_one = False
                
                for idx, attr_name in enumerate(list_ele):
                    if idx == length - 1:
                        tail = '└───'
                        new_last_one = True
                    
                    try:
                        packet_attr = getattr(obj, attr_name) if not_dict else obj[attr_name]
                    except:
                        print(f'{attr_name} {obj}  出错！')
                        continue
                    
                    packet_attr_type = type(packet_attr).__name__
                    if    packet_attr_type=='method':
                        continue

                    value = str(packet_attr).split('\n')[0][:show_len]  

                    # 打印属性信息
                    # attr_name=attr_name.ljust(15)
                    if packet_attr_type != 'builtin_function_or_method' : 
                            if packet_attr_type=='dict':
                                print(f'{new_body}{tail}< {Fore.BLUE}{attr_name}{Fore.RESET} {Fore.RED}{packet_attr_type}{Fore.RESET}  ')
                            else:
                                if is_dict:
                                    print(f'{new_body}{tail}# {Fore.GREEN}{attr_name}{Fore.RESET} {Fore.RED}{packet_attr_type}{Fore.RESET}  {value}')
                                else:
                                    print(f'{new_body}{tail}< {Fore.BLUE}{attr_name}{Fore.RESET} {Fore.RED}{packet_attr_type}{Fore.RESET}  {value}')


        

                    # 递归处理特定属性
                    if attr_name in fields_to_expand or packet_attr_type in types_to_expand :
                        _tree(packet_attr, new_last_one, new_body, level + 1)
                




        init()
        # fields_to_expand=['response', 'request', 'body', 'headers', 'values','get']
        fields_to_expand=['get']
        fields_to_expand.append(to_expand)
        types_to_expand=['dict','list']

        print(f'{Fore.YELLOW}{packet}{Fore.RESET}')
        _tree(packet) 


    @staticmethod
    def read_txt_file(file_name):
        try:
            with open(file_name, 'r', encoding='utf-8') as file:
                content = file.read()
                return content
        except FileNotFoundError:
            return "文件未找到，请检查文件名是否正确。"
        except Exception as e:
            return f"读取文件时出错：{e}"  

  
