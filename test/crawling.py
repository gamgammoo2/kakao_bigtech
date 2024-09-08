import requests
import xmltodict
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

# 날씨 API에 사용할 기본 정보를 설정하는 함수
def get_weather_data():
    # API 요청에 필요한 파라미터들
    service_key = os.getenv("SERVICE_KEY")
    url = 'http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtNcst'

    # 현재 날짜 및 시간 가져오기
    base_date = datetime.now().strftime("%Y%m%d")  # 현재 날짜를 'YYYYMMDD' 형식으로
    base_time = "1800"  # 요청하려는 시간
    
    # API 요청에 사용할 파라미터
    params = {
        'serviceKey': service_key,  # API 인증 키
        'numOfRows': '10',  # 한 번에 받아올 데이터 수
        'pageNo': '1',  # 페이지 번호
        'base_date': base_date,  # 기준 날짜
        'base_time': base_time,  # 기준 시간
        'nx': '55',  # 격자 X 좌표 (예시 값)
        'ny': '127',  # 격자 Y 좌표 (예시 값)
        'dataType': 'XML'  # 응답 형식 (XML)
    }

    # 요청 보내기
    response = requests.get(url, params=params)
    print(response)
    # 요청이 성공했는지 확인
    if response.status_code == 200:
        # XML 응답을 딕셔너리로 파싱
        parsed_data = xmltodict.parse(response.text)
        
        # 응답 데이터에서 필요한 값 추출
        try:
            items = parsed_data['response']['body']['items']['item']
            weather_data = {}

            # 필요한 데이터 추출
            for item in items:
                category = item['category']  # 데이터 종류 (기온, 습도 등)
                value = item['obsrValue']  # 실제 측정된 값

                # 기온, 습도, 강수량 등 카테고리에 맞는 값을 딕셔너리에 저장
                if category == 'T1H':  # 기온
                    weather_data['temperature'] = value
                elif category == 'RN1':  # 1시간 강수량
                    weather_data['rain'] = value
                elif category == 'REH':  # 습도
                    weather_data['humidity'] = value
                elif category == 'WSD':  # 풍속
                    weather_data['wind_speed'] = value

            return weather_data
        
        except KeyError as e:
            print(f"API 응답에서 필요한 키를 찾을 수 없습니다: {e}")
            return None
    else:
        print(f"API 요청에 실패했습니다. 상태 코드: {response.status_code}")
        return None

# 날씨 데이터 출력
weather_data = get_weather_data()
if weather_data:
    print(f"현재 기온: {weather_data.get('temperature')}°C")
    print(f"현재 습도: {weather_data.get('humidity')}%")
    print(f"현재 1시간 강수량: {weather_data.get('rain')}mm")
    print(f"현재 풍속: {weather_data.get('wind_speed')}m/s")
