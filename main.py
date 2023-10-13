import requests
import re
import os
import schedule
import time
import bs4 as bs
import urllib.parse
import pymongo

# #### For development

# from dotenv import load_dotenv

# # Load the .env file
# load_dotenv()

# ### For development

# Connect to MongoDB
mongo_uri = os.getenv('DB_URI')
client = pymongo.MongoClient(mongo_uri)
db = client['url_changes']  # database name
collection = db['url_data']  # collection name

# Send a message via a telegram bot
def telegram_bot_sendtext(bot_message):
    bot_token = os.getenv('BOT_TOKEN')
    bot_chatID = os.getenv('CHAT_ID')
    message = bot_message
    params = {'text': message}
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&' + urllib.parse.urlencode(params)

    response = requests.get(send_text)

    return response.json()

def report_change(url):
    html_response = (requests.get(url)).text
    soup = bs.BeautifulSoup(html_response,'lxml')
    txt = soup.select_one(".n-body > ul").get_text()
    notice = (re.sub(r'\n\s*\n', '\n', txt)).strip()

    # Check if MongoDB document exists for the given URL
    document = collection.find_one({"url": url})

    if document:
        cached_notice = document['notice']
        if notice != cached_notice:
            collection.update_one({"url": url}, {"$set": {"notice": notice}})
            print("website change reported!")
            latest_notice = notice.split('\n', 1)[0]

            # Extract URLs
            list_items = soup.select(".n-body > ul > li a")
            urls = [urllib.parse.urljoin(url, li['href']) for li in list_items]
            
            # # Print URLs (optional)
            # for u in urls:
            #     print(u)

            markdown = f"[{latest_notice}]({urls[0]})"
            print(markdown)  # Outputs: [text](url)
            # print(latest_notice)
            # telegram_bot_sendtext(latest_notice)
            telegram_bot_sendtext(markdown)
        else:
            print("no change")
    else:
        latest_notice = notice.split('\n', 1)[0]
        # print(latest_notice)
        # Extract URLs
        list_items = soup.select(".n-body > ul > li a")
        urls = [urllib.parse.urljoin(url, li['href']) for li in list_items]
        
        # # Print URLs (optional)
        # for u in urls:
        #     print(u)

        markdown = f"[{latest_notice}]({urls[0]})"
        print(markdown)  # Outputs: [text](url)

        # telegram_bot_sendtext(latest_notice)
        telegram_bot_sendtext(markdown)
        print(f"no cache document for {url} found, creating one...")
        collection.insert_one({"url": url, "notice": notice})

def scan_url():
    with open("urls.txt") as urls_file:
        urls_list = urls_file.readlines()
    urls_list = [x.strip() for x in urls_list]
    
    for url in urls_list:
        report_change(url)
        time.sleep(1)

scan_url()
schedule.every(300).seconds.do(scan_url)
while True:
    schedule.run_pending()
    time.sleep(1)
