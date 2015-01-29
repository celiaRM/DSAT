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

page = urllib.request.urlopen("http://www.dell.com/uk/p/inspiron-14-3451-laptop/pd?oc=cn35104")

soup = BeautifulSoup(page)

alls=soup.find_all("h5")

"""
Code for printing titles
"""

ok=[]
for h5 in alls:
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
titles.append("Price")

##for line in titles:
##    print(line)

"""
Code for printing the details of each title
"""  
right=soup.find_all("span")
test=[]

for line in right:
    test.append(line)

##for line in test:
##    print(line)
##    print()
lines=[]
for i in range(25,len(titles)+26):
    lines.append(strip_tags(str(test[i])))
deletePart=[]
i=-1

for i in deletePart:
    lines.pop(i)

for line in lines:
    i+=1
    if len(line) <=1:
        deletePart.append(i)
    elif 'Choose Options' in line:
        deletePart.append(i)
deletePart.sort(reverse=True)
del deletePart[0]
for num in deletePart:
    lines.pop(num)
lines.append("£"+ strip_tags(str(test[44])))

##randomTesting(test)
##commaSep=lines[11].split(",")
##moreSep=commaSep[1].split("/")
##portsDetail=commaSep+moreSep

##for line in lines:
##    print (line)
##    print()


##see=str(test[25])
##testing=strip_tags(see)
##print(testing)

"""
Exporting to a file
"""
##del(titles[5])
##computer = input("Enter the name of your purchase: ")+".txt"
file = open("computer.txt", 'w+')
index=0

while index!=len(titles):
    file.write(titles[index].upper()+":")
    file.write("\n")
##    if index == 11:
##        for line in portsDetail:
##            file.write("-"+line)
##            file.write("\n")
##        file.write("\n")
    file.write(lines[index])
    file.write("\n")
    file.write("\n")
    index += 1

##for line in lines:
##    for title in titles:
##        file.write(title)
##        file.write("\n")
##        break
##    file.write(line)
        
file.close()
