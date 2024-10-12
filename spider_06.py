import requests

import pymysql
from lxml import etree
connection=pymysql.connect(host='localhost',
                           user='root',
                           password='12ainipol',
                           database='movie_top250',
                           cursorclass=pymysql.cursors.DictCursor)

headers={
    "user-agent":"Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Mobile Safari/537.36"
}

def get_first_text(list_of_texts):
   if list_of_texts:
       return list_of_texts[0].strip() if list_of_texts[0] is not None else ""
   return ""


#伪装ip
proxies={
    "http":"http://127.0.0.1:7890",
    "https":"http://127.0.0.1:7890"
}

urls = ["https://movie.douban.com/top250".format(str(i * 25)) for i in range(10)]

with connection:
   for url in urls:
       res = requests.get("https://movie.douban.com/top250",headers=headers,proxies=proxies)
       html = res.text
       tree = etree.HTML(html)
       divs = tree.xpath('//div[@class="info"]')

       for index, li in enumerate(divs, start=1):

           # 标题——中文
           title = get_first_text(li.xpath('./div[@class="hd"]/a/span[@class="title"]/text()'))
           # 标题——英文
           title_en=get_first_text(li.xpath('./div[@class="hd"]/a/span[2]/text()'))
           # 网址
           src = get_first_text(li.xpath('./div[@class="hd"]/a/@href'))
           # 导演
           director = get_first_text(li.xpath('./div[@class="bd"]/p/text()'))
           # 类型
           type = get_first_text(li.xpath('./div[@class="bd"]/p/text()'))
           # 评分
           comment = get_first_text(li.xpath('./div[@class="bd"]/div/span[2]/text()'))
           # 评价人数
           valuator=get_first_text(li.xpath('./div[@class="bd"]/div/span[4]/text()'))
           with connection.cursor() as cursor:
               sql = "INSERT INTO movie_top250 (title, title_en, src, director, type, comment, valuator)" \
                     "VALUES(%s,%s,%s,%s,%s,%s,%s)"

               cursor.execute(sql,(title, title_en, src, director, type, comment, valuator))
   connection.commit()