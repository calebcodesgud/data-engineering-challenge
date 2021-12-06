from typing import List

import requests
from time import sleep
from random import randint
from listingParser import listingParser
from threading import Thread
from listing import listing
from constants import *
import lxml.html
from util import *
from repo import repo


def getLinksOnPages(pageNum: int):
    print(f'getting links on page {pageNum}')
    if pageNum == 1:
        response = requests.get(EVANSTON_BASE_URL, stream=True)
    else:
        response = requests.get(EVANSTON_BASE_URL + f'/page-{pageNum}', stream=True)
    print(response.status_code)
    tree = responseToTree(response)
    outerDivs = tree.xpath("//div[contains(@aria-label, 'Listing card for')]")
    for div in outerDivs:
        l = div.xpath(f".//a[contains(@href, '{EVANSTON}')]")
        try:
            propertyLinks.append(APARTMENTLIST_BASE_URL + l[0].get('href'))

        except IndexError:
            pass
    divs = tree.xpath("//div[contains(text(), 'Results within')]")
    return len(divs)


if __name__ == '__main__':
    nBots: int = 2
    propertyLinks: List[str] = []
    listings: List[listing] = []
    for j in range(nBots):
        p = listingParser(propertyLinks, listings, j)
        Thread(target=p.run).start()
    pageNum: int = 1
    while getLinksOnPages(pageNum) == 0:
        pageNum += 1
        sleepSecs: int = randint(5, 10)
        print(f'main sleeping for {sleepSecs} seconds')
        print(propertyLinks)
        sleep(sleepSecs)
    r = repo()
    prevLen = len(listings)
    while True:
        sleep(30)
        currLen = len(listings)
        if currLen == prevLen:
            print(f'{currLen} listings found')
            for l in listings:
                r.saveListing(l)
            print()
            r.lookupAmenities()
            r.lookupAvgRent()
            r.close()
            exit()
        prevLen = currLen
