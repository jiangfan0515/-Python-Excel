import re
import urllib.error
import urllib.request

import xlwt
from bs4 import BeautifulSoup


def main():
    baseurl ="http://jshk.com.cn"

    datelist = getDate(baseurl)
    savepath=".\\jshk.xls"
    saveDate(datelist,savepath)

    # askURL("http://jshk.com.cn/")

findlink = re.compile(r'<a href="(.*?)">')
findimg = re.compile(r'<img.*src="(.*?)"',re.S)
findtitle = re.compile(r'<span class="title">(.*)</span')
findrating = re.compile(r'<span class="rating_num" property="v:average">(.*)</span')
findjudge = re.compile(r'<span>(\d*)人评价</span>')
findinq= re.compile(r'<span class="inq">(.*)</span>')

def getDate(baseurl):
    datalist =[]
    for i in range(0,10):
        url=baseurl+str(i*25)
        html=askURL(url)
        soup = BeautifulSoup(html,"html.parser")
        for item in soup.find_all('div',class_="item"):
            data = []
            item = str(item)
            link = re.findall(findlink,item)[0]
            data.append(link)
            img=re.findall(findimg,item)[0]
            data.append(img)
            title=re.findall(findtitle,item)[0]

            rating=re.findall(findrating,item)[0]
            data.append(rating)
            judge=re.findall(findjudge,item)[0]
            data.append(judge)
            inq=re.findall(findinq,item)

            if len(inq)!=0:
                inq=inq[0].replace("。","")
                data.append(inq)
            else:
                data.append(" ")
            print(data)
            datalist.append(data)
        print(datalist)
    return datalist

def askURL(url):
    head = { 
   "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36"}
    request=urllib.request.Request(url,headers=head)
    html=""
    try:
        response=urllib.request.urlopen(request)
        html=response.read().decode("utf-8")
        # print(html)
    except urllib.error.URLError as e:
        if hasattr(e,"code"):
            print(e.code)
        if hasattr(e,"reason"):
            print(e.reason)

    return html

def saveDate(datalist,savepath):
    workbook = xlwt.Workbook(encoding='utf-8')
    worksheet = workbook.add_sheet('电影',cell_overwrite_ok=True)
    col =("电影详情","图片","影片","评分","评价数","概况")
    for i in range(0,5):
        worksheet.write(0,i,col[i])
    for i in range(0,250):
        print("第%d条" %(i+1))
        data=datalist[i]
        for j in range(0,5):
            worksheet.write(i+1,j,data[j])

    workbook.save(savepath)



if __name__ == '__main__':
    main()
    print("爬取完毕")
————————————————
版权声明：本文为CSDN博主「q56731523」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
原文链接：https://blog.csdn.net/weixin_44617651/article/details/129703015
若要更改爬取网站，则需要更改URL以及相应的html格式（代码中的“item”）
