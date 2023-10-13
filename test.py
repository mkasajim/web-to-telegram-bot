import requests
import re
import bs4 as bs
import urllib.parse

def report_change(url):
    html_response = (requests.get(url)).text
    soup = bs.BeautifulSoup(html_response,'lxml')

    # Extract text
    txt = soup.select_one(".n-body > ul").get_text()
    notice = (re.sub(r'\n\s*\n', '\n', txt)).strip()
    # print(notice)
    latest_notice = notice.split('\n', 1)[0]

    # Extract URLs
    list_items = soup.select(".n-body > ul > li a")
    urls = [urllib.parse.urljoin(url, li['href']) for li in list_items]
    
    # # Print URLs (optional)
    # for u in urls:
    #     print(u)

    markdown = f"[{latest_notice}]({urls[0]})"
    print(markdown)  # Outputs: [text](url)


    # print(urls[0])

    # return urls

url = 'https://www.bangabasi.ac.in/'
report_change(url)
