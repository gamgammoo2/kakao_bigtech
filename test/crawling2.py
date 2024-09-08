from bs4 import BeautifulSoup
#import requests
from datetime import datetime
from requests_html import HTMLSession

session = HTMLSession()

#기상청 url
#url = 'https://www.weather.go.kr/w/weather/forecast/short-term.do'

#response = requests.get(url)
response = session.get('https://www.weather.go.kr/w/weather/forecast/short-term.do')
# JavaScript 처리
response.html.render()

# 렌더된 페이지에서 원하는 데이터 추출
weather_div = response.html.find('div.dfs-daily-slider-body', first=True)

# HTML 내용을 출력
print(weather_div.html)

# soup = BeautifulSoup(response.text, 'html.parser') #페이지 가져오기
# with open("weather_page.html", "w", encoding="utf-8") as file:
#     file.write(soup.prettify())  # 보기 좋게 들여쓰기 포함해서 저장

# today = datetime.today().strftime('%Y-%m-%d') #오늘날짜 가져와 필요한 형태로 변형
# target_date = today

# slider_body = soup.find("div", {"class": "dfs-daily-slider-body"})
# print(slider_body)
# if slider_body:
#     weather_div = slider_body.find("div", {"data-date": target_date})

#     if weather_div:
#         am_weather = weather_div.find("span", {"class": "wic NB01"}) #오전 날씨
#         am_weather_text = am_weather.get('title') if am_weather else 'N/A'
        
#         pm_weather = weather_div.find("span", {"class": "wic NB03"}) #오후 날씨
#         pm_weather_text = pm_weather.get('title') if pm_weather else 'N/A'
        
#         print(f"날짜: {target_date}")
#         print(f"오전 날씨: {am_weather_text}")
#         print(f"오후 날씨: {pm_weather_text}")
#     else:
#         print(f"날짜 {target_date}에 대한 정보를 찾을 수 없습니다.")

