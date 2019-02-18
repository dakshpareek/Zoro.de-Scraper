import requests,os,lxml,re,json
from bs4 import BeautifulSoup

def save_data(temp_data):
  f=open('all_urls.txt','a')
  f.writelines(temp_data)
  f.close()

html=requests.get('https://www.zoro.de/')
soup = BeautifulSoup(html.text, 'lxml')
m1=soup.findAll('ul',{'class':'level0 submenu'})
#print(len(m1))
all_a=m1[0].findAll('a')
temp=[]
#print('http://dada/dsadfds'.count('/'))

for i in all_a:
  if i.attrs['href'].count('/')==3:
    temp.append(i.attrs['href'])
    #print(i.attrs['href'])
temp=list(set(temp))
all_cat_urls=[]
for cat in temp:
  #print(cat)
  html1=requests.get(cat)
  soup1 = BeautifulSoup(html1.text, 'lxml')
  m2=soup1.findAll('div',{'class':'filter-options-content filter-items-container'}) 
  for i in m2[0].findAll('a'):
    all_cat_urls.append(i.attrs['href'])


all_links_here=[]

#https://www.zoro.de/messen-prufen-testen/messgerate-elektrik?followSearch=10000&product_list_limit=60&p=1
url2='?followSearch=10000&product_list_limit=60&p='

for every_url in all_cat_urls[1:]:
  print('page:1')
  print(every_url+url2+'1')
  html2=requests.get(every_url+url2+'1')
  soup2 = BeautifulSoup(html2.text, 'lxml')
  pages=soup2.find('li',{'class':'item total'})
  try:
    pages=int(pages.text.split()[-1])
  except:
    pages=1
  print('Total Pages:'+str(pages))
  all_links=soup2.findAll('a',{'class':'product-item__photo-link'})
  for i in all_links:
    all_links_here.append(i.attrs['href']+ '\n' )
  print('---Done---')
  if pages>=2:
    for i in range(2,pages+1):
      print('page:'+str(i))
      print(every_url+url2+str(i))
      html3=requests.get(every_url+url2+str(i))
      soup3 = BeautifulSoup(html3.text, 'lxml')
      all_links=soup3.findAll('a',{'class':'product-item__photo-link'})
      for j in all_links:
        all_links_here.append(j.attrs['href']+ '\n')
      print("---Done---")
print('Result:'+str(len(all_links_here)))
save_data(all_links_here)