from fastapi import FastAPI, HTTPException
import httpx
from pydantic import BaseModel
import random

app = FastAPI()

FOOD_RECOMMENDATIONS = {
    "맑음": [
        {"name": "냉국수", "type": "한식", "image": "https://recipe1.ezmember.co.kr/cache/recipe/2019/06/24/9a0ad207acad524dd64e277d9e087af31.jpg"},
        {"name": "샐러드", "type": "건강식", "image": "https://gdimg.gmarket.co.kr/2451437691/Still/600"},
        {"name": "파스타", "type": "이탈리안", "image": "https://recipe1.ezmember.co.kr/cache/recipe/2023/07/01/c623bad240bcd949a10205fb1c402eea1.jpg"},
        {"name": "초밥", "type": "일식", "image": "https://rimage.gnst.jp/livejapan.com/public/article/detail/a/00/00/a0000370/img/basic/a0000370_main.jpg"},
        {"name": "볶음밥", "type": "한식", "image": "https://recipe1.ezmember.co.kr/cache/recipe/2015/08/27/932b0eac49b0f341ee9b91553d84d9b91.jpg"},
        {"name": "김밥", "type": "한식", "image": "https://homecuisine.co.kr/files/attach/images/140/242/110/78cf4cbedd6ea82034eaa80850bca420.jpg"},
        {"name": "아이스크림", "type": "디저트", "image": "https://src.hidoc.co.kr/image/lib/2020/9/2/1599030875087_0.jpg"},
        {"name": "샌드위치", "type": "간식", "image": "https://recipe1.ezmember.co.kr/cache/recipe/2021/11/04/641c9437db7a67ab4d3bd8692283de921.jpg"},
        {"name": "타코", "type": "멕시칸", "image": "https://www.bearstaco.com/wp-content/uploads/2022/05/taco2.jpg"},
        {"name": "햄버거", "type": "패스트푸드", "image": "https://cdn.hankyung.com/photo/201908/01.20330262.1.jpg"}
    ],
    "구름많음": [
        {"name": "라면", "type": "한식", "image": "https://img.choroc.com/newshop/goods/009179/009179_1.jpg"},
        {"name": "파전", "type": "한식", "image": "https://recipe1.ezmember.co.kr/cache/recipe/2017/11/04/66fdacb7533c367a4171c2ffb7de9fba1.jpg"},
        {"name": "피자", "type": "이탈리안", "image": "https://recipe1.ezmember.co.kr/cache/recipe/2018/11/08/148ecf4dbc5aa106fa9ffc5420a5f91f1.jpg"},
        {"name": "떡볶이", "type": "한식", "image": "https://recipe1.ezmember.co.kr/cache/recipe/2023/06/29/a1a5a04e39879f1033ae07367dfee5251.jpg"},
        {"name": "부침개", "type": "한식", "image": "https://recipe1.ezmember.co.kr/cache/recipe/2019/03/23/5817dbc909ccf6e53c7a06cb9f4841a61.jpg"},
        {"name": "오뎅", "type": "일식", "image": "https://recipe1.ezmember.co.kr/cache/recipe/2016/06/16/0ca2fb196ab46ec1ffd5472bbb5076091.jpg"},
        {"name": "햄버거", "type": "패스트푸드", "image": "https://cdn.hankyung.com/photo/201908/01.20330262.1.jpg"},
        {"name": "핫도그", "type": "간식", "image": "https://recipe1.ezmember.co.kr/cache/recipe/2019/03/18/3c84dd20e3ded9c198d207bb034ee8a21.jpg"},
        {"name": "수제비", "type": "한식", "image": "https://recipe1.ezmember.co.kr/cache/recipe/2018/08/06/995888655ae22da585af1427d0969642.jpg"},
        {"name": "카레", "type": "인도음식", "image": ""}
    ],
    "흐림": [
        {"name": "된장찌개", "type": "한식", "image": "https://recipe1.ezmember.co.kr/cache/recipe/2016/06/08/24c312f82313faaf1e4d5ef98761efcb1.jpg"},
        {"name": "김치찌개", "type": "한식", "image": "https://recipe1.ezmember.co.kr/cache/recipe/2015/06/08/fa3cd1800838bf561ea00b7552e9866a.jpg"},
        {"name": "국밥", "type": "한식", "image": "https://recipe1.ezmember.co.kr/cache/recipe/2022/09/29/428f9f2b8c23b64b190259bd6158a9b31.jpg"},
        {"name": "찜닭", "type": "한식", "image": "https://recipe1.ezmember.co.kr/cache/recipe/2016/12/05/cc1cb7798af9717f70a4772e5b53f0091.jpg"},
        {"name": "갈비찜", "type": "한식", "image": "https://recipe1.ezmember.co.kr/cache/recipe/2019/02/09/9377ac695a85566adfda9817b73438f31.jpg"},
        {"name": "족발", "type": "한식", "image": "https://recipe1.ezmember.co.kr/cache/recipe/2022/07/06/89d71f054c25989bd58368b82b1533471.jpg"},
        {"name": "쌀국수", "type": "베트남음식", "image": "https://recipe1.ezmember.co.kr/cache/recipe/2020/09/06/ee00d6e59def943bc0eb0354fb58a00d1.jpg"},
        {"name": "부대찌개", "type": "한식", "image": "https://recipe1.ezmember.co.kr/cache/recipe/2018/02/27/b5806f01ccb6f6d5d9aa94bdd6f4287e1.jpg"},
        {"name": "순두부찌개", "type": "한식", "image": "https://pds.joongang.co.kr/news/component/htmlphoto_mmdata/202108/25/0e57ae5e-f672-4551-aec0-19c6a523b010.jpg"},
        {"name": "스테이크", "type": "양식", "image": "https://recipe1.ezmember.co.kr/cache/recipe/2017/07/09/6741acc7f6bf0f7d04245851fb365c311.jpg"}
    ]
}

async def get_movie_recommendations(weather_condition: str):
    # 영화 api 가져오기
    api_key = "d4afba9f5b0bf66a17e5b35fc31e8c93"
    api_url = "https://api.themoviedb.org/3/movie/"

    # 날씨별로 장르 추천 묶기
    genre_map = {
        "맑음": ["Action", "Adventure", "Comedy", "Animation", "Drama", "Fantasy", "Romance"],
        "구름많음": ["Action", "Animation", "Crime", "Comedy", "Fantasy", "Horror", "Mystery", "Sci-Fi", "War", "History"],
        "흐림": ["Crime", "History", "Family", "Drama", "Horror", "Music", "Mystery", "Thriller", "Action"]
    }

    async with httpx.AsyncClient() as client:
        recommendations = []
        while len(recommendations) < 10:
            movie_id = random.randint(2, 100000)
            response = await client.get(f"{api_url}{movie_id}?api_key={api_key}&append_to_response=videos,images")
            if response.status_code == 200:
                data = response.json()
                genres = [genre["name"] for genre in data["genres"]]
                if any(genre in genre_map[weather_condition] for genre in genres):
                    poster_path = data["poster_path"]
                    poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}" #포스터 url ㅏ겨죠오기
                    recommendations.append({
                        "title": data["title"],
                        "genre": ", ".join(genres),
                        "poster_image": poster_url
                    })

    return recommendations

# 날씨 받아오는 api에서 JSON 형태로 받을려고 Pydantic 사용
class WeatherRequest(BaseModel):
    weather_condition: str

# 외부(weather의 api)에서 날씨 데이터를 가져오는 함수
async def fetch_weather_from_weather_api():
    async with httpx.AsyncClient() as client:
        response = await client.get("http://localhost:3005/weather/pangyo")
        if response.status_code == 200:
            return response.json()
        else:
            raise HTTPException(status_code=500, detail="Failed to fetch weather data")

@app.get("/recommend-from-api/")
async def get_recommendations_from_api():
    # 날씨 데이터 가져오는 함수 작동
    weather_data = await fetch_weather_from_weather_api()
    weather_condition = weather_data.get("weather_condition", "맑음")

    # 영화 및 음식 추천 가져오기
    movie_recommendations = await get_movie_recommendations(weather_condition)
    food_recommendations = FOOD_RECOMMENDATIONS.get(weather_condition, [])

    return {
        "weather": {
            "status": weather_condition,
            "forecast_time": weather_data.get("forecast_time"),
        },
        "recommend": {
            "movie": movie_recommendations,
            "foods": food_recommendations
        }
    }