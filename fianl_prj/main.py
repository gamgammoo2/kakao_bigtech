from fastapi import FastAPI, HTTPException
import httpx
from pydantic import BaseModel

app = FastAPI()

# 영화 및 음식 추천 데이터
MOVIE_RECOMMENDATIONS = {
    "맑음": [
        {"title": "La La Land", "genre": "Musical"},
        {"title": "파묘", "genre": "스릴러"},
        {"title": "어벤져스", "genre": "액션"},
        {"title": "인셉션", "genre": "SF"},
        {"title": "해리포터", "genre": "판타지"},
        {"title": "인터스텔라", "genre": "SF"},
        {"title": "그래비티", "genre": "드라마"},
        {"title": "포레스트 검프", "genre": "드라마"},
        {"title": "월터의 상상은 현실이 된다", "genre": "드라마"},
        {"title": "라따뚜이", "genre": "애니메이션"}
    ],
    "구름많음": [
        {"title": "셰이프 오브 워터", "genre": "드라마"},
        {"title": "이터널 선샤인", "genre": "로맨스"},
        {"title": "그랜드 부다페스트 호텔", "genre": "코미디"},
        {"title": "트루먼 쇼", "genre": "드라마"},
        {"title": "노트북", "genre": "로맨스"},
        {"title": "메멘토", "genre": "스릴러"},
        {"title": "다크 나이트", "genre": "액션"},
        {"title": "킹스맨", "genre": "액션"},
        {"title": "로마", "genre": "드라마"},
        {"title": "이터널스", "genre": "액션"}
    ],
    "흐림": [
        {"title": "블레이드 러너 2049", "genre": "SF"},
        {"title": "헐", "genre": "드라마"},
        {"title": "배트맨 비긴즈", "genre": "액션"},
        {"title": "어바웃 타임", "genre": "로맨스"},
        {"title": "택시 드라이버", "genre": "드라마"},
        {"title": "제미니 맨", "genre": "액션"},
        {"title": "슈퍼배드", "genre": "애니메이션"},
        {"title": "인터스텔라", "genre": "SF"},
        {"title": "매트릭스", "genre": "액션"},
        {"title": "아이언맨", "genre": "액션"}
    ]
}

FOOD_RECOMMENDATIONS = {
    "맑음": [
        {"name": "냉국수", "type": "한식"},
        {"name": "샐러드", "type": "건강식"},
        {"name": "파스타", "type": "이탈리안"},
        {"name": "초밥", "type": "일식"},
        {"name": "볶음밥", "type": "한식"},
        {"name": "김밥", "type": "한식"},
        {"name": "아이스크림", "type": "디저트"},
        {"name": "샌드위치", "type": "간식"},
        {"name": "타코", "type": "멕시칸"},
        {"name": "햄버거", "type": "패스트푸드"}
    ],
    "구름많음": [
        {"name": "라면", "type": "한식"},
        {"name": "파전", "type": "한식"},
        {"name": "피자", "type": "이탈리안"},
        {"name": "떡볶이", "type": "한식"},
        {"name": "부침개", "type": "한식"},
        {"name": "오뎅", "type": "일식"},
        {"name": "햄버거", "type": "패스트푸드"},
        {"name": "핫도그", "type": "간식"},
        {"name": "수제비", "type": "한식"},
        {"name": "카레", "type": "인도음식"}
    ],
    "흐림": [
        {"name": "된장찌개", "type": "한식"},
        {"name": "김치찌개", "type": "한식"},
        {"name": "국밥", "type": "한식"},
        {"name": "찜닭", "type": "한식"},
        {"name": "갈비찜", "type": "한식"},
        {"name": "족발", "type": "한식"},
        {"name": "쌀국수", "type": "베트남음식"},
        {"name": "부대찌개", "type": "한식"},
        {"name": "순두부찌개", "type": "한식"},
        {"name": "스테이크", "type": "양식"}
    ]
}

# JSON 형태의 날씨 데이터를 받기 위한 Pydantic 모델
class WeatherRequest(BaseModel):
    # city: str
    # forecast_time: str
    # temperature: str
    weather_condition: str


# 외부에서 날씨 데이터를 가져오는 함수
async def fetch_weather_from_weather_api():
    async with httpx.AsyncClient() as client:
        response = await client.get("http://localhost:3005/weather/pangyo")
        if response.status_code == 200:
            return response.json()
        else:
            raise HTTPException(status_code=500, detail="Failed to fetch weather data")

# 외부 weather API에서 날씨를 받아서 추천하는 API
@app.get("/recommend-from-api/")
async def get_recommendations_from_api():
    # 외부 API에서 날씨 데이터 가져오기
    weather_data = await fetch_weather_from_weather_api()
    weather_condition = weather_data.get("weather_condition", "맑음")
    
    # 날씨에 따른 영화 및 음식 추천 로직
    movies = MOVIE_RECOMMENDATIONS.get(weather_condition, [])
    foods = FOOD_RECOMMENDATIONS.get(weather_condition, [])
    
    return {
        "weather": {
            "status": weather_condition,
            "forecast_time": weather_data.get("forecast_time"),
        },
        "recommend": {
            "movie": movies[:10],  # 상위 10개 영화 추천
            "foods": foods[:10]    # 상위 10개 음식 추천
        }
    }