from bs4 import BeautifulSoup
import urllib.request
from html.parser import HTMLParser
import os
myVar =""
class MyHTMLParser(HTMLParser): #modified but from http://stackoverflow.com/questions/3075550/how-can-i-get-href-links-from-html-code
    def handle_starttag(self, tag, attrs):          #global idea http://stackoverflow.com/questions/423379/using-global-variables-in-a-function-other-than-the-one-that-created-them
        global myVar
        if tag == "a":      
           for name, value in attrs:
               if name == "href":
                   myVar = myVar + value + "\n"

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

def enterURL(extracode):
    return "http://search.euro.dell.com/"+extracode

product="inspiron"

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
print(myVar)


"""
Choosing a link
"""
wordSep = product.split()
iSearch = 0
for word in wordSep:                #problem is it has to go through as many elements as in len list. Will fix later
    print(word)
    if word in productNameList:
        print("yes")
#            finalPrices[URLlist[i]]=priceList[i]
    iSearch += 1
