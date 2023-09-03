#!/usr/bin/env python
# coding: utf-8

# In[1]:


from bs4 import BeautifulSoup
import json
from json import JSONDecodeError
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# 설정 파일 불러오기
with open('config.json', 'r') as f:
    config = json.load(f)

# 텔레그램 메시지 전송 함수
def send_telegram_message(token, chat_id, message):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': message
    }
    requests.post(url, params=payload)

# 웹 드라이버 설정
chrome_options = Options()
chrome_options.binary_location = config['chrome_driver_path']  # 설정 파일에서 불러오기
driver = webdriver.Chrome(options=chrome_options)

# 웹 페이지 접속
url = 'https://www.bok.or.kr/portal/bbs/P0000559/list.do?menuNo=200690'
driver.get(url)

# 페이지 로딩 대기
time.sleep(5)

# 페이지 소스 가져오기
html = driver.page_source

# BeautifulSoup 객체 생성
soup = BeautifulSoup(html, 'html.parser')

# 제목과 첨부파일 링크 추출
new_press_releases = []
for item in soup.select('a.secretSet'):
    title = item.find('span', {'class': 'titlesub'}).text.strip()
    parent = item.find_parent().find_parent()
    file_links = parent.find_all('a', href=True)
    
    file_link_list = []
    for link in file_links:
        if "fileDown.do" in link['href']:
            file_link = 'https://www.bok.or.kr' + link['href']
            file_link_list.append(file_link)
    
    new_press_releases.append({
        'title': title,
        'file_links': file_link_list
    })

# 이전에 저장된 보도자료 불러오기
try:
    with open('press_releases.json', 'r', encoding='utf-8') as f:
        old_press_releases = json.load(f)
except (FileNotFoundError, JSONDecodeError):
    old_press_releases = []    
    
# 새로운 보도자료가 있는지 확인
for new_release in new_press_releases:
    if new_release not in old_press_releases:
        message = f"새로운 보도자료: {new_release['title']}\n첨부파일 링크: {', '.join(new_release['file_links'])}"
        
        # 텔레그램 알림 전송
        send_telegram_message(config['telegram_token'], config['telegram_chat_id'], message)  # 설정 파일에서 불러오기

# 새로운 보도자료 저장
with open('press_releases.json', 'w', encoding='utf-8') as f:
    json.dump(new_press_releases, f, ensure_ascii=False, indent=4)

# 웹 드라이버 종료
driver.quit()

