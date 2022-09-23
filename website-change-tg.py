# UrlChange
# Checks for an updates to a given list of urls, and reports changes

# Tested with Python version 3.7.6

import requests
import re
import os
import schedule
import time
import bs4 as bs
import urllib.parse


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
    
    file_name = ''.join(x for x in url if x.isalpha()) + ".txt"

    # Check if file exists that matches the page's content
    if os.path.exists(file_name):
        cache_file = open(file_name, "r")
        html_cache = cache_file.read()
        # If the updated set is not equal to the stored set, update and report change
        if notice != html_cache:
            cache_file = open(file_name, "w")
            cache_file.write(notice)
            print("website change reported!")
            # Send the message (such as with a telegram bot provided below)
            latest_notice = notice.split('\n', 1)[0]
            print(latest_notice)
            telegram_bot_sendtext(latest_notice)
        else:
            print("no change")
    else:
        # Send the message (such as with a telegram bot provided below)
        latest_notice = notice.split('\n', 1)[0]
        print(latest_notice)
        res = telegram_bot_sendtext(latest_notice)
        print(res)
        # save the url's html content to a file
        print("no cache file for " + url + " found, creating one...")
        cache_file = open(file_name, "w")
        cache_file.write(notice)

# Read liust of urls from file
def scan_url():
    # Get list of urls from file:
    with open("urls.txt") as urls_file:
        urls_list = urls_file.readlines()
    urls_list = [x.strip() for x in urls_list]
    # Check each url for changes
    for url in urls_list:
        report_change(url)
        time.sleep(1)

# Initalize script to run every 5 minutes
scan_url()
schedule.every(300).seconds.do(scan_url)
while True:
    schedule.run_pending()
    time.sleep(1)
