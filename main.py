import requests
import bs4 as bs
import urllib.parse
import os
import pymongo
import schedule
import time
from pymongo.mongo_client import MongoClient

# Load the .env file during development
from dotenv import load_dotenv
load_dotenv()

# # Connect to MongoDB
# mongo_uri = os.getenv('DB_URI')
# # client = pymongo.MongoClient(mongo_uri)
# client = MongoClient(mongo_uri)

# Get the URI, username, and password from the environment
uri = os.getenv('DB_URI')
username = os.getenv('DB_USERNAME')
password = os.getenv('DB_PASSWORD')

# Create a new client and connect to the server with authentication
client = MongoClient(uri, username=username, password=password)
db = client['url_changes']  # Database name
collection = db['url_data']  # Collection name

# Send a message via a telegram bot
def telegram_bot_sendtext(bot_message):
    bot_token = os.getenv('BOT_TOKEN')
    bot_chatID = os.getenv('CHAT_ID')
    params = {'text': bot_message}
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&' + urllib.parse.urlencode(params)
    response = requests.get(send_text)
    return response.json()

def report_change(url):
    response = requests.get(url)
    soup = bs.BeautifulSoup(response.text, 'lxml')

    # Find the first li element in the quick-links section
    li_element = soup.select_one(".qiick-links > ul > li")
    if li_element:
        date = li_element.find("span", class_="neWs_date").get_text(strip=True)
        notice_text = li_element.find("h5").get_text(strip=True)
        notice_url = li_element.find("a")['href']
        full_url = urllib.parse.urljoin(url, notice_url)
        markdown = f"Date: {date}\nNews: [{notice_text}]({full_url})"

        # Check if MongoDB document exists for the given URL
        document = collection.find_one({"url": url})

        if document:
            cached_notice = document['notice']
            if markdown != cached_notice:
                collection.update_one({"url": url}, {"$set": {"notice": markdown}})
                print("Website change reported!")
                telegram_bot_sendtext(markdown)
            else:
                print("No change")
        else:
            print(f"No cache document for {url} found, creating one...")
            collection.insert_one({"url": url, "notice": markdown})
            telegram_bot_sendtext(markdown)
    else:
        print("No valid notice found at the provided URL.")

def scan_url():
    with open("urls.txt") as urls_file:
        urls_list = [x.strip() for x in urls_file.readlines()]
    
    for url in urls_list:
        report_change(url)
        time.sleep(1)

scan_url()
schedule.every(300).seconds.do(scan_url)
while True:
    schedule.run_pending()
    time.sleep(1)
