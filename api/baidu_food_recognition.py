import requests
import base64
from config.baidu_api_config import BAIDU_API_KEY, BAIDU_SECRET_KEY

def get_access_token():
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {
        "grant_type": "client_credentials",
        "client_id": BAIDU_API_KEY,
        "client_secret": BAIDU_SECRET_KEY
    }
    response = requests.post(url, params=params)
    return response.json().get("access_token")

def recognize_ingredient(image_path):
    """调用百度 API 识别果蔬"""
    with open(image_path, "rb") as f:
        img_b64 = base64.b64encode(f.read()).decode("utf-8")
    token = get_access_token()
    url = f"https://aip.baidubce.com/rest/2.0/image-classify/v1/classify/ingredient?access_token={token}"
    resp = requests.post(url, data={"image": img_b64}, headers={"content-type": "application/x-www-form-urlencoded"})
    return resp.json()


def recognize_dish(image_path):
    """调用百度 API 识别菜品"""
    with open(image_path, "rb") as f:
        img_b64 = base64.b64encode(f.read()).decode("utf-8")
    token = get_access_token()
    url = f"https://aip.baidubce.com/rest/2.0/image-classify/v2/dish?access_token={token}"
    resp = requests.post(url, data={"image": img_b64}, headers={"content-type": "application/x-www-form-urlencoded"})
    return resp.json()