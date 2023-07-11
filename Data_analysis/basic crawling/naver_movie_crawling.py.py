#필요한 라이브러리
#구버전 설치
#$pip install selenium==3.14.1

#import time #페이지 로드에 걸리는 시간조절
import json #데이터 저장

from selenium import webdriver
from bs4 import BeautifulSoup

#제어를 위한 웹 드라이버를 부른다.
path = 'chromedriver.exe' #basic directory
driver = webdriver.Chrome(path)

#네이버 영화페이지 로드
url = 'https://movie.naver.com/'
driver.get(url)
#예시1 확인

############################################################

#영화검색창의 Xpath를 찾고 해당 태그를 찾는다.
input_xpath = '//*[@id="ipt_tx_srch"]'
input = driver.find_element_by_xpath(input_xpath)
#영화제목을 넘겨준다
title = "짱구"
#input.clear()
input.click() #검색창을 클릭하고,
input.send_keys(title) #검색창에 영화제목 입력

#검색버튼의 xpath를 찾는다.
search_button_xpath = '//*[@id="jSearchArea"]/div/button'
search_button = driver.find_element_by_xpath(search_button_xpath)

#버튼을 클릭하여 검색 수행
search_button.click()
#예시2확인

####################################################

#첫번째 영화 제목 링크의 xpath를 찾는다
first_title_xpath = '//*[@id="old_content"]/ul[2]/li[1]/dl/dt/a'
first_title = driver.find_element_by_xpath(first_title_xpath)

#제목을 클릭하고 상세정보로 들어간다.
first_title.click()
#예시3확인

###################################################

#평점버튼을 찾고 클릭하여 평점 메뉴를 부른다.
vote_button_xpath = '//*[@id="movieEndTabMenu"]/li[5]/a/em'
vote_button = driver.find_element_by_xpath(vote_button_xpath)

vote_button.click()

#해당 페이지의 html 소스를 읽어온다.
html = driver.page_source
soup = BeautifulSoup(html,'html.parser')

#태그를 이용해 관람객평점리스트를 찾는다.

actual_vote_list = soup.find('div',{'id':'actual_point_tab_inner'}).find_all('em')

#print(actual_vote_list)

actual_vote = ''

for tag in actual_vote_list[:4]:
    actual_vote += tag.get_text() #.get_text()하면 태그 내의 텍스트를 가져옴

print(actual_vote)

#태그를 이용해 나이대별 평점?

age_vote_list = soup.find_all('strong',{'class':'graph_point'})

age_vote = []

for tag in age_vote_list[7:]:

    age_vote.append(tag.get_text())

print(age_vote)
#예시4확인


#################################################
#수집한 데이터 저장

#방법은 여러가지
#pandas의 csv로 저장할수도 있고, pickle로 저장할수도 있고
#  일단 여기서는 json으로 저장

data = {'actual_vote':actual_vote, 'age_vote':age_vote}

file_path = 'data.json'

with open(file_path,'w') as f:
    json.dump(data, f, ensure_ascii=False)

#load data

with open(file_path, "r") as json_file:
    data_dict = json.load(json_file)
    print(data_dict)
