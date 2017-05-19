import mechanize
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import society6ProfileParser
#import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import sys
from selenium.webdriver.support.expected_conditions import staleness_of
from datetime import datetime
from pymongo import MongoClient

class Society6Users:

    def __init__(self):
        self.browser = None
        self.driver = None
        self.usersUrls = []
        self.startingOrdinal = 0
        self.initDriver()
        self.client = MongoClient()
        self.forceUpdate = False
    def forceUpdateOn(self):
        self.forceUpdate = True
    def initBrowser(self):
        self.browser = mechanize.Browser(factory=mechanize.RobustFactory())
        self.browser.set_handle_robots(False)
        self.browser.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 6.1; rv:38.0) Gecko/20100101 Firefox/38.0')]
        self.browser.set_handle_equiv(True)
        self.browser.set_handle_redirect(True)
        self.browser.set_handle_referer(True)
        self.browser.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
        self.browser.set_handle_robots(False)
    def initDriver(self):
        self.driver = webdriver.PhantomJS('/usr/local/lib/node_modules/phantomjs-prebuilt/bin/phantomjs') #FIXME to config
        self.driver.set_window_size(1024, 768)
        self.base_url = "https://www.society6.com/"
        self.verificationErrors = []
        self.accept_next_alert = True
    def fetchUsersWithDriver(self, maxi, timeout=30):
        driver = self.driver
        driver.get(self.base_url)
        for i in range(2,maxi):
            self.driver.get(self.base_url+"discover?page="+str(i))
            
        print "Done scrolling, parsing now."
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        usernames = soup.find_all('a', {'class': 'author'})
        self.usersUrls += [username['href'] for username in usernames]
        print len(self.usersUrls), " users scrapped."
        for i, userUrl in enumerate(self.usersUrls):
            collection = self.client['scrapping']['society6Users']
            existing_object = collection.find_one({'society6URL': "https://www.society6.com"+userUrl})
            #only parse full page if not already in OR if self.forceUpdate
            if (not existing_object) or self.forceUpdate:
                try:
                    parsed = self.parsePage("https://www.society6.com"+userUrl)
                    parsed['society6URL'] = "https://www.society6.com"+userUrl
                    parsed['lasteUpdated'] = datetime.now()
                    self.manageObject(parsed)
                except:
                    print "Error: ", sys.exc_info()[0]
            else:
                print "already in DB"
                pass
    def manageObject (self, incoming_object):
        #check already existing object
        collection = self.client['scrapping']['society6Users']
        existing_object = collection.find_one({'society6URL': incoming_object['society6URL']})
        if(existing_object):
            collection.update({"_id":existing_object['_id']}, incoming_object)
            #create replace or update
        else:
            inserted_id = collection.insert_one(incoming_object).inserted_id
    def beginContinuousFetch(self, maxi = 10):
        print "\"infinite\" scrolling begins now. scrolling for ", maxi, " pages."
        self.fetchUsersWithDriver(maxi)
    def parsePage(self, url):
        print url
        self.driver.get(url)
        html = self.driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        parser = society6ProfileParser.Society6ProfileParser(self.driver, soup)
        return parser.parse()
