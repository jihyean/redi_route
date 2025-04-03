from fastapi import FastAPI, HTTPException
from starlette.responses import RedirectResponse
import redis
from pydantic import BaseModel
import os

app = FastAPI()
r = redis.Redis(host="redis", port=6379, decode_responses=True)  # Redis 컨테이너 이름 사용

BASE_URL = os.getenv("BASE_URL", "http://moa")  # 환경 변수에서 기본 도메인 설정

class UrlRequest(BaseModel):
    original_url: str
    short_code: str

@app.post("/shorten")
def shorten_url(request: UrlRequest):
    if not request.original_url.startswith("http"):
        raise HTTPException(status_code=400, detail="Invalid URL")

    short_code = request.short_code
    if r.exists(f"short:{short_code}"):
        raise HTTPException(status_code=400, detail="Short code already in use")

    r.set(f"short:{short_code}", request.original_url)
    return {"short_url": f"{BASE_URL}/{short_code}"}

@app.get("/{short_code}")
def redirect_url(short_code: str):
    original_url = r.get(f"short:{short_code}")
    if not original_url:
        raise HTTPException(status_code=404, detail="Short URL not found")
    return RedirectResponse(url=original_url)