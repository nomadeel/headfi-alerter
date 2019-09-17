#!/usr/bin/env python3

from typing import Mapping, List
import feedparser
import re
import urllib
import sys
import sqlite3
from bs4 import BeautifulSoup
from record.record import *
#from test.test import test

RSS_URL = "https://www.head-fi.org/forums/headphones-for-sale-trade.6550/index.rss"

class Listing:
    def __init__(self, title: str, guid: str, price: str, link: str, ships_to: str):
        self.title = title
        self.guid = guid
        self.price = price
        self.link = link
        self.ships_to = ships_to

    def __getattr__(self, name: str) -> str: ...

    def __repr__(self) -> str:
        return 'Title: {}\nID: {}\nPrice: {}\nLink: {}\nShips to: {}'.format(self.title, self.guid,
                                                                             self.price, self.link,
                                                                             self.ships_to)

def check_if_seen(guid: str, db_cursor: sqlite3.Cursor) -> bool:
    db_cursor.execute("SELECT * FROM seen WHERE id = ?", (guid,))
    if db_cursor.fetchone():
        return True
    return False

def parse_details(url: str) -> Mapping[str, str]:
    page = urllib.request.urlopen(url)
    soup = BeautifulSoup(page, "html.parser")
    # Returns stuff like: 
    # ['Type:', 'For Sale', 'Currency:', 'Euro', 'Price:', '750', 'Ship to:', 'Anywhere',
    # 'Best offer:', 'Yes']
    unparsed_info = list(soup.find_all(class_="pairsRows secondaryContent")[0].stripped_strings)
    return dict(zip([x.rstrip(':') for x in unparsed_info[::2]], unparsed_info[1::2]))

def parse_feed(db_cursor: sqlite3.Cursor) -> List[Listing]:
    feed = feedparser.parse(RSS_URL)
    listings = []

    if feed["bozo"] == 1:
        sys.exit("Malformed RSS feed! Exiting...")

    id_regex = re.compile(".*\.(\d+)/$")

    for item in feed["items"]:
        listing_guid = id_regex.match(item["guid"]).group(1)
        if check_if_seen(listing_guid, db_cursor):
            continue
        details = parse_details(item["link"])
        listing = Listing(item["title"], listing_guid,
                          '{} {}'.format(details["Price"], details["Currency"]), item["link"],
                                         details["Ship to"])
        listings.append(listing)

    return listings
