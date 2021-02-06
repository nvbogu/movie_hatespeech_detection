import os
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import time
import re
from urllib.parse import quote

from urllib.request import Request, urlopen


# using the download url, download the subtitles in a zip file 
def download_zip(url,movie_n):
	
	req3 = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
	page_html3 = urlopen(req3).read()
	page_html3=page_html3.decode(encoding='utf-8',errors=	'ignore')
	
	page_soup3 = soup(page_html3,"html.parser")
	
	containers3 = page_soup3.find("a", { "class" : "btn-icon download-subtitle" }) 
	
	download_url = 'https://yifysubtitles.org'+(re.findall(r'<a .*href="(.*)"><span.*', str(containers3))[0])
	print('NEWEST URL--\n',str(download_url))
	req4 = Request(download_url, headers={'User-Agent': 'Mozilla/5.0'})
	f1=open("movie_subtitles/"+movie_n+'.zip','wb+')
	f1.write(urlopen(req4).read())
	f1.close()


# get the movie list(can also get from the list of movie names generated)
movie_list = ["BlacKkKlansman","Talk Radio","Woodlawn","The Red Pill","The Intruder","Der ewige Jude","Shut Him Down: The Rise of Jordan Peterson","The Intruder"]


for movie in movie_list:
	# create search extension for the movie name
	extension = ''
	if len(movie.split(' '))>1:
		sp = movie.split(' ')
		for s in sp:
			extension+=quote(str(sp))+'+'
	else:
		extension = movie
		
	# search the site for movie
	my_url = "https://yifysubtitles.org/search?q="+extension
	req = Request(my_url, headers={'User-Agent': 'Mozilla/5.0'})
	page_html = urlopen(req).read()
	page_html=page_html.decode(encoding='utf-8',errors=	'ignore')
	
	page_soup = soup(page_html,"html.parser")
	
	# get the first value from the searched page and get it's URL
	containers = page_soup.find("div", { "class" : "media-left media-middle" }) 
	
	if containers:
		children = []
		ch = containers.findChildren("a" , recursive=False)
		new_url = 'https://yifysubtitles.org'+(re.findall(r'<a href="(.*)" itemprop="url".*', str(ch[0]))[0])
		print('NEW URL--\n',new_url)

		# open the movie subtitle page and look for english subtitles
		req2 = Request(new_url, headers={'User-Agent': 'Mozilla/5.0'})
		page_html2 = urlopen(req2).read()
		page_html2=page_html2.decode(encoding='utf-8',errors=	'ignore')
		
		page_soup2 = soup(page_html2,"html.parser")

		table = page_soup2.find('table', attrs={'class':'table other-subs'})

		table_body = table.find('tbody')

		rows = table_body.find_all('tr')
		for row in rows:
		    cols = row.find_all('td')
		    cols_parsed = [ele.text.strip() for ele in cols]
		    # when english subtitle found, capture the download url for the same
		    if cols_parsed[1]=='English':
		    	print(len(cols))
		    	download_url = 'https://yifysubtitles.org'+re.findall(r'<a href="(.*)"><span.*', str(cols[2]))[0]
		    	print(download_url)
		    	download_zip(download_url, movie)
		    	break

