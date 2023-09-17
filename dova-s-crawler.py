
# -*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup
import os
import time
import re
import random
from tkinter import *
from tkinter.filedialog import askdirectory

se = requests.session()


class Dova_s_bgm():

    def __init__(self):
        self.temp_num=0
        print("制作：Container_Z")
        print("个人主页：Container-z.cn\n")
        print("【请注意：部分曲目可能有一定程度的版权限制，在商用前请详询Dova-S对应页面，由此软件产生的版权纠纷本人概不负责！】\n")
        print("SQL查询语句预设：")
        dict = {'光明': 'run.html?tags=m01', '快乐': 'run.html?tags=m02', '温暖': 'run.html?tags=m03', '平静': 'run.html?tags=m04', '友好': 'run.html?tags=m05','清爽': 'run.html?tags=m30', 
               '时髦': 'run.html?tags=m31', '力量': 'run.html?tags=m32', '微弱': 'run.html?tags=m33', '怀念': 'run.html?tags=m06', '怀疑': 'run.html?tags=m07', '嘈杂': 'run.html?tags=m08', 
               '可爱': 'run.html?tags=m09', '晦涩': 'run.html?tags=m10','严重': 'run.html?tags=m28', '紧张': 'run.html?tags=m34', '谦虚': 'run.html?tags=m12', '孤独': 'run.html?tags=m13', 
               '伤感': 'run.html?tags=m14', '冰冷': 'run.html?tags=m15', '黑暗': 'run.html?tags=m16', '悲哀': 'run.html?tags=m17', '愤怒': 'run.html?tags=m18', '恐惧': 'run.html?tags=m19', 
               '暴力': 'run.html?tags=m20',  '暴力': 'run.html?tags=m21','赛博': 'run.html?tags=m22','幻想曲': 'run.html?tags=m23', '恶意': 'run.html?tags=m24', '可疑': 'run.html?tags=m25',
                '日常': 'run.html?tags=m35', '热情': 'run.html?tags=m36', '冷静': 'run.html?tags=m37', '淡白': 'run.html?tags=m38', '希望': 'run.html?tags=m27',
               '绝望': 'run.html?tags=m26', '虚无': 'run.html?tags=m29'};
        for key,value in dict.items():
            self.temp_num+=1
            if self.temp_num%3 is 0:
                print(key+':'+str(value))
            else:
                print(key+':'+str(value),end="   ")
        root = Tk()
        root.withdraw()
        self.input_url = input("\n请输入待爬取的网页尾部SQL查询语句\n(输入错误将自动从无分类标签中下载):\n")
        self.input_mum = input("\n输入起始页码\n(输入错误将自动从第一页下载):\n")
        if self.input_mum.isdigit():
            pass
        else:
            print("输入错误，将自动从第一页开始下载")
            self.input_mum = 1
        self.load_path = 'D:\Studio\BGM'
        self.input_yn = input("\n是否自定义下载路径(为空或\"n\"默认下载至"+self.load_path+")？（y or n）:")
        if self.input_yn is "y":
            self.load_path = askdirectory()
        self.tag_url="https://dova-s.jp/_contents/settingSound/"+self.input_url
        self.target_url = 'https://dova-s.jp/bgm/index.html?page='
        self.main_url = 'https://dova-s.jp'
        self.headers = {
            'Referer': 'https://dova-s.jp/',
            'Accept-Language':'zh-CN,zh;q=0.8,ja;q=0.6,en-US;q=0.4,en;q=0.2',
            #'Accept-Encoding':'gzip, deflate, br',
            #'Cache-Control':'max-age=0',
            'Connection':'keep-alive',
            #'Host':'dova-s.jp',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:63.0) Gecko/20100101 Firefox/63.0'
        }
        self.pass_download = False
        

    def login(self):
        se.post(self.tag_url,headers=self.headers)

    def get_form(self,jump_to_url):
        data={
            'playerSelect': 2
            }
        try:
            se.post(jump_to_url, data=data, headers=self.headers)
        except:
            print('被网站拒绝访问，再次尝试中')
            self.get_form(jump_to_url)


    def get_html(self, url, timeout):
        try:
            return se.get(url, headers=self.headers, timeout=timeout)
        except:
            print('获取网页出错,5秒后将会重新获取')
            time.sleep(5)
            return self.get_html(url, timeout)


    def get_bgm(self, html, page_num):
        li_soup = BeautifulSoup(html, 'lxml')  # 传入第page_num页的html
        li_list = li_soup.find_all('dl', attrs={'class', 'item'})   # 找到dl所在位置
        # print('get_list succeed')
        #print(li_list)
        for li in li_list:
            href = li.find('a')['href']  # 直接提取第一个href
            # print('get_href succeed')
            #print(href)
            jump_to_url = self.main_url + href  # 跳转到目标的url
            self.get_form(jump_to_url)
            #print(jump_to_url)
            # print('get_jump_to_url succeed')
            jump_to_html = self.get_html(jump_to_url, 3).text  # 获取音频网页的html
            #print('get_jump_to_html succeed'+jump_to_html)

            try:
                bgm_soup = BeautifulSoup(jump_to_html, 'lxml')
                bgm_info = bgm_soup.find(id="HTML5").find_all(name='script')
                bgm_info = re.findall( r'[a-zA-z]+://[^\s]*.mp3', str(bgm_info), re.M|re.I)
                id_info = bgm_soup.find('div', attrs={'class', 'contents'}).find('div', attrs={'class', 'titleArea'}).find(name='p').getText()


                print(str(bgm_info[0]))
                #print(id_info)
                # 找到目标位置的信息
                if bgm_info is None:  # 找不到的url,直接continue
                    continue
                self.download_bgm(bgm_info, jump_to_url, page_num,id_info)  # 下载
            except: 
                 print('该音频资源404，可能网站上已经下架，程序将跳过此音频下载')

    def download_bgm(self, bgm_info, href, page_num,id_info):
        title = id_info # 提取标题
        src = bgm_info[0]  # 提取音频地址
        src_headers = self.headers
        src_headers['Referer'] = href  # 加一个referer,否则403
        #src_headers['Host'] = 'dova2.heteml.jp'  
        #src_headers['Accept'] ='audio/webm,audio/ogg,audio/wav,audio/*;q=0.9,application/ogg;q=0.7,video/*;q=0.6,*/*;q=0.5'


        title = title.replace('?', '_').replace('/', '_').replace('\\', '_').replace('*', '_').replace('|', '_')\
            .replace('>', '_').replace('<', '_').replace(':', '_').replace('"', '_').strip()
        if os.path.exists(os.path.join(self.load_path, str(page_num), title + '.mp3')):
            print('文件为'+ title + ' 的音频已存在，跳过下载')
            return
        try:
            #print(src_headers)
            html = requests.get(src, headers=src_headers,timeout=10)
            bgm = html.content
        except:  
            print('获取该音频失败，即将再次访问')
            self.download_bgm(bgm_info, href, page_num,id_info)
            #print('获取该音频失败')
            #return False


        # 过滤非法文件名

        #if os.path.exists(os.path.join(self.load_path, str(page_num), title + '.mp3')):
            #for i in range(1, 100):
            #    if not os.path.exists(os.path.join(self.load_path, str(page_num), title + str(i) + '.mp3')):
            #        title = title + str(i)
            #        break
        # 如果重名了,就加上一个数字
        #print('正在保存名字为: ' + title + ' 的音频')
        #with open(title + '.mp3','ab') as f:  # 以ab二进制保存
        #    f.write(bgm)
        #print('保存该音频完毕')
        if os.path.exists(os.path.join(self.load_path, str(page_num), title + '.mp3')):
            print('访问成功')
            return
        else:
            print('正在保存名字为: ' + title + ' 的音频')
            with open(title + '.mp3','ab') as f:  # 以ab二进制保存
                f.write(bgm)
            print('保存该音频完毕')


    def mkdir(self, path):
        path = path.strip()
        is_exist = os.path.exists(os.path.join(self.load_path, path))
        if not is_exist:
            print('创建一个名字为 ' + path + ' 的文件夹')
            os.makedirs(os.path.join(self.load_path, path))
            os.chdir(os.path.join(self.load_path, path))
            return True
        else:
            print('名字为 ' + path + ' 的文件夹已经存在')
            os.chdir(os.path.join(self.load_path, path))
            return False

    def work(self):
        self.login()
        print('\n文件将保存在：'+self.load_path+"\n")
        for page_num in range(int(self.input_mum), 10000):  # 设置页数
            try:
                if os.path.getsize(os.path.join(self.load_path, str(page_num-1))):
                    pass
                else:
                    if os.path.getsize(os.path.join(self.load_path, str(page_num-2))):
                        pass
                    else:
                        if os.path.getsize(os.path.join(self.load_path, str(page_num-3))):
                            pass
                        else:
                            print("\n已全部下载完成，最后三个文件夹为空是正常现象，请手动删除！\n")
                            return
            except:
                pass
            path = str(page_num)  # 每一页开一个文件夹
            self.mkdir(path)  # 创建文件夹
            #print(self.target_url + str(page_num))
            now_html = self.get_html(self.target_url + str(page_num), 3)  # 获取页码
            self.get_bgm(now_html.text, page_num)  # 获取音频
            print('第 {page} 页保存完毕'.format(page=page_num))
            #time.sleep(2)  # 防止太快被反

dova_s_bgm = Dova_s_bgm()
dova_s_bgm.work()