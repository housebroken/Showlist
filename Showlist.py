#!/usr/bin/env python

from bs4 import BeautifulSoup
import urllib2
from collections import defaultdict
import xml.etree.ElementTree

def scrape():  # Scrape the data for all h4 and table elements.
	from bs4 import BeautifulSoup
	import urllib2
	html_doc = urllib2.urlopen('http://www.showlistaustin.com')
	soup = BeautifulSoup(html_doc)
	h4 = soup.find_all("h4")
	h4 = h4[6:]
	table = soup.find_all("table")
	scrapeddata = [h4, table]
	return scrapeddata

def get_dates(scrapeddata):  # Grab the dates from the h4 elements found after scrape.
	h4 = scrapeddata[0]
 	dates = []
	for i in range(len(h4)):
		tag = h4[i].find_all("b")
		for i in range(len(tag)):
			thing = tag[i].get_text()
			dates.append(str(thing))
	return dates


def get_events(scrapeddata):  #  Grab the events from the table elements found after scrape.
	table = scrapeddata[1]
	events = []
	rough = []
	draft = []
	final = []
	for i in range(len(table)):
		for string in table[i].stripped_strings:
			if len(string) >= 3:
				rough.append(string)
			else:
				pass
		events.append(rough)
		rough = []
	for i in range(len(events)):
		for y in range(len(events[i])):
			item = str(events[i][y]).lower()
			the = "the"
			at = "at"
			if item[-3:] == the:
				draft.append(item[:-7]) 
			elif item[-2:] == at:
				draft.append(item[:-3])
			else:
				pass
		final.append(draft)
		draft = []
		new_final = []
		new_day = []
	for i in range(len(final)):
		current_day = final[i]
		for i in range(len(current_day)):
			current_event = current_day[i]
			new_event = current_event.split(', ')
			new_day.append(new_event)
			new_event = []
		new_final.append(new_day)
		new_day = []
	return new_final


def get_venue(scrapeddata):  #  Grab the list of venues where the shows are playing. The venues will match up with the list of events.
	table = scrapeddata[1]
	temp = []
	venues = []
	for i in range(len(table)):
		current_table = table[i]
		b_tags_rough = current_table.find_all("b")
		for i in range(len(b_tags_rough)):
			stripped = b_tags_rough[i].get_text()
			stripped = str(stripped)
			temp.append(stripped)
		venues.append(temp)
		temp = []
	return venues


def make_dict(scrapeddata):  # Make a dictionary key for each artist found on showlist, mapping the date and venue as values.
	dictionary = defaultdict(list)
	new_final = get_events(scrapeddata)
	dates = get_dates(scrapeddata)
	venue = get_venue(scrapeddata)
	event_count = 0
	day_count = 0
	for i in range(len(new_final)):
		day = new_final[i]
		for i in range(len(day)):
			event = day[i]
			for i in range(len(event)):
				band = event[i]
				current_venue = venue[day_count][event_count]
				current_date = dates[day_count]
				dictionary[band].append(current_venue)
				dictionary[band].append(current_date)
			event_count += 1
		event_count = 0
		day_count += 1
	return dictionary


def iTunes():  #  Scan iTunes .XML for artists, make a list of all artists.
	tree = xml.etree.ElementTree.ElementTree() 
	tree.parse('C:\Users\Brian\Music\iTunes\iTunes Music Library.xml') 
	doc = tree.getroot()
	top = doc.find('dict')
	tracks = top.find('dict')
	sets = []
	for track in tracks.findall('dict'):
	  	name = track.findall('string')
	  	name = name[1].text
	  	name = name.lower()
	  	if name in sets:
	  		pass
	  	else:
	  		sets.append(name)
	return sets


def make_list():  #  Find matches between iTunes artists and Showlist's artists.
	scrapeddata = scrape()
	ituneslist = iTunes()
	dictionary = make_dict(scrapeddata)
	matches = defaultdict(list)
	for i in range(len(ituneslist)):
		if ituneslist[i] in dictionary:
			print ituneslist[i], dictionary[ituneslist[i]]
			print '\n\n'
		else:
			pass

if __name__ == '__main__':
	make_list()