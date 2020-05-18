
import csv
import requests
# 2) get the html structure using beautofulSoup
from bs4 import BeautifulSoup


# 1) get the page url
def getPage(url):
	response = requests.get(url)
	
	# check response status
	if not response.ok:
		print('server responded: ', response.status_code)
	else:
		# using beautifulSoup here that contain 2 param,
		# 	i) the html resourse
		#   ii) 'lxml'
		soup = BeautifulSoup(response.text, 'lxml')

	# return the soup data
	return soup

# 3) get the data details from html by function with the return of pageUrl as param. 
def getDetailProduct(soup):
	# get the product title using params of html tag element
	try:
		title = soup.find('h1', id='itemTitle').text.strip().split('  ')[1].replace('\xa0', '')
	except:
		title = ''

	# get the price & currency
	try:
		try:
			try:
				data = soup.find('span', id='prcIsum').text.strip().replace('$', '')
			except:
				data = soup.find('span', id='prcIsum_bidPrice').text.strip().replace('$', '')
		except:
			data = soup.find('span', id='mm-saleDscPrc').text.strip().replace('$', '')
		currency, price = data.split(' ')
	except:
		currency = ''
		price = ''

	# get qty of sold
	try:
		try:
			sold = soup.find('span', class_='vi-qtyS-hot-red').find('a').text.strip().split(' ')[0]
		except:
			sold = soup.find('span', class_='vi-qtyS').find('a').text.strip().split(' ')[0]
	except:
		sold = ''

	# 4) pack all the results as a single data with type of list/python-array
	data = {
		'title': title,
		'currency': currency,
		'price': price,
		'total sold': sold
	}

	return data

# 5) scrape all links with details products by looking at the web page & pagination
def getDataLinkOnPage(soup):
	try:
		links = soup.findAll('a', class_='s-item__link')
	except:
		links = []
	
	# 6) get only the href link urls
	urls = [item.get('href') for item in links]

	return urls

# 9) create CSV as an output file => need to import CSV on top of the code
def createCsv(data, url):
	with open('output.csv', 'a') as csvfile:
		writer = csv.writer(csvfile)


		row = [data['title'], data['price'], data['currency'], data['total sold'], url]

		writer.writerow(row)


# MAIN Function that runs every time
def main():
	url = 'https://www.ebay.com/sch/i.html?_nkw=iphone&_pgn=3'
	
	# 7) get the getail product for all data links by iterating getDetailProduct on every getDataLink urls
	urlsProducts = getDataLinkOnPage(getPage(url))

	# 8) iterating the product details
	for link in urlsProducts:
		data = getDetailProduct(getPage(link))
		# 10) call create csv file function
		createCsv(data, link)
		# print(data)

if __name__ == '__main__':
	main()