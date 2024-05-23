import pandas
from fake_useragent import UserAgent
import requests
import os
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from chromedriver_py import binary_path
import os
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

ua = UserAgent().random
url = 'https://tracker.gg/valorant/leaderboards/ranked/all/default?page=2&region=global&act=22d10d66-4d2a-a340-6c54-408c7bd53807'

scriptdir = os.path.dirname(__file__) 

for i in range(300, 301):
    svc = webdriver.ChromeService(executable_path=binary_path)
    driver = webdriver.Chrome(service=svc)
    ua = UserAgent().random
    url = 'https://tracker.gg/valorant/leaderboards/ranked/all/default?page=' + str(i) + '&region=global&act=4539cac3-47ae-90e5-3d01-b3812ca3274e'
    driver.get(url=url)
    time.sleep(6)
    src = driver.page_source
    soup = bs(src, 'html.parser')
    table = soup.find('table', {'class': 'trn-table'})
    trs = table.find_all('tr')
    ll = []
    for tr in trs[1:]:
        username = tr.find('span', {'class': 'trn-ign__username'}).text
        tag = tr.find('span', {'class': 'trn-ign__discriminator'}).text
        ut = (username, tag)
        ll.append(ut)
    with open(os.path.join(scriptdir, 'Pages', f'userPage-{i}.txt'), 'w', encoding='utf-8') as f:
        nlist = [f"USER: {i[0]};;;TAG: {i[1]}" for i in ll]
        f.write('\n'.join(nlist))
        f.close()
    driver.quit()
    print(i)