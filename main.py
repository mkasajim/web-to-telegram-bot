import requests
import re
import os
import schedule
import time
import bs4 as bs

url = "https://www.bangabasi.ac.in/"
html_response = (requests.get(url)).text
soup = bs.BeautifulSoup(html_response,'lxml')
txt = soup.select_one(".n-body > ul").get_text()
txt2 = re.sub(r'\n\s*\n', '\n', txt)

file_name = ''.join(x for x in url if x.isalpha()) + ".txt"
cache_file = open(file_name, "w")
cache_file.write(txt2)

