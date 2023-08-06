import os
import time
from datetime import datetime
from email import message_from_bytes

import requests
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By

from .craigslist import Craigslist
from .email import Email

# SET UP ENVIRONMENT VARIABLES
CL_USERNAME = os.environ.get('CL_USER')
CL_PASSWORD = os.environ.get('CL_PASS')
EMAIL_ADDRESS = CL_USERNAME
EMAIL_PASSWORD = os.environ.get('CL_EMAIL_PASS')
# WEBHOOK (optional) configures the discord webhook url to send summary to
WEBHOOK = os.environ.get('DISCORD_WEBHOOK')

# MAX_POST_DAYS configures the maximum number of days old a post can be active for before it is reposted 
MAX_POST_DAYS = 11

# IMAP_SERVER for email provider, default for gmail
IMAP_SERVER = 'imap.gmail.com'

repost_count = 0
renew_count = 0

current_time = datetime.now()
inbox = Email(IMAP_SERVER, EMAIL_ADDRESS, EMAIL_PASSWORD)
cl = Craigslist()
cl.get_login_page()
cl.login(CL_USERNAME, CL_PASSWORD)
if not cl.check_logged_in():
    time.sleep(1)
    print('Not logged in, verifying login')
    cl.driver.find_element(By.CLASS_NAME, 'submit-onetime-link-button').click()
    time.sleep(5)
    for msgid, data in inbox.wait_unread_emails():
        print('Found email from craigslist')
        contents = message_from_bytes(data[b'RFC822'])
        content = contents.get_payload()[1].get_payload(decode=True)
        soup = BeautifulSoup(content, 'html.parser')
        links = soup.find_all('a', href=True)
        cl.driver.get(links[0]['href'])
        inbox.email.delete_messages(msgid)
        time.sleep(1)

time.sleep(2)
cl.filter_active_posts()
cl.set_home_window()
active_posts = cl.get_posts()
for post in active_posts:
    post_date = cl.parse_date(cl.get_post_date(post))
    if (current_time - post_date).days > MAX_POST_DAYS:
        print('Found old post, reposting')
        cl.repost(post)
        cl.driver.close()
        cl.driver.switch_to.window(cl.home_window)
        print('Reposted, waiting 120 seconds')
        repost_count += 1
        time.sleep(120)

inbox.delete_craigslist_emails()
print('Unread emails from craigslist deleted')

cl.driver.refresh()
for button in cl.get_renewal_buttons():
    print('Renewing post')
    cl.command_click(button)
    renew_count += 1
    time.sleep(2)

cl.driver.quit()

summary = f'Craigslist.com listings renewed: {renew_count}\nCraigslist.com listings reposted: {repost_count}'
print(summary)

if WEBHOOK:
    data = {'content':summary}
    result = requests.post(WEBHOOK, json = data)