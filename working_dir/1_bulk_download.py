#!/usr/bin/env python
'''this script bulk downloads the precipitation files from the CHIRPS domain.

Author  : albert nkwasa
Contact : nkwasa.albert@gmail.com / albert.nkwasa@vub.be 
Date    : 2021.07.30

'''

import os
from bs4 import BeautifulSoup
import requests
from requests import get
import certifi
import urllib3

working_dir = os.path.dirname(os.path.realpath(__file__))
os.chdir(working_dir)
# http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())

# domain = 'https://hydrosheds.cr.usgs.gov'

# http_setup = ['https://data.chc.ucsb.edu/products/CHIRPS-2.0/africa_daily/tifs/p05/2021/']
http_setup = ['https://data.chc.ucsb.edu/products/CHIRPS-2.0/africa_daily/tifs/p05/1989/', 'https://data.chc.ucsb.edu/products/CHIRPS-2.0/africa_daily/tifs/p05/1990/',
              'https://data.chc.ucsb.edu/products/CHIRPS-2.0/africa_daily/tifs/p05/1991/', 'https://data.chc.ucsb.edu/products/CHIRPS-2.0/africa_daily/tifs/p05/1992/',
              'https://data.chc.ucsb.edu/products/CHIRPS-2.0/africa_daily/tifs/p05/1993/', 'https://data.chc.ucsb.edu/products/CHIRPS-2.0/africa_daily/tifs/p05/1994/',
              'https://data.chc.ucsb.edu/products/CHIRPS-2.0/africa_daily/tifs/p05/1995/', 'https://data.chc.ucsb.edu/products/CHIRPS-2.0/africa_daily/tifs/p05/1996/',
              'https://data.chc.ucsb.edu/products/CHIRPS-2.0/africa_daily/tifs/p05/1997/', 'https://data.chc.ucsb.edu/products/CHIRPS-2.0/africa_daily/tifs/p05/1998/',
              'https://data.chc.ucsb.edu/products/CHIRPS-2.0/africa_daily/tifs/p05/1999/', 'https://data.chc.ucsb.edu/products/CHIRPS-2.0/africa_daily/tifs/p05/2000/',
              'https://data.chc.ucsb.edu/products/CHIRPS-2.0/africa_daily/tifs/p05/2001/', 'https://data.chc.ucsb.edu/products/CHIRPS-2.0/africa_daily/tifs/p05/2002/',
              'https://data.chc.ucsb.edu/products/CHIRPS-2.0/africa_daily/tifs/p05/2003/', 'https://data.chc.ucsb.edu/products/CHIRPS-2.0/africa_daily/tifs/p05/2004/',
              'https://data.chc.ucsb.edu/products/CHIRPS-2.0/africa_daily/tifs/p05/2005/', 'https://data.chc.ucsb.edu/products/CHIRPS-2.0/africa_daily/tifs/p05/2006/',
              'https://data.chc.ucsb.edu/products/CHIRPS-2.0/africa_daily/tifs/p05/2007/', 'https://data.chc.ucsb.edu/products/CHIRPS-2.0/africa_daily/tifs/p05/2008/',
              'https://data.chc.ucsb.edu/products/CHIRPS-2.0/africa_daily/tifs/p05/2009/', 'https://data.chc.ucsb.edu/products/CHIRPS-2.0/africa_daily/tifs/p05/2010/',
              'https://data.chc.ucsb.edu/products/CHIRPS-2.0/africa_daily/tifs/p05/2011/', 'https://data.chc.ucsb.edu/products/CHIRPS-2.0/africa_daily/tifs/p05/2012/',
              'https://data.chc.ucsb.edu/products/CHIRPS-2.0/africa_daily/tifs/p05/2013/', 'https://data.chc.ucsb.edu/products/CHIRPS-2.0/africa_daily/tifs/p05/2014/',
              'https://data.chc.ucsb.edu/products/CHIRPS-2.0/africa_daily/tifs/p05/2015/', 'https://data.chc.ucsb.edu/products/CHIRPS-2.0/africa_daily/tifs/p05/2016/',
              'https://data.chc.ucsb.edu/products/CHIRPS-2.0/africa_daily/tifs/p05/2017/', 'https://data.chc.ucsb.edu/products/CHIRPS-2.0/africa_daily/tifs/p05/2018/',
              'https://data.chc.ucsb.edu/products/CHIRPS-2.0/africa_daily/tifs/p05/2019/', 'https://data.chc.ucsb.edu/products/CHIRPS-2.0/africa_daily/tifs/p05/2020/'
              'https://data.chc.ucsb.edu/products/CHIRPS-2.0/africa_daily/tifs/p05/2021/']

for site in http_setup:

    page = requests.get(site)

    html = page.text

    soup = BeautifulSoup(html, 'html.parser')

    for link in soup.find_all('a'):
        url = site + link.get('href')
        if '.tif.gz' in url:
            file_name = url.split('/')[-1]
            with open(file_name, 'wb') as file:
                response = get(url)
                file.write(response.content)
        else:
            continue


print('\t >finished')
