import requests
import re
import urlparse
from bs4 import BeautifulSoup

class WebsiteCrawler:

    # Basic e-mail regexp:
    # letter/number/dot/comma @ letter/number/dot/comma . letter/number
    email_re = re.compile(r'([\w\.,]+@[\w\.,-]+\.\w+)')

    # HTML <a> regexp
    # Matches href="" attribute
    link_re = re.compile(r'href="(.*?contact.*?)"')

    fetched_links = []

    def crawl(self, url, maxlevel):
        # Limit the recursion, we're not downloading the whole Internet
        if(maxlevel == 0):
            return []

        # Get the webpage
        req = requests.get(url)
        result = []

        # Check if successful
        if req.status_code != 200:
            return []

        # Find and follow all the links
        # print req.text
        soup = BeautifulSoup(req.text, 'html.parser')
        a_tags = soup.find_all('a')
        links = []
        for a_tag in a_tags:
            links += self.link_re.findall(str(a_tag))
        # print links
        for link in links:
            # print link
            # Get an absolute URL for a link
            link = self.get_url_absolute_path(link)
            # print self.fetched_links
            if link not in self.fetched_links:
                # print link
                self.fetched_links.append(link)
                link = urlparse.urljoin(url, link)
                print "Fetching " + link + "..."
                result += self.crawl(link, maxlevel - 1)

        # Find all emails on current page
        result += self.email_re.findall(req.text)
        return result

    def get_domain(self, url):
        return urlparse.urlparse(url)[1]

    def get_url_absolute_path(self, url):
        return urlparse.urlparse(url)[2]

wc = WebsiteCrawler()
emails = wc.crawl('http://www.groupe-aplitec.com/', 3)

print "Scrapped e-mail addresses:"
for email in emails:
    print email