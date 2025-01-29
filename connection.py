import httpx
from pydantic import BaseModel
from typing import List


class ScoreItem(BaseModel):
    id: str
    score: int
    username: str

class ApiResponse(BaseModel):
    items: List[ScoreItem]


BASE_URL = "http://127.0.0.1:8090"


def get_user_max_scores(nickname: str):
    url = f"{BASE_URL}/api/collections/max_scores/records"
    params = {
        "filter": f"username='{nickname}'"
    }

    r = httpx.get(url, params=params)
    r.raise_for_status()

    json = r.json()
    return ApiResponse(**json)

def create_user(nickname: str, score: int):
    url = f"{BASE_URL}/api/collections/max_scores/records"
    payload = {
        "username": nickname,
        "score": score
    }

    r = httpx.post(url, data=payload)
    r.raise_for_status()

def update_user_max_scores(id: str, new_score: int):
    url = f"{BASE_URL}/api/collections/max_scores/records/{id}"
    payload = {"score": new_score}

    r = httpx.patch(url, json=payload)
    r.raise_for_status()
