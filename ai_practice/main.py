from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from datetime import datetime
import requests

app = FastAPI()

# 정적 파일(css, 이미지 등)을 제공하는 경로 설정
app.mount("/static", StaticFiles(directory="static"), name="static")

# 템플릿 디렉터리 설정
templates = Jinja2Templates(directory="templates")

# 외부 API에서 날씨 데이터를 가져오는 함수
def fetch_weather_from_api():
    try:
        response = requests.get("http://localhost:8000/weather/")  # weather API 호출
        if response.status_code == 200:
            return response.json()
        else:
            return {"weather_status": "알 수 없음", "forecast_time": "00:00"}
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return {"weather_status": "알 수 없음", "forecast_time": "00:00"}

# 메인 페이지 HTML 반환 엔드포인트
@app.get("/", response_class=HTMLResponse)
async def get_homepage(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# 메인 페이지 엔드포인트 (JSON 반환)
@app.get("/api/data")
async def read_root():
    # 현재 시간 가져오기
    current_time = datetime.now().strftime("%H:%M")
    
    # 날씨 데이터 가져오기 (외부 API 호출)
    weather_data = fetch_weather_from_api()
    weather_status = weather_data.get("weather_status", "알 수 없음")
    forecast_time = weather_data.get("forecast_time", "00:00")

    # 추천 영화와 음식 (예시 데이터)
    movie_recommendations = [{"title": "Inception", "genre": "Sci-Fi"}, {"title": "Interstellar", "genre": "Sci-Fi"}, {"title": "shapeofwater", "genre": "Sci-Fi"}, {"title": "eternalsunshine", "genre": "romance"}]
    food_recommendations = [{"name": "샐러드", "type": "건강식"}, {"name": "파스타", "type": "이탈리안"}, {"name": "카레", "type": "인도"}, {"name": "사케동", "type": "일식"}]

    # JSON 형식으로 반환
    return {
        "current_time": current_time,
        "weather_status": weather_status,
        "movie_recommendations": movie_recommendations,
        "food_recommendations": food_recommendations
    }