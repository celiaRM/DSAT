from bs4 import BeautifulSoup
import collections
import urllib.request
from html.parser import HTMLParser
import os
URLdetails =""
class MyHTMLParser(HTMLParser): #modified but from http://stackoverflow.com/questions/3075550/how-can-i-get-href-links-from-html-code
    def handle_starttag(self, tag, attrs):          #global idea http://stackoverflow.com/questions/423379/using-global-variables-in-a-function-other-than-the-one-that-created-them
        global URLdetails
        if tag == "a":      
           for name, value in attrs:
               if name == "href":
                   URLdetails = URLdetails + value + "\n"
                   
class MLStripper(HTMLParser):   #class taken from http://stackoverflow.com/questions/753052/strip-html-from-strings-in-python
    def __init__(self):
        self.reset()
        self.strict = False
        self.convert_charrefs= True
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

def randomTesting(testList):
    for line in testList:
        print(line)
        print()
        
def URLsearch(productName):
    keyWords = productName.split()
    searchAddOn=keyWords[0]
    for i in range(1,len(keyWords)):
        searchAddOn = searchAddOn + "+" +keyWords[i]
    return "http://search.euro.dell.com/results.aspx?s=dhs&c=uk&l=en&cs=ukdhs1&cat=all&k=" + searchAddOn

def URLFinalSearch(URLextraPart):
    return "http://www.dell.com/" + URLextraPart

def enterURL(extracode):
    return "http://search.euro.dell.com/"+extracode

product="xps"
lowCase = product.lower()

page = urllib.request.urlopen(URLsearch(product))

soup = BeautifulSoup(page)

"""
Locating the URL code
"""
#input("Please enter the name of the product you would like to know more about: ")
locator = soup.find_all("div", class_="rgTitle")
productNameList=[]
for line in locator:
    productNameList.append(strip_tags(str(line)))

parser = MyHTMLParser()
parser.feed(str(locator))

searchLinks =  URLdetails.split()                           #searchLinks contains actual links for each one


"""
Choosing a link
"""
wordSep = lowCase.split()
finalNameList = []
LinksTitles = collections.OrderedDict()                                #learnt how to do this using: http://pymotw.com/2/collections/ordereddict.html

for word in wordSep:
    for i in range(0,len(productNameList)):                         
        if word in productNameList[i].lower():
            LinksTitles[productNameList[i]] = searchLinks[i] 

for i in range (0,len(finalNameList)):
    for word in finalNameList:
        LinksTitles[word]=1

print(LinksTitles)
        
titleSelect = collections.OrderedDict()
numList=1
linksCount=0

for key in LinksTitles:
    print(numList,"-",key)
    titleSelect[searchLinks[linksCount]] = numList
    numList += 1
    linksCount += 1

page.close()

selectionInput = input("\nSelect a product by entering the corresponding number on the left: ")
for key in titleSelect:
    if selectionInput in str(titleSelect[key]):
        nextURL = enterURL(key)
        typeSelector = urllib.request.urlopen(nextURL)
        typesSoup = BeautifulSoup(typeSelector)
        linkFinder = typesSoup.find_all("h2", class_="pStackHeader")
        cleanLinkFinder = str(linkFinder).split('<h2 class="pStackHeader">')
        print(cleanLinkFinder)
        URLdetails = ""
        findA=MyHTMLParser()
        findA.feed(str(linkFinder))
        productNamesList=[]

        for elem in cleanLinkFinder:
            productName = strip_tags(elem)
            if "]" in productName or "[" in productName:
                productName = productName.replace("]", "")
                productName = productName.replace("[", "")
            productName = productName.replace("\n", "")
            productNamesList.append(productName)

        nameLinks = URLdetails.split()
        namesWithLinks = collections.OrderedDict()

        for i in range (0,len(nameLinks)):
            namesWithLinks[productNames[i]] = nameLinks[i]   
        numSelector = 1
        anotherIndex = 0
        modelSelect = collections.OrderedDict()

        for key in namesWithLinks:
            print(numSelector,"-",key)
            modelSelect[nameLinks[anotherIndex]] = numSelector
            numSelector += 1
            anotherIndex += 1
        modelInput = input("\nSelect a model by entering the corresponding number on the left: ")

        for key in modelSelect:
            if modelInput in str(modelSelect[key]):
                finalURL = URLFinalSearch(key)
                print(finalURL)
        break
        
        
