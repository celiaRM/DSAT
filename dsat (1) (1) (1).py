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

def SearchBar(product):
    global URLdetails
    URLdetails = ""
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
            productNamesList.pop(0)
            for i in range (0,len(nameLinks)):
                namesWithLinks[productNamesList[i]] = nameLinks[i]   
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
                    return(finalURL)
            break
"""
Opening website html on python
"""
page = urllib.request.urlopen(SearchBar(input("Enter your search query: ")))

soup = BeautifulSoup(page)

allTitles=soup.find_all("h5")

"""
Code for printing titles
"""

ok=[]
for h5 in allTitles:
    if h5 != "</h5>" or h5 != "<h5>":
        ok.append(h5)

emptList=[]
for word in ok:
    emptList.append(str(word))

cleanList=[]
for line in emptList:
    newstr = line.replace("\t", " ")
    cleanList.append(newstr)
    
fixList=[]
for line in cleanList:
    fixList.append(" ".join(line.split()))
 
titles=[]
for line in fixList:
    titles.append(strip_tags(line))
titles.append(" Price")

"""
Code for printing the details of each title
"""
alright=soup.find_all("div", class_="specContent")
lines=[]
for line in alright:
    lines.append(strip_tags(str(line)))

deletePart=[]
i=0
emptStr=0

yay = open("miracle.txt", 'w+')

for line in lines:		
    yay.write(str(line))
    yay.write("\n")				
yay.close()		
superList=[]		
letsFix=open("miracle.txt")		
for line in letsFix:		
    superList.append(line)

letsFix.close()
    
for line in superList:
    if len(line) <=1:
        if emptStr>0 :
            deletePart.append(i)
            emptStr=0
    if '/xa0' in line:
            deletePart.append(i)
            emptStr=0
    elif 'Choose Options' in line:
        deletePart.append(i)
        emptStr += 1
    i+=1

deletePart.sort(reverse=True)

for i in deletePart:
    superList.pop(i)
 
randomList=[]
priceFinder=soup.find_all("div", class_="pLine dellPrice")
randomList.append(strip_tags(str(priceFinder)))

for line in randomList:
    if "Price" in line and "[" and "]":
        Priceline=line

if "Price" in Priceline and "[" and "]":
    change1=Priceline.replace("[", "")
    change2=change1.replace("Price", "")
    actualPrice=change2.replace("]", "")
finalPrice = actualPrice.replace("\n", "")
superList.append(finalPrice)

"""
Menu code
"""
print("Welcome to the Dell Systems Analytical Tool")
print("What would you like to do next?")
print("1. View the details of a specific product")
print("2. Compare the prices of Dell products")
select = input("To select a function, type it's number here or type 'q' to quit: ")
finalPrices={}
priceList=[]
while not select in ("quit","q","Quit","Q"):
    if select == "1":
        
        file = open("computer.txt", 'w+')
        index=0
        print(len(superList))
        print(len(titles))

        while index!=len(titles):
            file.write(titles[index].upper()+":")
            file.write("\n")
        ##    if index == 11:
        ##        for line in portsDetail:
        ##            file.write("-"+line)
        ##            file.write("\n")
        ##        file.write("\n")
            file.write(superList[index])
            file.write("\n")
            file.write("\n")
            index += 1

        file.close()
        os.remove("miracle.txt")
        print("\n")
        print("What would you like to do next?")
        print("1. View the details of another product")
        print("2. Compare the prices of Dell products")
        select = input("To select a function, type it's number here or type 'q' to quit: ")

    elif select == "2":
        URLlist = []
        finished = False

        while not finished:
            computerURL = input("Enter the URL of the Dell product or type 'finished' to end: ")

            if computerURL == "finished":
                break
            URLlist.append(computerURL)

        for URL in URLlist:
            soupComputer = BeautifulSoup(urllib.request.urlopen(URL))
            randomList=[]
            priceFinder=soupComputer.find_all("div", class_="pLine dellPrice")
            randomList.append(strip_tags(str(priceFinder)))

            for line in randomList:
                if "Price" in line and "[" and "]":
                    Priceline=line

            if "Price" in Priceline and "[" and "]":
                change1=Priceline.replace("[", "")
                change2=change1.replace("Price", "")
                actualPrice=change2.replace("]", "")
            finalPrice = actualPrice.replace("\n", "")
            priceList.append(finalPrice)

        for i in range(0,len(URLlist)):
            finalPrices[URLlist[i]]=priceList[i]
        print("{0:<60s}".format("Product:"),"Price:")
        sorted(finalPrices.items(), key=lambda x: x[1])

        for key in finalPrices:
            print("{0:<31s}".format(key),finalPrices[key])
        print("\n")
        print("What would you like to do next?")
        print("1. View the details of a specific product")
        print("2. Compare the prices of Dell products")
        select = input("To select a function, type it's number here or type 'q' to quit: ")
