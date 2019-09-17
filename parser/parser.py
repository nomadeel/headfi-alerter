#!/usr/bin/env python3

from typing import Mapping, List
import feedparser
import re
import urllib
import sys
from bs4 import BeautifulSoup
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

def check_ship_australia_or_worldwide(details: Mapping[str, str]) -> bool:
    if "Ship to" not in details:
        return False
    if "Anywhere" == details["Ship to"] or "Australia" == details["Ship to"]:
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

def parse_feed() -> List[Listing]:
    feed = feedparser.parse(RSS_URL)
    listings = []

    if feed["bozo"] == 1:
        sys.exit("Malformed RSS feed! Exiting...")

    id_regex = re.compile(".*\.(\d+)/$")

    for item in feed["items"]:
        details = parse_details(item["link"])
        if not check_ship_australia_or_worldwide(details):
            continue
        listing = Listing(item["title"], id_regex.match(item["guid"]).group(1),
                          '{} {}'.format(details["Price"], details["Currency"]), item["link"])
        listings.append(listing)

    return listings
