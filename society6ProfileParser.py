import re
import time
from bs4 import BeautifulSoup
import locale

class Society6ProfileParser:

    # Basic e-mail regexp:
    # letter/number/dot/comma @ letter/number/dot/comma . letter/number
    # email_re = re.compile(r'([\w\.,]+@[\w\.,-]+\.\w+)')
    email_re = re.compile(("([a-z0-9!#$%&'*+\/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+\/=?^_`"
                    "{|}~-]+)*(@|\sat\s)(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?(\.|"
                    "\sdot\s))+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?)"))

    def __init__(self, driver, soup):
        self.driver = driver
        self.soup = soup
        self.emails = []
        locale.setlocale( locale.LC_ALL, 'en_US.UTF-8' )
    def parse(self):
        #socials & joined
        badges = self.soup.find('div', {'class': 'badges'})
        socials=[]
        if badges:
            year = badges.find('div', {'class' : 'year'})
            joined = year['title']
            socials += [social['href'] for social in badges.find_all('a')]
        else:
            joined = "Unknown"
        #TODO manage socials ?

        #stats
        stats = {}
        subMenus = self.soup.find_all('a', {'data-gtm-event': 'artistSubmenu'})
        if subMenus :
            for i, stat in enumerate(subMenus):
                strippedstat = stat.text.split()
                if(len(strippedstat) > 1):
                    stats[strippedstat[0]]={"count" : locale.atoi(strippedstat[1][1:-1]), "url" : stat['href']}
                else:
                    stats[strippedstat[0]]={"url": stat['href']}

        #products
        productList = self.soup.find_all('a', {'data-gtm-event': 'artistShop'})
        products=[]
        if productList:
            products += [product.text.strip() for product in productList]

        return {
            'dateJoined':joined,
            'socialProfiles':socials,
            'stats':stats,
            'productTypes': products
        }

    def fetchEmails(self):
        result = []
        # result += self.email_re.findall(self.soup.text)
        result += [email[0] for email in re.findall(self.email_re, self.soup.text) if not email[0].startswith('//')]
        return result
