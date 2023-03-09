'''
Photopeach Scraper, Written by Tristan Epler 3/9/2023

Photopeach died with adobe flash player, and 
images from albums are only accessible through
photopeach's API.

This program takes the an album ID from the user
and downloads all the images in that album to
a folder named after the album title.
'''


import requests
from xml.etree import ElementTree
import xmltodict
import re
import pandas as pd
import urllib.request
from bs4 import BeautifulSoup
import os

#Photopeach API wants album ID, so we have the user input it
albumID = str(input("Album ID: "))

#assemble url for requests
url = "http://photopeach.com/api/getphotos?album_id=" + albumID

#use url to get response
response = requests.get(url)

#turn xml response into python dictionary
dict_data = xmltodict.parse(response.content)

#turn dictionary into string
string_data = str(dict_data)

#make regex pattern to extract URLs
link_regex = re.compile("((https?):((//)|(\\\\))+([\w\d:#@%/;$()~_?\+-=\\\.&](#!)?)*)", re.DOTALL)

#find links in string_data
urls = re.findall(link_regex, string_data)

#find title using xml/html parser "BeautifulSoup"
soup = BeautifulSoup(response.text, 'html.parser')
htmlAlbumTitle = soup.find('title')

#get string of title, above code returns "<title>[albumTitle]</title>"
albumTitle = htmlAlbumTitle.string
print(albumTitle)

#sanitize the album title to remove any characters windows won't let you put in a folder name, and remove leading/trailing whitespace
SanitizedAlbumTitle = albumTitle.replace("*", "").replace("/", "").replace("\\", "").replace("|", "").replace("\"", "").replace("?", "").replace("<", "").replace(">", "").rstrip().lstrip()

#Use properties inherent in dictionary type to remove duplicate urls (dict wont allow duplicate entries)
unique_links = list(dict.fromkeys(urls))

#find location of this file, for use when creating album folders
cwd=os.getcwd()

# Create a folder to save this album's pics to, if it doesn't exist
album_path = cwd+ "/" + SanitizedAlbumTitle
if not os.path.exists(album_path):
    os.makedirs(album_path)
    print("Folder \'"+SanitizedAlbumTitle+"\' created here: "+album_path)


# Adding headers to our image download requests, so the image hosting website won't know we are a bot
opener=urllib.request.build_opener()
opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
urllib.request.install_opener(opener)


#Now we find the links with images and save them to the album path defined above
stepper=0
for lnk in unique_links:
    #Only want to save links that are images
    if lnk[0].endswith(".jpg"):
        urllib.request.urlretrieve(lnk[0], album_path+"/"+str(stepper)+".jpg")
        print("Written "+album_path+"/"+str(stepper)+".jpg")
        stepper+=1

print("Images all successfully downloaded!")