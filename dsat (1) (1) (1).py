import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import urllib.request
from html.parser import HTMLParser

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
"""
Opening website html on python
"""

def geturl():

    err=True

    print("Enter the full URL of the Dell product.\nMake sure to get the URL after http://www.dell.com/uk/p/.")

    while err == True:

        err=False

        url=input("URL: ")

        fullurl = "http://www.dell.com/uk/p/" + url

    return fullurl



##product_url = geturl()
##
##print("The full URL is",product_url)

page = urllib.request.urlopen("http://www.dell.com/uk/p/inspiron-15-3542-laptop/pd?oc=cn54243&model_id=inspiron-15-3542-laptop")

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
Code for accessing parameters efficiently 
"""

##test=[]
##
##for line in right:
##    test.append(line)
##
##start=0
##locatorStart = soup.find("span", {"class" : "shortSpec spec~bjAwYXczMDE~146"})             #code for finding specific things
##for line in test:
##    if locatorStart == line:
##        break
##    start += 1
##
##priceIndex=0
##locatorPrice = soup.find("span", {"class" : "pAmt strike"})
##for line in test:
##    if locatorPrice == line:
##        break
##    priceIndex += 1


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


####commaSep=lines[11].split(",")
####moreSep=commaSep[1].split("/")
####portsDetail=commaSep+moreSep
##


"""
Exporting to a file
"""

####computer = input("Enter the name of your purchase: ")+".txt"
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
