#-*- coding: utf-8 -*-
import re
import requests
import codecs

class Spider(object):
    def __init__(self):
        print('开始爬虫....')
#get_source获取当前网页的源代码

    def get_source(self, url):
        html = requests.get(url)
        return html.text
#change_page实现翻页的功能，并保存所有url

    def change_page(self, url, total_page):
        now_page = int(re.search('pageNum=(\d+)', url, re.S).group(1))
        page_group = []
        for i in range(now_page, total_page+1):
            link = re.sub('pageNum=(\d+)', 'pageNum=%d'%i, url, re.S)
            page_group.append(link)
        return page_group
#geteachclass获取所有课程的块信息

    def get_allclass(self, source):
        allclass = re.findall('(" target="_blank".*?</li>)', source, re.S)
        return allclass
#getinfor从每个课程块中提取信心

    def getinfor(self, eachclass):
        infor = {}
        infor['title'] = re.search('title="(.*?)"', eachclass, re.S).group(1)
        infor['content'] = re.search('display: none;">(.*?)</p>', eachclass, re.S).group(1)
        timeandlevel = re.findall('</i><em>(.*?)</em>', eachclass, re.S)
        infor['time'] = (timeandlevel[0]).replace(' ','')
        infor['level'] = timeandlevel[1]
        infor['learn_num'] = re.search('<em class="learn-number">(.*?)</em>', eachclass, re.S).group(1)
        return infor

    def saveinfor(self, classinfor):
        f = open('infor.txt', 'a', encoding='utf-8')
        for each in classinfor:
            f.writelines('title' + '\t\t\t' + each['title'] + '\n')
            f.writelines('content' + '\t' + each['content'] + '\n')
            # a = each['content']
            # a = a.lstrip()
            f.writelines('time' + '\t' + each['time'].replace(' ', '') + '\n')
            f.writelines('level' + '\t' + each['level'] + '\n')
            f.writelines('learn_num' + '\t' +each['learn_num'] +'\n')
            f.writelines('\t\t#***************************#' + '\n')
        f.close()
if __name__ == '__main__':
    classinfor = []
    url = 'http://www.jikexueyuan.com/course/?pageNum=1'
    fsh = Spider()
    all_links = fsh.change_page(url, 10)
    # print(all_links)
    for link in all_links:
        print('正在处理'+link)
        html = fsh.get_source(link)
        allclass = fsh.get_allclass(html)
        allclass.pop(0)
        for x in range(len(allclass)):
            infor = fsh.getinfor(allclass[x])
        # for each in allclass:
        #     infor = fsh.getinfor(each)

            classinfor.append(infor)

    fsh.saveinfor(classinfor)

