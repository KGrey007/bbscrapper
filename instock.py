from bs4 import BeautifulSoup

import requests
site_name = "https://www.bestbuy.com/site/computer-cards-components/video-graphics-cards/abcat0507002.c?id=abcat0507002"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'}

listitems = []
maxPages = 1
curr_depth = 0;

def isOut(listitem):
  listitem = str(listitem)
  if listitem.find("Add to Cart") >= 0:
    return True
  else:
    return False

def gpuScraper(headers, listitems, site_name, maxPages, curr_depth):
  print("Scraping page " + str(curr_depth + 1))

  if maxPages == curr_depth + 1 and curr_depth > 0:
    site_root = requests.get(site_name, headers=headers)
    soup = BeautifulSoup(site_root.text, 'html.parser')
    soup.prettify()
    itemBank = soup.find_all("li", class_="sku-item");
    for x in itemBank:
      if isOut(x):
        listitems.append(x)
    return listitems

  site_root = requests.get(site_name, headers=headers)
  soup = BeautifulSoup(site_root.text, 'html.parser')
  soup.prettify()

  linkBank = soup.find_all("li", class_="page-item");
  potMax = len(linkBank)
  if potMax > maxPages:
    maxPages = potMax

  bankIndex = 0
  found = None
  for listed in linkBank:
    tempstr = str(listed)
    if 0 <= tempstr.find("Selected"):
      found = bankIndex
      bankIndex += 1
    else:
      bankIndex += 1

  items = linkBank[int(found) + 1].find_all('a')
  item = items[0].get('href')

  itemBank = soup.find_all("li", class_="sku-item");
  for x in itemBank:
    if isOut(x):
      listitems.append(x)

  curr_depth += 1
  return gpuScraper(headers, listitems, item, maxPages, curr_depth)


print("Starting Domain: " + str(site_name))
gpuScraper(headers, listitems, site_name, maxPages, curr_depth)

print("Number of GPUs currently in stock at BestBuy: " + str(len(listitems)))
