#!/usr/bin/python

from bs4 import BeautifulSoup
import urllib.request
import pandas as pd
import time

html_doc = urllib.request.urlopen("http://www.slocountyhomes.com/newlistex.php").read()

soup = BeautifulSoup(html_doc, 'html.parser')

names = [
    "MLSNumber",
    "Street",
    "City",
    "Price",
    "BR",
    "Bath",
    "Footage"
]

def extract_listings(soup):
    rows = soup.find_all("tr")
    
    new_listings = []
    
    for row in rows[1:]:
        items = row.find_all("td")
        if len(items) != 8:
            continue

        row_data = []

        try :
            for idx, item in enumerate(items):
                if idx == 7:
                    continue

                if idx == 0:
                    row_data.append(int(item.contents[0].contents[0].strip()))    
                elif idx == 3:
                    row_data.append(int(item.contents[0].strip().strip("$").replace(",","")))
                elif idx == 4 or idx == 5:
                    row_data.append(int(item.contents[0].strip()))
                elif idx == 6:
                    row_data.append(float(item.contents[0].strip()))
                else:
                    if len(item.contents) == 2:
                        row_data.append(item.contents[1].contents[0].strip())
                    else:
                        row_data.append(item.contents[0].strip().strip("$"))
        except:
            continue
        new_listings.append(row_data)
        
    return pd.DataFrame(columns=names, data=new_listings)

new_listings = extract_listings(soup)

fn = '/home/waylinw/Project3/' + time.strftime("%d-%m-%Y") + '.csv'

new_listings.to_csv(fn)
