import re
import time
from bs4 import BeautifulSoup

class BehanceUserProfileParser:

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

    def parse(self):
        # div id="profile-display-name"
        profileDisplayNameRaw = self.soup.find('div', {'id': 'profile-display-name'}).find('a')
        if profileDisplayNameRaw:
            profileDisplayName = profileDisplayNameRaw.text.strip()
        else:
            profileDisplayName = None
        # div id="profile-title"
        profileTitleRaw = self.soup.find('div', {'id': 'profile-title'})
        if profileTitleRaw:
            profileTitle = profileTitleRaw.text.strip()
        else:
            profileTitle = None
        # div id="profile-company"
        profileCompanyRaw = self.soup.find('div', {'id': 'profile-company'})
        if profileCompanyRaw:
            profileCompany = profileCompanyRaw.text.strip()
        else:
            profileCompany = None
        # a class="profile-location-link"
        profileLocationRaw = self.soup.find('a', {'class': 'profile-location-link'})
        if profileLocationRaw:
            profileLocation = profileLocationRaw.text.strip()
        else:
            profileLocation = None
        # a id="profile-website" --> href
        profileWebsiteTag = self.soup.find('a', {'id': 'profile-website'})
        if profileWebsiteTag:
            profileWebsite = profileWebsiteTag['href']
        else:
            profileWebsite = None
        # a class="js-project-views-count"
        projectViewsCountRaw = self.soup.find('a', {'class': 'js-project-views-count'})
        if projectViewsCountRaw:
            projectViewsCount = projectViewsCountRaw.text.strip()
        else:
            projectViewsCount = None
        # a class="js-appreciations-count"
        appreciationsCountRaw = self.soup.find('a', {'class': 'js-appreciations-count'})
        if appreciationsCountRaw:
            appreciationsCount = appreciationsCountRaw.text.strip()
        else:
            appreciationsCount = None
        # a class="js-followers-count"
        followersCountRaw = self.soup.find('a', {'class': 'js-followers-count'})
        if followersCountRaw:
            followersCount = followersCountRaw.text.strip()
        else:
            followersCount = None
        # a class="js-following-count"
        followingCountRaw = self.soup.find('a', {'class': 'js-following-count'})
        if followingCountRaw:
            followingCount = followingCountRaw.text.strip()
        else:
            followingCount = None
        # a class="field" --> several fields, get them all
        fieldsRaw = self.soup.find_all('a', {'class': 'field'})
        if fieldsRaw:
            fields = [fieldRaw['title'] for fieldRaw in fieldsRaw]
        else:
            fields = None
        # --> fetch emails on current link
        self.emails += self.fetchEmails()
        # a class="profile-section-more" --> href, go to link and fetch emails
        resumeTag = self.soup.find('a', {'class': 'profile-section-more'})
        if resumeTag:
            resumeUrl = resumeTag['href']
            self.driver.get(resumeUrl)
            time.sleep(3)
            html = self.driver.page_source
            self.soup = BeautifulSoup(html, 'html.parser')
            self.emails += self.fetchEmails()
        else:
            resumeUrl = None
        # print profileDisplayName
        # print profileTitle
        # print profileCompany
        # print profileLocation
        # print profileWebsite
        # print projectViewsCount
        # print appreciationsCount
        # print followersCount
        # print followingCount
        # print str(fields)
        # print resumeUrl
        # print str(self.emails)
        return [profileDisplayName, profileTitle, profileCompany, profileLocation, profileWebsite, str(projectViewsCount), str(appreciationsCount),
                str(followersCount), str(followingCount), str(fields), resumeUrl, str(self.emails)]

    def fetchEmails(self):
        result = []
        # result += self.email_re.findall(self.soup.text)
        result += [email[0] for email in re.findall(self.email_re, self.soup.text) if not email[0].startswith('//')]
        return result
