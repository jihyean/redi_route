from fastapi import FastAPI, HTTPException
from starlette.responses import RedirectResponse
from utils import generate_short_code
import redis
from pydantic import BaseModel
import os

app = FastAPI()
URL = f"http://localhost:1000"
r = redis.Redis(host="localhost", port=6379, decode_responses=True)
# r = redis.Redis(host="redis", port=6379, decode_responses=True)  # Redis 컨테이너 이름 사용

class UrlRequest(BaseModel):
    original_url: str
    short_code: str  # 사용자 입력을 받기 위해 추가

@app.post("/shorten")
def shorten_url(request: UrlRequest):
    if not request.original_url.startswith("http"):
        raise HTTPException(status_code=400, detail="Invalid URL")
    
    short_code = request.short_code
    # short_code가 이미 존재하는지 확인
    if r.exists(f"short:{short_code}"):
        raise HTTPException(status_code=400, detail="Short code already in use")
    
    r.set(f"short:{short_code}", request.original_url)
    return {"short_url": f"{URL}/{short_code}"}

@app.get("/{short_code}")
def redirect_url(short_code: str):
    original_url = r.get(f"short:{short_code}")
    if not original_url:
        raise HTTPException(status_code=404, detail="Short URL not found")
    return RedirectResponse(url=original_url)