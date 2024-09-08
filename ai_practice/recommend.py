from fastapi import FastAPI, Query
import requests

app = FastAPI()

movie_recm = {
    "맑음" : ["Inception", "Interstellar", "The Grand Budapest Hotel"],
    "구름많음": ["The Dark Knight", "The Prestige", "The Matrix"],
    "흐림": ["Blade Runner 2049", "Her", "Arrival"]
}

food_recm = {
    "맑음": ["샐러드", "파스타", "아이스크림"],
    "구름많음": ["라면", "파전", "피자"],
    "흐림": ["된장찌개", "국밥", "찜닭"]
}

# 날씨 데이터 받아오기
def get_weather_data(selected_time: str):
    # 날씨 API 호출 
    weather_api_url = f"https://weather.api.com/data?time={selected_time}"
    response = requests.get(weather_api_url)
    if response.status_code == 200:
        return response.json().get('weather_status')
    return None

# 영화 및 음식 추천 API
@app.get("/recommendations/")
async def get_recommendations(time: str = Query(..., description="사용자가 선택한 시간대")):
    # 선택한 시간대의 날씨 데이터 가져오기
    weather_status = get_weather_data(time)
    
    if weather_status is None:
        return {"error": "날씨 데이터를 가져올 수 없습니다."}
    
    # 날씨에 따른 영화 및 음식 추천
    movie_list = MOVIE_RECOMMENDATIONS.get(weather_status, [])
    food_list = FOOD_RECOMMENDATIONS.get(weather_status, [])
    
    return {
        "time": time,
        "weather_status": weather_status,
        "movies": movie_list,
        "foods": food_list
    }