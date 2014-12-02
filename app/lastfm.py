#coding:utf-8

import urllib
import urllib2
import xml.etree.ElementTree as etree
import os

base_url="http://ws.audioscrobbler.com/2.0"
api_key="8e4a879b21145f24ae09dae366f086d3"

def download_user_artists(username):
	url = base_url + \
			"/?method=library.getartists" + \
			"&api_key=" + api_key + \
			"&user=" + username + \
			"&limit=0"
	print url
	# xmldata = urllib2.urlopen(url).read()
	xmldata= urllib.URLopener()
	saveto = '/tmp/' + username + '.xml'
	xmldata.retrieve(url, saveto)
	return saveto
	
def user_artists(username):
	xmldata = '/tmp/' + username + '.xml'
	if not os.path.isfile(xmldata):
		download_user_artists(username)
	tree = etree.parse(xmldata)
	root = tree.getroot()
	response = []
	for artist in root.findall("./artists/artist/name"):
		response.append(artist.text)
	return response
