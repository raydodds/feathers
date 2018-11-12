#
#	feather_scraper.py
#	Pulls feathers from FWS Feather Atlas
#

__author__ = "Raymond Dodds"


#	IMPORTS

from bs4 import BeautifulSoup
import requests
import os

#	CONSTANTS

baseURL = "https://www.fws.gov/lab/featheratlas/"
browseURL = "browse.php"

def main():

	# Scrape order browse page
	bsoup = getPageSoup(baseURL+browseURL)
	olList = filterLinksByTerm(bsoup, "Order")

	orders = []
	for link in olList:
		url = link['href']
		name = link['href'][24:]

		new_order = Taxa(name, url)
		orders += [new_order]

	print("Finished getting orders")


	# Scrape family browse pages for each order
	families = []
	for order in orders:
		osoup = getPageSoup(baseURL+order.url)
		fllist = filterLinksByTerm(osoup, "Family")
		
		for link in fllist:
			url = link['href']
			name = link['href'][25:]

			new_family = Taxa(name, url)
			families += [new_family]
			order.addChild(new_family)

	print("Finished getting families")

	# Scrape species/common name browse pages for each family
	species = []
	for family in families:
		fsoup = getPageSoup(baseURL+family.url)
		sllist = filterLinksByTerm(fsoup, "CommonName")

		for link in sllist:
			url = link['href']
			name = link['href'][30:]
			
			new_species = Taxa(name, url)
			species += [new_species]
			family.addChild(new_species)

	print("Finished getting species")

	# Scrape image urls from species browse pages	
	images = []
	for sp in species:
		ssoup = getPageSoup(baseURL+sp.url)
		illist = filterLinksByTerm(ssoup, "Bird")

		for link in illist:
			img = getImageDescByURL(link['href'])

			images += [img]
			sp.addChild(img)

	print("Finished getting image URLs")

	# Create needed directories and download images

	baseDir = './feather_images/'

	os.mkdir(baseDir)
	
	for order in orders:
		# Composite Name
		odir = baseDir + order.name + "/"
		# Make directory
		os.mkdir(odir)

		for family in order.children:
			# composite name and mkdir
			fdir = odir + family.name + "/"
			os.mkdir(fdir)

			for species in family.children:
				# composite name and mkdir
				sdir = fdir + species.name + "/"
				os.mkdir(sdir)
				for img in species.children:
					# start a process to get the image
					imgReq = requests.get(img.url)

					with open(sdir+img.name+".jpg", 'wb') as imfile:
						imfile.write(imgReq.content)

					print("Downloaded", img.name)
				print("Finished downloading", species.name)
			print("Finished downloading", family.name)
		print("Finished downloading", order.name)


	print("Done")

		
		
	

# Get image url for a given bird link
def getImageDescByURL(href):
	imageName = href[17:]	
	imageURL = baseURL + "images/feathers/" + imageName + ".jpg"

	return ImageDesc(imageName, imageURL)



# Get only links that fit the requirements
def filterLinksByTerm(soup, term):
	# Pull links that match the order links.
	linkList = soup.find_all('a', class_="", href=True)

	flList = []
	for link in linkList:
		if(term in link['href']):
			flList += [link]
	
	return flList


# Get the soup of a page
def getPageSoup(pageURL):
	# Get the order list page
	browsePage = requests.get(pageURL)

	# Make sure that the page came back right
	if(browsePage.status_code == 200):
		return BeautifulSoup(browsePage.content, 'html.parser')
	else:
		return None

class Taxa:
	def __init__(self, name, url):
		self.name = name
		self.url = url
		self.children = []

	def addChild(self, new_child):
		self.children.append(new_child)

class ImageDesc:
	def __init__(self, name, url):
		self.name = name
		self.url = url


if __name__ == "__main__":
	main()
