# scraper nicknamed frosty

import webbrowser
import urllib.request as urllib
from bs4 import BeautifulSoup



opener = urllib.build_opener()
opener.addheaders = [('User-Agent', 'Mozilla/5.0')]

counties = []

# Declares all of the county lists for a given locale
washingtonCounties = []
connecticutCounties = []
bostonCounties = []
newyorkCounties = []
philadelphiaCounties = []


# Associates a local with its given scrapable url
siteKey = {"washington":"http://www.nbcwashington.com/weather/school-closings/",
            "connecticut":"http://www.nbcconnecticut.com/weather/school-closings/",
            "boston":"http://www.nbcboston.com/weather/school-closings/",  #issues
            "newyork":"http://web.archive.org/web/20150127141611/http://www.nbcnewyork.com/weather/school-closings/", 
            "philadelphia":"http://www.nbcphiladelphia.com/weather/school-closings/",
            }

# Associates a locale with its list of counties
listKey = {"washington":washingtonCounties, "connecticut":connecticutCounties, "boston":bostonCounties, "newyork":newyorkCounties, "philadelphia":philadelphiaCounties}


# alll keywords should be entered lower case
cancelledKey = ["schools are cancel", "are closed", "code red", "be closed", "schools is closed", "schools are closed", "schools&nbsp;is closed"]
delayedKey = ["are delayed", "two hour delay", "open late", "two hours late", "two-hour" ]
normalKey = ["normal schedule", "as is", "schools open on time", "no delay", "posted schedule", "schools will open on time"]





class County:
    def __init__(self, name, state, url=None, nbcRegion=None):
        counties.append(self)
        exec(nbcRegion + "Counties.append(self)")
        self.status = "normal"
        self.name = name
        self.state = state
        self.url = url
        self.nbcRegion = nbcRegion
        
#    def getPageContent(self):
#        page = opener.open(self.url)
#        soup = BeautifulSoup(page, "lxml")
#        [s.extract() for s in soup(['style', 'script', '[document]', 'head', 'title'])] # Removes html tags from file
#        pageContent = soup.get_text().lower()
#        return pageContent
#        
#    def openPage(self):
#        webbrowser.open_new_tab(self.url)
        
           
          
#Executes all of lines in countyDeclarations.txt
          ##    Only done this way, to save space
          ##        For actual production code, move those lines into this module
with open("countyDeclarations.txt", "r") as handle:
    for line in handle:
        if "County" in line:
            exec(line)
            
        





def checkNBC(locale):
    url = siteKey[locale]
    page = opener.open(url)
    soup = BeautifulSoup(page, "lxml")
    [s.extract() for s in soup(['style', 'script', '[document]', 'head', 'title'])]
    pageContent = soup.get_text().lower()
    
    # ALL schools in given locale are open
    if "schools are open" in pageContent or "forecast: school's open." in pageContent:
        for county in listKey[locale]:
            county.status = "normal"
                
    # NOT ALL schools are open
    else:
        tags = soup.findAll("p", class_="closing_item")
        y = []
        
        for x in tags:
            [s.extract() for s in x(['br'])]
            name = str(x.contents[0])
            status = str(x.contents[1])
            status = status.replace("<span>", "")
            status = status.replace("</span>", "")
            y.append(name + " " + status)
            tags = [x for x in y if not 'YMCA' in x and not "Academy" in x]
                            
        for county in listKey[locale]:
            y = next((s for s in tags if county.name in s), None)
            if y:
                y = y.lower()
            if y:
                if "open" in y and "late" in y or "2 hr" in y:
                    county.status = "delayed"
                elif "closed" in y or "canceled" in y:
                    county.status = "closed"
            else:
                county.status = "normal"
    
    


### Driver ###
checkNBC('newyork')
checkNBC('washington')
checkNBC('connecticut')

count = 0
for county in counties:
    count += 1
    print(county.name, "---------------", county.status)
    
print(count)

