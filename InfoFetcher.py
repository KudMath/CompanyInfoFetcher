import mechanize
from bs4 import BeautifulSoup
import urllib
import WebsiteCrawler2

class InfoFetcher:

    companies = []
    browser = None

    def __init__(self):
        self.initBrowser()

    def initBrowser(self):
        self.browser = mechanize.Browser(factory=mechanize.RobustFactory())
        self.browser.set_handle_robots(False)
        self.browser.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 6.1; rv:38.0) Gecko/20100101 Firefox/38.0')]
        self.browser.set_handle_equiv(True)
        self.browser.set_handle_redirect(True)
        self.browser.set_handle_referer(True)
        self.browser.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
        self.browser.set_handle_robots(False)


    def getCompaniesFromFile(self):
        fo = open("companies.txt", "r")
        companyName = fo.readline()
        isEof = companyName == ""
        self.companies = [companyName]
        while not isEof:
            companyName = fo.readline()
            isEof = companyName == ""
            if not isEof:
                self.companies.append(companyName)

    def getGoogleSearch(self, company):
        websiteUrl = None
        phoneNumber = None
        googleUrl = 'https://www.google.fr'
        encodedCompany = urllib.quote(company)
        url = googleUrl + '/search?q=' + encodedCompany
        response = self.browser.open(url)
        html = response.read()
        soup = BeautifulSoup(html, 'html.parser')
        div = soup.find('div', {'class' : '_ldf'})
        if div:
            a = div.find('a')
            if a:
                websiteUrl = a['href']
                if 'maps' in websiteUrl:
                    websiteUrl = None
        divs = soup.find_all('div', {'class' : '_eFb'})
        if divs:
            for div in divs:
                spans = div.find('span')
                if spans:
                    for span in spans:
                        spanInside = span.find('span')
                        if spanInside and spanInside != -1:
                            phoneNumber = spanInside.string

        if websiteUrl == None:
            div = soup.find('div', {'class' : 'rc'})
            if div:
                h3 = div.find('h3', {'class' : 'r'})
                if h3:
                    a = h3.find('a')
                    if a:
                        if a.has_attr('data-href'):
                            websiteUrl = a['data-href']
                        elif websiteUrl == None:
                            websiteUrl = a['href']
        print 'websiteUrl = ' + str(websiteUrl)
        print 'phoneNumber = ' + str(phoneNumber)
        return [str(websiteUrl), str(phoneNumber)]

    def getWebsiteCrawledEmails(self, websiteUrl):
        wc = WebsiteCrawler2.WebsiteCrawler()
        emails = []
        try :
            emails = wc.crawl(websiteUrl,3)
            # emails = wc.crawl('http://www.' + company.strip().replace('%0A','').replace(' ','') + '.com', 30)
        except :
            pass
        # try :
        #     emails += wc.crawl('http://www.' + company.strip().replace('%0A','').replace(' ','') + '.fr', 30)
        # except :
        #     pass
        return emails

    def getCompaniesInfo(self):
        f = open('companies.csv', 'w')
        self.getCompaniesFromFile()
        for company in self.companies:
            searchRes = self.getGoogleSearch(company)
            websiteUrl = searchRes[0]
            phone = searchRes[1]
            emails = self.getWebsiteCrawledEmails(websiteUrl)
            line = company.strip().replace('%0A','').replace('\n','') + ";" + websiteUrl + ";" + phone + ";" + str(emails) + "\n"
            f.write(line)
            print line
        f.close()

    def testGetCompanyInfo(self, company):
        searchRes = self.getGoogleSearch(company)
        websiteUrl = searchRes[0]
        emails = self.getWebsiteCrawledEmails(websiteUrl)
        print emails






infoFetcher = InfoFetcher()
infoFetcher.testGetCompanyInfo('(Groupe) astek')
# infoFetcher.getCompaniesFromFile()
# infoFetcher.getGoogleSearch('IMMOBILIER COMMERCE FRANCHISE ICF')
# infoFetcher.getCompaniesInfo()