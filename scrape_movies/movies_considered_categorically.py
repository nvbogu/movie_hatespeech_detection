import os
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import time
import re
from urllib.parse import quote
import glob

from urllib.request import Request, urlopen

got_movies_list = []

with open('movies_written.txt','r') as mwr:
	got_movies_list.extend(mwr.read().split('\n'))

new_got_movies = {}
for val in got_movies_list:
	val_n = val.replace(" ", "")
	val_n = val_n.replace(",", "")
	val_n = val_n.replace("?", "")
	val_n = val_n.replace(".", "")
	new_got_movies[val_n] = val

for filename in glob.glob('wrong/*'):
	print(filename[6:])
	fn = filename[6:]
	if filename in new_got_movies:
		got_movies_list.remove(new_got_movies[filename])

# get the movie list(can also get from the list of movie names generated)
movie_list_friendship = []

with open('movie_names/movie_names_friendship.txt','r') as f:
	movie_list_friendship.extend(f.read().split('\n'))

movie_list_hate = []

with open('movie_names/movie_names_hate-speech.txt','r') as f:
	movie_list_hate.extend(f.read().split('\n'))


movie_list_racism = []

with open('movie_names/movie_names_racism.txt','r') as f:
	movie_list_racism.extend(f.read().split('\n'))

fr = list(set(got_movies_list) & set(movie_list_friendship))
ht = list(set(got_movies_list) & set(movie_list_hate))
rac = list(set(got_movies_list) & set(movie_list_racism))

print('Len from friendship: ', len(fr))
print('Len from Hate speech: ', len(ht))
print('Len from racism: ', len(rac))

print(" FRIENDSHIP-\n",fr)
print("\n\nHATE SPEECH-\n",ht)
print("\n\nRACISM-\n",rac)