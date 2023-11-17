import requests
import xlsxwriter
from bs4 import BeautifulSoup

def IndiaToday_Chandigarh():
    print("IndiaToday Chd")
    workbook=xlsxwriter.Workbook('IndiaToday_Chandigarh.xlsx')
    worksheet=workbook.add_worksheet()
    row=0
    column=0
    worksheet.write(row,column,"Heading")
    worksheet.write(row,column+1,"Body")
    worksheet.write(row,column+2,"Updated Date")
    worksheet.write(row,column+3,"URL")
    row+=1
    HEADERS = {'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148'}
    r=requests.get('https://www.indiatoday.in/cities/chandigarh-news', headers=HEADERS)
    urls_to_visit=[]
    unique_urls={}
    count=0
    try:
        if(r.status_code==200):
            soup=BeautifulSoup(r.text, 'html.parser')
            for url in soup.findAll('a'):
                try:
                    if(url.has_attr('href')):
                        if("video" not in url['href'].split("/") and "tag" not in url['href'].split("/") and "author" not in url['href'].split("/")):
                            if(url['href'][0]=='/' and "https://www.indiatoday.in/cities/chandigarh"+url['href'] not in unique_urls.keys() and ("chandigarh-news" in url['href'].split("/") or "chandigarh" in url["href"].split("/"))):
                                unique_urls["https://www.indiatoday.in/cities/chandigarh"+url['href']]=True
                                urls_to_visit.append("https://www.indiatoday.in/cities/chandigarh"+url['href'])
                            elif(url['href'][0]=='h' and url['href'].split("/")[2]=="www.indiatoday.in" and url['href'] not in unique_urls.keys() and("chandigarh-news" in url['href'].split("/") or "chandigarh" in url["href"].split("/"))):
                                unique_urls[url['href']]=True
                                urls_to_visit.append(url['href'])
                finally:
                    continue
        while(urls_to_visit and count<2):
                urltoVisit=urls_to_visit[0]
                print(urltoVisit)
                print(count)
                urls_to_visit.pop(0)
            
                if(urltoVisit[0]=='h' and (["tags","tag", "livetv", "video"] not in urltoVisit.split("/"))):
                    try:
                        r=requests.get(urltoVisit, headers=HEADERS)
                        if(r.status_code==200):
                            soup=BeautifulSoup(r.text, 'html.parser')
                            for url in soup.findAll('a'):
                                try:
                                    if(url.has_attr('href')):
                                        if("video" not in url['href'].split("/") and "tag" not in url['href'].split("/") and "author" not in url['href'].split("/")):
                                            if(url['href'][0]=='/' and "https://www.indiatoday.in/cities/chandigarh"+url['href'] not in unique_urls.keys() and ("chandigarh-news" in url['href'].split("/") or "chandigarh" in url["href"].split("/"))):
                                                unique_urls["https://www.indiatoday.in/cities/chandigarh"+url['href']]=True
                                                urls_to_visit.append("https://www.indiatoday.in/cities/chandigarh"+url['href'])
                                            elif(url['href'][0]=='h' and url['href'].split("/")[2]=="www.indiatoday.in" and url['href'] not in unique_urls.keys() and("chandigarh-news" in url['href'].split("/") or "chandigarh" in url["href"].split("/"))):
                                                unique_urls[url['href']]=True
                                                urls_to_visit.append(url['href'])
                                finally:
                                    continue
                            
                            if(soup.find('h1', {'class':'Story_strytitle__MYXmR'}) and (soup.find('html',{'lang':'en'}) or soup.find('html',{'lang':'en-us'}) or soup.find('html',{'lang':'en-uk'}))):
                                heading_title=soup.find('h1', {'class':'Story_strytitle__MYXmR'})
                                print("Yes")
                                if(soup.find('div', {'class':'Story_description__fq_4S'}).findAll('p')):
                                    print("Yes")
                                    
                                    
                                    heading_desc=soup.find('div', {'class':'Story_description__fq_4S'}).findAll('p')
                                    news=""
                                    for text in heading_desc:
                                        
                                        news+=text.text
                                        
                                    updated=soup.find('span',{'class':'strydate'}).text
                                    print(updated)
                        
                                    worksheet.write(row,column,heading_title.text)
                                    worksheet.write(row,column+1,news)
                                    worksheet.write(row,column+2,updated)
                                    worksheet.write(row,column+3,urltoVisit)
                                
                                    row+=1
                                    
                                    count+=1
                    finally:
                        continue        
            
        
    finally:
        print("India today Chandigarh finished")
        workbook.close()