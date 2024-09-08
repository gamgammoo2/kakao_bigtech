from fastapi import FastAPI
import requests
from datetime import datetime, timedelta
import os
import xmltodict
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

# FastAPI 인스턴스 생성
app = FastAPI()

# 날씨 데이터를 크롤링하는 함수
def get_weather_data():
    service_key = os.getenv("SERVICE_KEY")
    url = 'http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst'
    
    now = datetime.now() - timedelta(minutes=150)
    base_date = now.strftime("%Y%m%d")  # YYYYMMDD 형식
    base_time = now.strftime("%H%M")  # HHMM 형식 (기준 시간)
    
    params = {
        'serviceKey': service_key,
        'numOfRows': '10',
        'pageNo': '1',
        'base_date': base_date,
        'base_time': base_time,
        'nx': '55',
        'ny': '127',
        'dataType': 'XML'
    }

    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        parsed_data = xmltodict.parse(response.text)
        items = parsed_data['response']['body']['items']['item']
        # 필요한 데이터 추출 (SKY 카테고리)
        for item in items:
            if item['category'] == 'SKY':
                value = item['fcstValue']
                fcst_time = item['fcstTime']
                
                if value == '1':
                    return '맑음', fcst_time
                elif value == '3':
                    return '구름많음', fcst_time
                elif value == '4':
                    return '흐림', fcst_time
                
    return '알 수 없음', None

# FastAPI 엔드포인트: 날씨 데이터 제공
@app.get("/weather/")
async def fetch_weather():
    weather_status, forecast_time = get_weather_data()
    return {"weather_status": weather_status, "forecast_time": forecast_time}
    print(weather_status, forecast_time)
