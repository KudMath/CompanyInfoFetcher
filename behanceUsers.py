import mechanize
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import behanceUserProfileParser
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.expected_conditions import staleness_of
from selenium.common.exceptions import TimeoutException
from datetime import datetime
from pymongo import MongoClient

class BehanceUsers:

    def __init__(self):
        self.browser = None
        self.driver = None
        self.usersUrls = []
        self.columns = ['profileDisplayName', 'profileTitle', 'profileCompany',
                        'profileLocation', 'profileWebsite', 'projectViewsCount',
                        'appreciationsCount', 'followersCount', 'followingCount', 'fields',
                        'resumeUrl', 'emails']
        self.behanceUsersDf = pd.DataFrame(columns=('profileDisplayName', 'profileTitle', 'profileCompany',
                                                    'profileLocation', 'profileWebsite', 'projectViewsCount',
                                                    'appreciationsCount', 'followersCount', 'followingCount', 'fields',
                                                    'resumeUrl', 'emails'))
        # self.initBrowser()
        self.initDriver()
        self.client = MongoClient()
        self.forceUpdate = False

    def forceUpdateOn(self):
        self.forceUpdate = True
        pass
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
        self.driver = webdriver.PhantomJS('/usr/local/lib/node_modules/phantomjs-prebuilt/bin/phantomjs') # TO DO FIX !!!! r'F:\Programs\phantomjs-2.0.0-windows\bin\phantomjs.exe'
        # self.driver = webdriver.Chrome(r'F:\workspace-python\CompanyInfoFetcher\webdriver\chromedriver_win32\chromedriver.exe')
        self.driver.set_window_size(1024, 768)

    def fetchUsersWithBrowser(self):
        url = "https://www.behance.net/search?ordinal=50&per_page=25&field=&content=users&sort=featured_date&time=all"
        response = self.browser.open(url)
        html = response.read()
        print html

    def fetchUsersWithDriver(self, timeout=30, ordinal=0, per_page=25):
        url = "https://www.behance.net/search?ordinal=" + str(ordinal) + "&per_page=" + str(per_page) + "&field=&content=users&sort=featured_date&time=all"
        self.driver.get(url)
        #time.sleep(3)
        html = self.driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        usernames = soup.find_all('a', {'class': 'user-name'})
        self.usersUrls += [username['href'] for username in usernames]

    def manageObject (self, incoming_object):
        #check already existing object
        collection = self.client['scrapping']['behanceUsers']
        existing_object = collection.find_one({'profileDisplayName': incoming_object['profileDisplayName']})
        if(existing_object):
            print "already in", existing_object['profileDisplayName']
            collection.update({"_id":existing_object['_id']}, incoming_object)
            #create replace or update
            pass
        else:
            inserted_id = collection.insert_one(incoming_object).inserted_id
            print "new user inserted", inserted_id

    def fetchUsers(self, usersCount, ordinal=0):
        pageCount = usersCount / 25
        lastPageOrdinal = usersCount % 25
        for i in range(pageCount):
            self.fetchUsersWithDriver(ordinal=ordinal + i * 25)
        if lastPageOrdinal > 0:
            self.fetchUsersWithDriver(ordinal=ordinal + pageCount * 25, per_page=lastPageOrdinal)
        #print self.usersUrls
        for i, userUrl in enumerate(self.usersUrls):
            collection = self.client['scrapping']['behanceUsers']
            existing_object = collection.find_one({'behanceURL': userUrl})

            #only parse full page if not already in OR if self.forceUpdate
            if (not existing_object) or self.forceUpdate:
                #print "updating"
                parsed = self.parsePage(userUrl)
                dict_obj = dict(zip(self.columns, parsed))
                dict_obj['behanceURL'] = userUrl
                dict_obj['lasteUpdated'] = datetime.now()
                print dict_obj
                self.manageObject(dict_obj)
                pass
            else:
                #print "not parsing"
                pass
        return ordinal
    def continuousFetch(self, ordinal):
        print "current ordinal", ordinal
        new_ordinal = self.fetchUsers(50, ordinal=ordinal)
        self.continuousFetch(new_ordinal)
        pass
    def beginContinuousFetch(self):
        print "continuousFetch begins"
        self.continuousFetch(0)
        pass
    def parsePage(self, url):
        self.driver.get(url)
        time.sleep(3)
        html = self.driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        parser = behanceUserProfileParser.BehanceUserProfileParser(self.driver, soup)
        return parser.parse()


print "Starting Benhance parsing", str(datetime.now())
behanceUsers = BehanceUsers()
#behanceUsers.fetchUsers(100)
behanceUsers.beginContinuousFetch()
# print behanceUsers.parsePage("https://www.behance.net/thomascampi")
print "Done parsing Behance", str(datetime.now())
