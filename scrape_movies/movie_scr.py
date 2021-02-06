from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import re

# imdb url lists:

# racism - https://www.imdb.com/search/keyword/?keywords=racism&sort=moviemeter,asc&mode=detail&page=2&ref_=kw_nxt
# friendship- https://www.imdb.com/search/keyword/?keywords=friendship&sort=moviemeter,asc&mode=detail&page=2&ref_=kw_nxt
# hate speech- https://www.imdb.com/search/keyword/?keywords=friendship&sort=moviemeter,asc&mode=detail&page=2&ref_=kw_nxt


# file to save the movie list
genres = ['racism','friendship','hate-speech']

for genre in genres:
	f=open('movie_names_'+genre+'.txt', 'w',encoding="utf-8")
	# k is number of pages to traverse for the link
	for k in range(1,5):
		print(str(k))
		my_url = 'https://www.imdb.com/search/keyword/?keywords='+genre+'&sort=moviemeter,asc&mode=detail&page='+str(k)+'&ref_=kw_nxt'
		print(my_url)
		uClient = uReq(my_url)
		page_html = uClient.read()
		uClient.close()
		page_soup = soup(page_html,"html.parser")

		# filter all the h3 elements which have the movie name
		containers = page_soup.findAll('h3')	
		children = []

		# for every movie name container
		for container in containers:
			# the movie name is in <a> tag, so for every element of container, match and extract movie name
			ch = container.findChildren("a" , recursive=False)
			for c in ch:
				children.append((re.findall(r'<a.*>(.*)<.*', str(c)))[0])

		# write movie names in file
		for child in children:
			f.write("%s" % str(child)+"\n")
	f.close()