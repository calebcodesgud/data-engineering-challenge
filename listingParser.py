from typing import List
from time import sleep
import lxml.html
from lxml import etree
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from datetime import datetime as dt
from unit import unit
from listing import listing
from random import randint
from constants import *
from util import *
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service


class listingParser(object):

    def __init__(self, propertyLinks: List[str], listings: List[listing], parserNum: int):
        self.propertyLinks = propertyLinks
        self.listings = listings
        self.parserNum = parserNum
        self.noPropetiesRemainingCounter = 0
        s = Service('./chromedriver.exe')
        chromeOptions = Options()
        # chromeOptions.add_argument("--disable-gpu")
        # chromeOptions.add_argument("--headless")
        self.driver = webdriver.Chrome(service=s, options=chromeOptions)
        self.driver.implicitly_wait(10)
        sleep(5)

    def printMe(self, string: str, end='\n'):
        print(f'{dt.now().isoformat()} | parser {self.parserNum} | {string}', end)

    def run(self):
        while len(self.propertyLinks) == 0:
            self.printMe(f'no properties yet, sleeping for 1 secs')
            sleep(1)
        while True:
            link = self.getLink()
            if len(link) > 0:
                self.processLink(link)
                sleepSecs: int = randint(1, 2)
                self.printMe(f'sleeping for {sleepSecs} seconds')
                sleep(sleepSecs)
                self.printMe(f'{len(self.propertyLinks)} properties remaining')

    def getLink(self):
        try:
            link: str = self.propertyLinks.pop(0)
            self.printMe(link)
            return link
        except IndexError:
            sleep(10)
            self.noPropetiesRemainingCounter += 1
            if self.noPropetiesRemainingCounter == 3:
                self.printMe(f'no properties left, exiting')
                self.driver.close()
                exit()
            return ''

    def processLink(self, link: str):
        self.driver.get(link)
        propertyAmenities, unitAmenities = self._getAmenities()
        zip = self._getZip()
        unitList: List[unit] = self._getUnits()
        for u in unitList:
            l = listing(zip,
                        propertyAmenities,
                        unitAmenities,
                        u.numberBeds,
                        u.rent,
                        u.sqft)
            # self.printMe(str(l))
            self.listings.append(l)
        self.printMe(f'added {len(unitList)} listings')

    def _getZip(self):
        loc = self.driver.find_element(By.XPATH, "//a[@href='#location']")
        self.driver.execute_script('arguments[0].click();', loc)
        locationDiv = self.driver.find_element(By.XPATH,
                                               "//a[@id = 'location']/following-sibling::div/div/div[contains(@class, 'Subtitle')]")
        locationList = locationDiv.text.replace('\n', ' ').split(' ')
        for s in reversed(locationList):
            if len(s) == 5:
                try:
                    int(s)
                    return s
                except Exception:
                    pass
        return None

    def _getAmenities(self):
        self.driver.find_element(By.XPATH, "//a[@href='#amenities']").click()
        pAmensList: List[str] = []
        uAmensList: List[str] = []
        pAmenDivs = self.driver.find_elements(By.XPATH,
                                              "//div[contains(text(), 'Property Amenities')]/following-sibling::div/div")
        for amen in pAmenDivs:
            a = amen.find_element(By.XPATH, ".//div")
            pAmensList.append(a.text)
        uAmenDivs = self.driver.find_elements(By.XPATH,
                                              "//div[contains(text(), 'Unit Amenities')]/following-sibling::div/div")
        for amen in uAmenDivs:
            a = amen.find_element(By.XPATH, ".//div")
            uAmensList.append(a.text)
        return pAmensList, uAmensList

    def _getUnits(self):
        loc = self.driver.find_element(By.XPATH, "//a[@href='#location']")
        self.driver.execute_script('arguments[0].click();', loc)
        wrapperDiv = self.driver.find_element(By.XPATH, "//div[contains(@class, 'PriceAndSizeWrapper')]")
        self.driver.implicitly_wait(3)
        try:
            wrapperDiv.find_element(By.XPATH, ".//div[contains(@class, 'MoreUnitsButton')]")
        except NoSuchElementException:
            return self._getSmallNumUnits(wrapperDiv)
        return self._getLargeNumUnits(wrapperDiv)

    def _getLargeNumUnits(self, wrapperDiv: WebElement):
        unitsList: List[unit] = []
        btn = wrapperDiv.find_element(By.XPATH, ".//div[contains(@class, 'MoreUnitsButton')]")
        self.driver.execute_script('arguments[0].click();', btn)
        sleep(1)
        wrapperDiv = self.driver.find_element(By.ID, "content-wrapper")
        types = wrapperDiv.find_elements(By.XPATH, "./div/child::*")
        for t in types:
            innerDivs = t.find_elements(By.XPATH, "./div/div/div/child::*")
            for d in innerDivs:
                detailsDiv = d.find_element(By.XPATH, ".//div[contains(@class, 'UnitDetails')]")
                self._processUnitDetails(detailsDiv, unitsList)
        return unitsList

    def _getSmallNumUnits(self, wrapperDiv: WebElement):
        unitsList: List[unit] = []
        unitDivs = wrapperDiv.find_elements(By.XPATH, "./div")
        self.driver.find_element(By.XPATH, ".//h2[contains(text(), 'Price and availability')]").click()
        for i in range(2, len(unitDivs) - 1):
            detailsDiv = unitDivs[i].find_element(By.XPATH, ".//div[contains(@class, 'UnitDetails')]")
            self._processUnitDetails(detailsDiv, unitsList)
        return unitsList

    def _processUnitDetails(self, d: WebElement, unitsList: List[unit]):
        priceStr = d.find_element(By.XPATH, ".//div[contains(@class, 'Price')]/p").text
        bedsdAndSqft = d.find_element(By.XPATH, ".//p[contains(@class, 'unitSubTitle')]").text
        price = float(priceStr.replace('$', '').replace(',', ''))
        bedsdAndSqftList = bedsdAndSqft.split('·')
        nBeds = bedsdAndSqftList[0].split(' ')[0]
        nBeds = int('1' if nBeds == 'Studio' else nBeds)
        try:
            sqft = int(bedsdAndSqftList[2].split(' ')[1])
        except Exception:
            sqft = None
        unitsList.append(unit(nBeds, price, sqft))

