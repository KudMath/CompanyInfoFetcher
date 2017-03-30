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

class BehanceUsers:

    def __init__(self):
        self.browser = None
        self.driver = None
        self.usersUrls = []
        self.behanceUsersDf = pd.DataFrame(columns=('profileDisplayName', 'profileTitle', 'profileCompany',
                                                    'profileLocation', 'profileWebsite', 'projectViewsCount',
                                                    'appreciationsCount', 'followersCount', 'followingCount', 'fields',
                                                    'resumeUrl', 'emails'))
        # self.initBrowser()
        self.initDriver()

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
        self.driver = webdriver.PhantomJS(r'F:\Programs\phantomjs-2.0.0-windows\bin\phantomjs.exe')
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
        time.sleep(3)
        html = self.driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        usernames = soup.find_all('a', {'class': 'user-name'})
        self.usersUrls += [username['href'] for username in usernames]

    def fetchUsers(self, usersCount, ordinal=0):
        pageCount = usersCount / 25
        lastPageOrdinal = usersCount % 25
        for i in range(pageCount):
            self.fetchUsersWithDriver(ordinal=ordinal + i * 25)
        if lastPageOrdinal > 0:
            self.fetchUsersWithDriver(ordinal=ordinal + pageCount * 25, per_page=lastPageOrdinal)
        print self.usersUrls
        for i, userUrl in enumerate(self.usersUrls):
            self.behanceUsersDf.loc[i] = self.parsePage(userUrl)
        self.behanceUsersDf.to_csv('behanceUsers.csv', sep=';', encoding='utf-8')

    def parsePage(self, url):
        self.driver.get(url)
        time.sleep(3)
        html = self.driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        parser = behanceUserProfileParser.BehanceUserProfileParser(self.driver, soup)
        return parser.parse()


print str(datetime.now())
behanceUsers = BehanceUsers()
behanceUsers.fetchUsers(100)
# print behanceUsers.parsePage("https://www.behance.net/thomascampi")
print str(datetime.now())
