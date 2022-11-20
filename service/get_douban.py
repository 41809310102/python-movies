import random
import re  # 正则表达式，进行文字匹配
import time

import requests
import xlwt  # 进行excel操作
from bs4 import BeautifulSoup  # 网页解析，获取数据
# 生成词云数据
from wordcloud import WordCloud
import xlrd

# 1.获取影片超链接的规则
findLink = re.compile(r'<a href="(.*?)">')  # 生成正则表达式对象，表示规则（字符串的模式）
# 2.影片图片
findImgSrc = re.compile(r'<img.*src="(.*?)"', re.S)  # S忽略换行
# 3.影片片名
findTitle = re.compile(r'<span class="title">(.*)</span>')
# 4.影片评分
findRating = re.compile(r'<span class="rating_num" property="v:average">(.*)</span>')
# 5.影片评价人数
findJudge = re.compile(r'<span>(\d*)人评价</span>')
# 6.影片概况
findInq = re.compile(r'<span class="inq">(.*)</span>')
# 7.影片相关信息
findBd = re.compile(r'<p class="">(.*?)</p>', re.S)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/97.0.4692.71 Safari/537.36',
}

ip_list = []


def getHtml(url, headers):
    response = requests.get(url, headers=headers)
    response.encoding = "utf-8"
    return response.text


# 得到指定一个URL的网页内容
def askURL(url):
    # 根据url获取html
    res = requests.get(url, headers=headers)
    # 从网页的内容中分析网页编码的方式
    res.encoding = res.apparent_encoding
    return res.text


# Step1.爬取网页
def getData(baseurl):
    print("getData...")
    datalist = []  # 创建电影列表
    for i in range(0, 10):  # 调用获取页面信息的函数，10次，25条/页
        url = baseurl + str(i * 25)
        time.sleep(3)
        askURL(url)
        html = askURL(url)  # 保存获取到的网页源码
        # Step2.逐一解析数据
        soup = BeautifulSoup(html, "html.parser")  # 对象，解析器
        num = i * 25 + 1
        for item in soup.find_all('div', class_="item"):  # 查找符合要求的字符串，形成列表
            data = [num]  # 保存一部电影的所有信息
            item = str(item)
            # print(item)     # 测试：查看电影Item全部信息
            # break

            # 1.获取影片超链接
            link = re.findall(findLink, item)[0]  # re库通过正则表达式查找指定的字符串
            data.append(link)
            # 2.影片图片
            imgSrc = re.findall(findImgSrc, item)[0]
            data.append(imgSrc)
            # 3.影片片名
            titles = re.findall(findTitle, item)
            if len(titles) == 2:
                ctitle = titles[0]  # 添加中文名
                data.append(ctitle)
                otitle = titles[1].replace("/", "")  # 去掉无关符号
                otitle = re.sub(' ', "", otitle)  # 替换，去除空格
                otitle = re.sub('( )+', "", otitle)  # 替换，去除空格
                data.append(otitle)  # 添加外文名
            else:
                data.append(titles[0])
                data.append(' ')  # 外文名空
            # 4.影片评分
            rating = re.findall(findRating, item)[0]
            data.append(rating)
            # 5.影片评价人数
            judgeNum = re.findall(findJudge, item)[0]
            data.append(judgeNum)
            # 6.影片概况
            inq = re.findall(findInq, item)
            if len(inq) != 0:
                inq = inq[0].replace(".", "")
                data.append(inq)
            else:
                data.append(" ")
            # 7.影片相关信息
            bd = re.findall(findBd, item)[0]
            bd = re.sub('<br(\s+)?/>', " ", bd)  # 替换，去除标签
            bd = re.sub('/', " ", bd)  # 替换，去除斜杠
            bd = re.sub(' ', "", bd)  # 替换，去除空格
            bd = re.sub('( )+', "", bd)  # 替换，去除空格
            data.append(bd.strip())  # 去空格
            num += 1  # 呼号
            # 将一部电影信息添加到电影列表
            print(data)  # 在控制台上打印
            datalist.append(data)

    # 测试：在控制台打印信息
    return datalist


# Step3.保存数据
def saveData(datalist, savepath):
    print("saveData...")
    book = xlwt.Workbook(encoding="utf-8", style_compression=0)  # 创建Workbook对象
    sheet = book.add_sheet('豆瓣电影Top250', cell_overwrite_ok=True)  # 创建工作表
    col = ("序号", "电影详情链接", "图片链接", "影片中文名", "影片外文名", "评分", "评价人数", "概况", "相关信息")
    for i in range(0, 8):
        sheet.write(0, i, col[i])  # 列名
    for i in range(0, 250):
        data = datalist[i]
        print(data)
        for j in range(0, 8):
            sheet.write(i + 1, j, data[j])  # 数据

    book.save(savepath)  # 保存


# 2.解析html
def parseHtml(htmlCode):
    # Windows 请运行在 cmd上pip install lxml-3.7.3-cp36-cp36m-win_amd64.whl
    # soup = BeautifulSoup(htmlCode, 'html.parser')
    soup = BeautifulSoup(htmlCode, 'html.parser')
    trs = soup.select("#list > table > tbody > tr")
    for tr in trs:
        tds = tr.find_all("td")
        ip = tds[0].get_text()
        ip_list.append(ip)
    return ip_list


# Step0.程序执行时
def main():
    print("开始爬取豆瓣电影...")
    baseurl = "https://movie.douban.com/top250?start="
    # Step1.爬取网页；Step2.逐一解析数据
    datalist = getData(baseurl)
    savepath = "./豆瓣.xls"
    # Step3.保存数据
    saveData(datalist, savepath)  # 保存数据到Excel


# 获取top10信息
def getap10_douban():
    # 电影top10
    data = xlrd.open_workbook('./豆瓣.xls')

    table = data.sheets()[0]
    # nrows = table.nrows  # 行数
    #
    # ncols = table.ncols  # 列数
    arr_name = []
    for i in range(1, 11):
        row = table.row_values(i)  # 某一行数据
        arr_name.append(row[3])
    return arr_name


def getcloud_chart():
    w = WordCloud(background_color="white", font_path="./SimplifiedChinese/SourceHanSerifSC-SemiBold.otf")  # font_path="msyh.ttc"，设置字体，否则显示不出来
    text = ''
    data = getap10_douban()
    for s in data:
        text += s+"\n"
    w.generate(text)
    w.to_file("../static/img/doubanTop10cloud.png")


# 豆瓣电影程序入口（主方法）
if __name__ == "__main__":
    # 调用函数
    # main()
    getcloud_chart()
    print("爬取完毕")
