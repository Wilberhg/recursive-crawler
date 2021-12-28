from urllib.request import urlopen
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import re
import datetime
import random

pages = set()
random.seed(datetime.datetime.now())

def get_internal_links(soup, include_url):
    incluve_url = f'{urlparse(include_url).scheme}://{urlparse(include_url).netloc}'
    internal_links = []

    for link in soup.find_all('a', href=re.compile('^(/|.*'+include_url+')')):
        if link.attrs['href'] is not None:
            if link.attrs['href'] not in internal_links:
                if(link.attrs['href'].startswith('/')):
                    internal_links.append(include_url+link.attrs['href'])
                else:
                    internal_links.append(link.attrs['href'])
    return internal_links

def get_external_links(soup, exclude_url):
    external_links = []
    for link in soup.find_all('a', href=re.compile('^(http|www)((?!'+exclude_url+').)*$')):
        if link.attrs['href'] is not None:
            if link.attrs['href'] not in external_links:
                external_links.append(link.attrs['href'])
    return external_links

def get_random_external_link(starting_page):
    html = urlopen(starting_page)
    soup = BeautifulSoup(html, 'html.parser')
    external_links = get_external_links(soup, urlparse(starting_page).netloc)
    if len(external_links) == 0:
        print('No external links, looking around the site for one')
        domain = f'{urlparse(starting_page).scheme}://{urlparse(starting_page).netloc}'
        internal_links = get_external_links(soup, domain)
        return get_random_external_link(internal_links[random.randint(0, len(internal_links)-1)])
    else:
        return external_links[random.randint(0, len(external_links)-1)]

def follow_external_only(starting_site):
    external_link = get_random_external_link(starting_site)
    print(f'Random external link is {external_link}')
    follow_external_only(external_link)

follow_external_only('http://oreilly.com')
