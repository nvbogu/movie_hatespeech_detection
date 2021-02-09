import os
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import time
import re
from urllib.parse import quote
import glob

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
	movie_n_new = movie_n.replace(" ", "")
	movie_n_new = movie_n.replace(",", "")
	movie_n_new = movie_n.replace("?", "")
	movie_n_new = movie_n.replace(".", "")
	with open(os.path.join('movie_subtitles_zips/', movie_n_new+'.zip'), 'wb') as temp_file:
		temp_file.write(urlopen(req4).read())
	with open("movies_written.txt",'a') as mw:
		mw.write(movie_n+'\n')
	print("\n-------------------------------------------------------------------Done ",movie_n)


# get the movie list(can also get from the list of movie names generated)
movie_list = []

for file_name in glob.iglob('movie_names/*.txt', recursive=True):
	with open(file_name,'r') as f:
		movie_list.extend(f.read().split('\n'))

print("Length of total movies obtained: ", len(movie_list))
movie_list = list(set(movie_list))
movie_list = [x for x in movie_list if x]
print("Length of movie list after removing duplicates: ",len(movie_list))

rem_list = []
with open('movies_written.txt','r') as mwr:
	rem_list.extend(mwr.read().split('\n'))

for rem in rem_list: 
    if rem in movie_list:
        movie_list.remove(rem) 

print("Length of movie list after removing already downloads : ",len(movie_list))
for movie in movie_list:
	# create search extension for the movie name
	print("*************MOVIE-- ",movie)
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

