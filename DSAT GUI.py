from bs4 import BeautifulSoup
import collections
import urllib.request
from html.parser import HTMLParser
import os
from tkinter import *
import requests

URLdetails =""

class MyHTMLParser(HTMLParser): #modified but from http://stackoverflow.com/questions/3075550/how-can-i-get-href-links-from-html-code
	def handle_starttag(self, tag, attrs):		  #global idea http://stackoverflow.com/questions/423379/using-global-variables-in-a-function-other-than-the-one-that-created-them
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

def soupWebsite(URL):
	page = requests.get(URL)
	soup = BeautifulSoup(page.text)

	return soup

def searchStep1(searchQuery):
	global URLdetails
	URLdetails = ""
	lowCase = searchQuery.lower()

	page = requests.get(URLsearch(searchQuery))   
	soup = BeautifulSoup(page.text)

	"""
	Locating the URL code
	"""
	extraLinkFinder = soup.find_all("div", class_="c4 seriesTitle")
	locator = soup.find_all("div", class_="rgTitle")

	if len(extraLinkFinder)>0:
		productNameList = []
		cleanProductNameList = []
		LinksTitles = collections.OrderedDict()

		for line in extraLinkFinder:
			productNameList.append(strip_tags(str(line)))

		parser = MyHTMLParser()
		parser.feed(str(extraLinkFinder))

		searchLinks =  URLdetails.split()

		for name in productNameList:
			name = name.replace("\n", "")
			cleanProductNameList.append(name)

		for i in range (len(searchLinks)-1,-1,-1):
			if "#" in searchLinks[i]:
				searchLinks.pop(i)


		#print(searchLinks)
		#print(cleanProductNameList)

		numList=1
		linksCount=0

		#TODO: change from number to name
		for key in LinksTitles:
			#print(numList,"-",key)
			titleSelect[searchLinks[linksCount]] = key
			numList += 1
			linksCount += 1

		page.close()

		#go to next step
		return titleSelect
	
	elif len(locator)>0:
		productNameList=[]
		for line in locator:
			productNameList.append(strip_tags(str(line)))

		parser = MyHTMLParser()
		parser.feed(str(locator))

		searchLinks =  URLdetails.split()				   #searchLinks contains actual links for each one

		"""
		Choosing a link
		"""
		wordSep = lowCase.split()
		finalNameList = []
		LinksTitles = collections.OrderedDict()							 #learnt how to do this using: http://pymotw.com/2/collections/ordereddict.html

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
			#print(numList,"-",key)
			titleSelect[searchLinks[linksCount]] = key
			numList += 1
			linksCount += 1

		page.close()

		#go to next step
		return titleSelect

def searchStep2(URL):
	global URLdetails
	nextURL = enterURL(URL)

	typeSelector = urllib.request.urlopen(nextURL)
	typesSoup = BeautifulSoup(typeSelector)
	linkFinder = typesSoup.find_all("h2", class_="pStackHeader")
	if len(linkFinder)==0:
		return((0,nextURL))
	else:
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
			#print(numSelector,"-",key)
			modelSelect[nameLinks[anotherIndex]] = key
			numSelector += 1
			anotherIndex += 1

		return((1,modelSelect))

def searchStep3(URL):
	return ((0,URLFinalSearch(URL)))

def searchBar(product):
	global URLdetails
	URLdetails = ""
	lowCase = product.lower()

	page = urllib.request.urlopen(URLsearch(product))   
	soup = BeautifulSoup(page)

	"""
	Locating the URL code
	"""
	extraLinkFinder = soup.find_all("div", class_="c4 seriesTitle")
	locator = soup.find_all("div", class_="rgTitle")

	if len(extraLinkFinder)>0:
		productNameList = []
		cleanProductNameList = []
		LinksTitles = collections.OrderedDict()

		for line in extraLinkFinder:
			productNameList.append(strip_tags(str(line)))

		parser = MyHTMLParser()
		parser.feed(str(extraLinkFinder))

		searchLinks =  URLdetails.split()

		for name in productNameList:
			name = name.replace("\n", "")
			cleanProductNameList.append(name)

		for i in range (len(searchLinks)-1,-1,-1):
			if "#" in searchLinks[i]:
				searchLinks.pop(i)


		print(searchLinks)
		print(cleanProductNameList)

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
				if len(linkFinder)==0:
					return(nextURL)
					break
				else:
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
	
	elif len(locator)>0:
		productNameList=[]
		for line in locator:
			productNameList.append(strip_tags(str(line)))

		parser = MyHTMLParser()
		parser.feed(str(locator))

		searchLinks =  URLdetails.split()				   #searchLinks contains actual links for each one

		"""
		Choosing a link
		"""
		wordSep = lowCase.split()
		finalNameList = []
		LinksTitles = collections.OrderedDict()							 #learnt how to do this using: http://pymotw.com/2/collections/ordereddict.html

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
				if len(linkFinder)==0:
					return(nextURL)
					break
				else:
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


def productTitles(soupHTML):
	allTitles=soupHTML.find_all("h5")
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

	return titles

def productDetails(soupHTML):
	alright=soupHTML.find_all("div", class_="specContent")
	lines=[]
	for line in alright:
		lines.append(strip_tags(str(line)))

	deletePart=[]
	i=0
	emptStr=0

	yay = open("miracle.txt", 'w+',encoding="utf-8")

	for line in lines:		
		yay.write(str(line))
		yay.write("\n")				
	yay.close()		
	superList=[]		
	letsFix=open("miracle.txt", 'r', encoding="utf-8")		
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
	priceFinder=soupHTML.find_all("div", class_="pLine dellPrice")
	randomList.append(strip_tags(str(priceFinder)))

	for line in randomList:
		if "Price" in line and "[" and "]":
			Priceline=line

	if "Price" in Priceline and "[" and "]":			
		Priceline=Priceline.replace("[", "")
		Priceline=Priceline.replace("Price", "")
		Priceline=Priceline.replace("]", "")
	Priceline = Priceline.replace("\n", "")
	superList.append(Priceline)

	os.remove("miracle.txt")
	
	return superList

def exportToFile(titlesList,detailsList):
		file = open("computer.txt", 'w+', encoding="utf-8")
		index=0

		while index!=len(titlesList):
			file.write(titlesList[index].upper()+":")
			file.write("\n")
		##	if index == 11:
		##		for line in portsDetail:
		##			file.write("-"+line)
		##			file.write("\n")
		##		file.write("\n")
			file.write(detailsList[index])
			file.write("\n")
			file.write("\n")
			index += 1
		file.close()

def productPrice(URLlist):
	priceList = []
	randomList = []
	
	for URL in URLlist:
		soupComputer = soupWebsite(URL)
		priceFinder=soupComputer.find_all("div", class_="pLine dellPrice")
		randomList.append(strip_tags(str(priceFinder)))
	
	for line in randomList:
		line = line.replace("[", "")
		line = line.replace("Price", "")
		line = line.replace("]", "")
		line = line.replace("\n", "")
		priceList.append(line)

	return priceList

def productName(URLlist):
	namesList = []
	extraList = []

	for URL in URLlist:
		soupComputer = soupWebsite(URL)
		nameFinder=soupComputer.find_all("h1", class_="cufonGothamBook")
		extraList.append(strip_tags(str(nameFinder)))

	for name in extraList:
		name = name.replace("]","")
		name = name.replace("\r\n\t\t\t\t\t\t\t\t\t\t\t","")
		name = name.replace("/t","")
		name = name.replace("[","")
		namesList.append(name)

	return namesList
	

"""
Interface code
"""

def myfunction(event):
    canvas.configure(scrollregion=canvas.bbox("all"),width=200,height=200)


root = Tk()

root.title("DSAT")
root.geometry("600x400")

canvas = Canvas(root, borderwidth=0, background="#DDECEF")
frame = Frame(canvas, background="#DDECEF")
vsb = Scrollbar(root, orient="vertical", command=canvas.yview)
canvas.configure(yscrollcommand=vsb.set)

vsb.pack(side="right", fill="y")
canvas.pack(side="left", fill="both", expand=True)

canvas.create_window((2,3), window=frame, anchor="nw", 
                                  tags="frame")

frame.bind("<Configure>",myfunction)

extraButtons = []
detailStore = []

def clearExtraButtons():
	for b in extraButtons:
		b.destroy()
	del extraButtons[:]

def searchButtonCallback(searchQuery, shouldIrepeat = 0):
	clearExtraButtons()
	listOfStuff = searchStep1(searchQuery)

	i = 6
	for key in listOfStuff:
		makeButton(listOfStuff[key], key, 1, i, shouldIrepeat)
		i+=1
	#print(listOfStuff)

def saveToFileButtonCallback(titles, details):
	exportToFile(titles, details)
	return 0

def createSearchBar(shouldIrepeat = 0):
	clearExtraButtons()
	e = Entry(frame)
	e.grid(row=5, column=1)

	e.focus_set()

	b = Button(frame, text="Search", width=10, command=lambda: searchButtonCallback(e.get(),shouldIrepeat))
	b.grid(row=5, column=2)

	extraButtons.append(e)
	extraButtons.append(b)

	if(shouldIrepeat == 1):
		b2 = Button(frame, text="Stop", width=10, command=lambda: comparisonSearch(detailStore))
		b2.grid(row=5, column=3)
		extraButtons.append(b2)


def showProductDetails(URL):
	clearExtraButtons()

	html = soupWebsite(URL[1])
	titles = productTitles(html)
	details = productDetails(html)
	titlesDetails = collections.OrderedDict()
	
	for i in range(0,len(titles)):
		titlesDetails[titles[i]]=details[i]
	
	i = 6
	for key in titlesDetails:
		proc = Label(frame, text=key + ": " + titlesDetails[key], width=50, wraplength=300, background="#ffffff")
		proc.grid(row=i, column=0, columnspan=3)
		extraButtons.append(proc)
		i+=1

	saveToFileButton = Button(frame, text="Save", width=20, command=lambda: saveToFileButtonCallback(titles, details))
	saveToFileButton.grid(row=i, column=1)
	extraButtons.append(saveToFileButton)


def comparisonSearch(URLlist):   #delete finalPrices, do the loop with the 2 lists 
	finalPrices = collections.OrderedDict()

	priceList = productPrice(URLlist)
	nameList = productName(URLlist)
	print(len(priceList))
	print(len(nameList))
	print(nameList)

	for i in range(0,len(nameList)):
		finalPrices[nameList[i]]=priceList[i]

	start = Label(frame, text="Name" + "            " + "Price", width=50, wraplength=300, background="#DDECEF")
	start.grid(row=5, column=0, columnspan=3)
	extraButtons.append(start)
	print(len(finalPrices))

	index = 7
	for i in range(0,len(nameList)):
		proc = Label(frame, text=nameList[i] + "            " + priceList[i], width=50, wraplength=300, background="#DDECEF")
		proc.grid(row=index, column=0, columnspan=3)
		index += 1
		extraButtons.append(proc)
	i2 = 7
	for i in range(0,len(nameList)):
		html = soupWebsite(URLlist[i])
		titles = productTitles(html)
		details = productDetails(html)
		saveToFileButton = Button(frame, text="Save", width=20, command=lambda: saveToFileButtonCallback(titles, details))
		saveToFileButton.grid(row=i2, column=2)
		i2 += 1

	detailStore = []
	print(detailStore)
	#sorted(finalPrices.items(), key=lambda x: x[1])

def pressButtonForPriceComparison():
	clearExtraButtons()
	createSearchBar(1)

	
def listButtonCallback2(URL, shouldIrepeat = 0):
	clearExtraButtons()
	if(shouldIrepeat == 0):
		showProductDetails(searchStep3(URL))
	else:
		detailStore.append(searchStep3(URL)[1])
		createSearchBar(1)


def listButtonCallback(URL, shouldIrepeat = 0):
	clearExtraButtons()
	result = searchStep2(URL)
	if(result[0] == 0):
		#go to product
		if shouldIrepeat == 0:
			showProductDetails(searchStep3(result[1]))
		else:
			detailStore.append(searchStep3(result[1])[1])
			createSearchBar(1)
	else:
		i = 6
		for key in result[1]:
			makeButton(result[1][key], key, 0, i, shouldIrepeat)
			i+=1
	return 0

#btype: 1 when the button might go to model types. 0 when it always goes to product
def makeButton(name, URL, btype, row = 0, shouldIrepeat = 0):
	specialb = 0
	if(btype == 1):
		specialb = Button(frame, text=name, width=50, command=lambda: listButtonCallback(URL, shouldIrepeat))
	else:
		specialb = Button(frame, text=name, width=50, command=lambda: listButtonCallback2(URL, shouldIrepeat))
	specialb.grid(row=row, column=1)
	extraButtons.append(specialb)

myList =  ["Welcome to the Dell Systems Analytical Tool. ","What would you like to do next?"]

Label(frame, text="", width=20, background="#DDECEF").grid(row=0, column=0)

i = 0
for elem in myList:  
    w = Label(frame, text=elem, background="#DDECEF")
    w.grid(row=i, column=1)
    i+=1

selectb1 =  Button(frame, text="View the details of a specific product", width=30, command=lambda: createSearchBar())
selectb1.grid(row=2, column=1)
selectb2 =  Button(frame, text="Compare the prices of Dell products", width=30, command=lambda: pressButtonForPriceComparison())
selectb2.grid(row=3, column=1)
empty = Label(frame, text="", width=50, wraplength=300, background="#DDECEF")
empty.grid(row=4, column=1)
Button(frame, text="Quit", command=root.destroy).grid(row=0, column=2)
root.mainloop()