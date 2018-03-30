
import webbrowser
import urllib.request as urllib
from bs4 import BeautifulSoup

opener = urllib.build_opener()
opener.addheaders = [('User-Agent', 'Mozilla/5.0')]

counties = []


# alll keywords should be entered lower case
cancelledKey = ["schools are cancel", "are closed", "code red", "be closed", "schools is closed", "schools are closed", "schools&nbsp;is closed"]
delayedKey = ["are delayed", "two hour delay", "open late", "two hours late", "two-hour" ]
normalKey = ["normal schedule", "as is", "schools open on time", "no delay", "posted schedule", "schools will open on time"]





class County:
    def __init__(self, name, state, url):
        counties.append(self)
        self.status = "normal"
        self.name = name
        self.state = state
        self.url = url
        self.benchStats = {"normal":0, "delayed":0, "cancelled":0}
        
    def getPageContent(self):
        page = opener.open(self.url)
        soup = BeautifulSoup(page, "lxml")
        [s.extract() for s in soup(['style', 'script', '[document]', 'head', 'title'])]
        pageContent = soup.get_text().lower()
        return pageContent
        
    def openPage(self):
        webbrowser.open_new_tab(self.url)
        
        
    def getBenchmark(self):
        pageContent = self.getPageContent()
        for x in cancelledKey:
            if x in pageContent:
                self.benchStats["cancelled"] += pageContent.count(x)

        for x in delayedKey:
            if x in pageContent:
                self.benchStats["delayed"] += pageContent.count(x)
        for x in normalKey:
            if x in pageContent:
                self.benchStats["normal"] += pageContent.count(x)
                
        
        
#    def checkStatus(self):
#        pageContent = self.createSoup().get_text()
        
        
    

BCPS = County("Baltimore County Public Schools", "MD", "http://web.archive.org/web/20150122163538/http://www.bcps.org/")
MCPS = County("Montgomery County Public Schools", "MD", "http://web.archive.org/web/20160209132933/http://www.montgomeryschoolsmd.org/")
#PGCPS = County("Prince George's County Public Schools", "MD", "http://www.pgcps.org/")
AACPS = County("Anne Arundel County Public Schools", "MD", "http://web.archive.org/web/20150302100013/http://www.aacps.org:80/")
#HCPS = County("Howard County Public Schools", "MD", "http://www.hcpss.org/")
#FCPS = County("Frederick County Public Schools", "MD", "http://www.fcps.org/")
#BCityPS = County("Baltimore City Public Schools", "MD", "http://www.baltimorecityschools.org/")
WCPS = County("Washington County Public Schools", "MD", "http://web.archive.org/web/20160210093751/http://wcpsmd.com:80/")
HarfordCPS = County("Harford County Public Schools", "MD", "http://web.archive.org/web/20170316223234/http://www.hcps.org/")



for county in counties:
    county.getBenchmark()
    print(county.benchStats)
    



