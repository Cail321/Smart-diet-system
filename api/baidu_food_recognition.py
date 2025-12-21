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

def recognize_food(image_path: str):
    with open(image_path, 'rb') as f:
        img_data = f.read()
    img_b64 = base64.b64encode(img_data).decode('utf-8')

    access_token = get_access_token()
    url = f"https://aip.baidubce.com/rest/2.0/image-classify/v2/food?access_token={access_token}"
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(url, data={'image': img_b64}, headers=headers)
    return response.json()