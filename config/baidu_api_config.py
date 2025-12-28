import os
from dotenv import load_dotenv

load_dotenv()

BAIDU_API_KEY = os.getenv("BAIDU_API_KEY")
BAIDU_SECRET_KEY = os.getenv("BAIDU_SECRET_KEY")
BAIDU_FOOD_API_URL = "https://aip.baidubce.com/rest/2.0/image-classify/v2/food"
