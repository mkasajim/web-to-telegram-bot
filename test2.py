import requests
import bs4 as bs
import urllib.parse

def report_change(url):
    response = requests.get(url)
    soup = bs.BeautifulSoup(response.text, 'lxml')

    # Find the first li element in the quick-links section
    li_element = soup.select_one(".qiick-links > ul > li")

    # Extract date and notice text
    date = li_element.find("span", class_="neWs_date").get_text(strip=True)
    notice_text = li_element.find("h5").get_text(strip=True)

    # Extract URL
    notice_url = li_element.find("a")['href']
    full_url = urllib.parse.urljoin(url, notice_url)

    # Format output
    markdown = f"Date: {date}\nNews: [{notice_text}]({full_url})"
    print(markdown)

url = 'https://www.bangabasi.ac.in/'
report_change(url)
