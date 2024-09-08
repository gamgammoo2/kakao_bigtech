import requests
import xmltodict
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

def get_weather_data():
    # API 요청에 필요한 파라미터들
    service_key = os.getenv("SERVICE_KEY")
    url = 'http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst'

    # 현재 날짜 및 시간 가져오기
    base_date = datetime.now().strftime("%Y%m%d")  # 현재 날짜를 'YYYYMMDD' 형식으로
    base_time = "0500"  # 요청하려는 시간 (06시)

    # 현재 시간 계산
    current_hour = int(datetime.now().strftime("%H"))

    # API 요청에 사용할 파라미터
    params = {
        'serviceKey': service_key,  # API 인증 키
        'numOfRows': '1000',  # 한 번에 받아올 데이터 수
        'pageNo': '1',  # 페이지 번호
        'base_date': base_date,  # 기준 날짜
        'base_time': base_time,  # 기준 시간
        'nx': '55',  # 격자 X 좌표 (예시 값)
        'ny': '127',  # 격자 Y 좌표 (예시 값)
        'dataType': 'XML'  # 응답 형식 (XML)
    }

    # 요청 보내기
    response = requests.get(url, params=params)

    # 요청이 성공했는지 확인
    if response.status_code == 200:
        try:
            # XML 응답을 딕셔너리로 파싱
            parsed_data = xmltodict.parse(response.text)
            items = parsed_data['response']['body']['items']['item']
            weather_data_list = []

            # 필요한 데이터 추출 (category가 'SKY'인 것만)
            for item in items:
                category = item['category']
                if category == 'SKY':
                    value = item['fcstValue']  # 예보 값
                    fcst_date = item['fcstDate']  # 예보 날짜
                    fcst_time = item['fcstTime']  # 예보 시간

                    # fcstTime을 HH:mm 형식으로 변환
                    fcst_time_formatted = f"{fcst_time[:2]}:{fcst_time[2:]}"

                    # SKY 값에 따른 날씨 상태 설정
                    if value == '1':
                        weather_status = "맑음"
                    elif value == '3':
                        weather_status = "구름많음"
                    elif value == '4':
                        weather_status = "흐림"
                    else:
                        weather_status = "알 수 없음"

                    # 현재 시간 이후의 데이터를 저장
                    if int(fcst_time[:2]) >= current_hour:
                        weather_data = {
                            'date': fcst_date,
                            'time': fcst_time_formatted,
                            'status': weather_status
                        }
                        weather_data_list.append(weather_data)

            # 수집된 모든 데이터 출력
            if weather_data_list:
                for data in weather_data_list:
                    print(f"예보 날짜: {data['date']}")
                    print(f"측정 시간: {data['time']}")
                    print(f"날씨 상태: {data['status']}")
                    print('----------------------')

            return weather_data_list
        
        except KeyError as e:
            print(f"API 응답에서 필요한 키를 찾을 수 없습니다: {e}")
            return None
        except Exception as e:
            print(f"알 수 없는 오류 발생: {e}")
            return None
    else:
        print(f"API 요청에 실패했습니다. 상태 코드: {response.status_code}")
        return None

# 날씨 데이터 출력
weather_data = get_weather_data()
