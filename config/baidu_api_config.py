import os
from dotenv import load_dotenv

load_dotenv()

BAIDU_API_KEY = os.getenv("Y2Oj3mbizKc4iEEtA0awsg3y")
BAIDU_SECRET_KEY = os.getenv("e0PoH1PCc423TmiDP7CzEccfZFgrpGWx")
BAIDU_FOOD_API_URL = "https://aip.baidubce.com/rest/2.0/image-classify/v2/food"
