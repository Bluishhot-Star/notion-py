from bs4 import BeautifulSoup
import requests
from datetime import *
def IT():
    source = 'INPUT SOURCE URL'
    IT_NewsList = []
    for i in range(1, 3): #Set pages to crawl
        #======Customizing queries======
        postfix = '?page=' + str(i)
        req = requests.get(source+postfix)
        #===============================
        
        soup = BeautifulSoup(req.content.decode('UTF-8', 'replace'), "html.parser")

        # Select container of news list
        rawnews = soup.select('.list-cover')

        for onenews in rawnews[0]:
            #======Customizing HERE======
            #Example
            title = onenews.select('div > div.flex-box.list-item-box > div.item-main.text900 > a.item-title.link-text.link-underline.text900')[0].text
            newsurl = onenews.select('div > div.flex-box.list-item-box > div.item-main.text900 > a.item-title.link-text.link-underline.text900')[0].get('href')
            published_date = onenews.select('div > div.flex-box.list-item-box > div.item-main.text900 > div > div:nth-child(4)')[0].text
            now = datetime.now()
            create_date = "%s-%02d-%s %02d:%02d:%02d" % (now.year, now.month, now.day, now.hour, now.minute, now.second)

            #Block Object
            crawling_one_news = {
                '기사 제목' : title,
                '기사 링크' : "https://yozm.wishket.com"+newsurl,
                '기사 날짜' : published_date,
                '출처' : '요즘IT',
                '크롤링 날짜' : create_date
            }

            IT_NewsList.append(crawling_one_news)

    return IT_NewsList




from enex2notion import *
from notion.block import *
from notion.client import *

# Define Schema
def get_collection_schema():
    return {
        "title" : {"name" : "title", "type" : "text"},
        "url" : {"name" : "url", "type" : "url"},
        "crawlingDate" : {"name" : "crawlingdate", "type" : "text"},
        "publishedDate" : {"name" : "publisheddate" , "type" : "text"},
        "source" : {"name" : "source", "type" : "text"},
    }

# 
token = "INPUT YOUR tokenv2" 
url = "INPUT YOUR URL of Notion page" 

client = NotionClient(token_v2=token)
page = client.get_block(url)

child_page = page.children.add_new(CollectionViewPageBlock)
child_page.collection = client.get_collection(
    client.create_record('collection', parent=child_page, schema=get_collection_schema())
)

child_page.title = "SET TITLE"

#Get data
news = IT()

for onenews in news:
    row = child_page.collection.add_row() # Create new row
    #======Set Property======
    row.set_property("title", onenews['기사 제목'])
    row.set_property("source", onenews['출처'])
    row.set_property("publishedDate", onenews['기사 날짜'])
    row.set_property("crawlingDate", onenews['크롤링 날짜'])
    row.set_property("url", onenews['기사 링크'])

# Add page (e.g. by table type)
view = child_page.views.add_new(view_type='table')
