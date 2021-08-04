from urllib.parse import urlparse
from urllib.parse import urlsplit

from collections import deque
import requests
from bs4 import BeautifulSoup
import requests.exceptions

url = 'https://grad.ucdavis.edu/admissions/admission-faqs'


new_urls = deque([url])
processed_urls = set()
local_urls = set()
foreign_urls = set()
broken_urls = set()


# process urls one by one until we exhaust the queue
while len(new_urls):    
    # move url from the queue to processed url set    
    url = new_urls.popleft()    
    processed_urls.add(url)    
    # print the current url    
    print('Processing %s' % url)


parts = urlsplit(url)
base = '{0.netloc}'.format(parts)
strip_base = base.replace('www.', '')
base_url = '{0.scheme}://{0.netloc}'.format(parts)
path = url[:url.rfind('/')+1] if '/' in parts.path else url

soup = BeautifulSoup(response.text, “lxml”)

for link in soup.find_all(‘a’):    
    # extract link url from the anchor    
    anchor = link.attrs[“href”] if “href” in link.attrs else ‘’
    if anchor.startswith(‘/’):        
        local_link = base_url + anchor        
        local_urls.add(local_link)    
    elif strip_base in anchor:        
        local_urls.add(anchor)    
    elif not anchor.startswith(‘http’):        
        local_link = path + anchor        
        local_urls.add(local_link)    
    else:        
        foreign_urls.add(anchor)

