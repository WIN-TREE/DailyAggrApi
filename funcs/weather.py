#天气获取
import requests
from dotenv import load_dotenv
import os

def GetWeather(ip : str,get_indices : bool = False): #通过IP获取近4日天气
    req = requests.get("https://uapis.cn/api/v1/network/ipinfo",params={"ip": ip})
    if req.status_code != 200:
        return {"status": "ERR_IPINFO_API_ERROR","message": "IP地理位置API异常","data": None}
    jsonres = req.json()
    region = jsonres["region"]
    req = requests.get("https://uapis.cn/api/v1/misc/weather",params={"city": region,"extended": True,"forecast": True,"indices": get_indices})
    if req.status_code != 200:
        return {"status": "ERR_WEATHER_API_ERROR","message": "天气API异常","data": None}
    jsonres = req.json()
    load_dotenv()
    aisug = None
    if os.environ.get("GLM_API_KEY") != None:
        # AI建议
        data = {
            "model": "glm-4.7-flash",
            "messages": [
                {
                    "role": "system",
                    "content": "你是一个关心生活的天气专家，用户将给你一些天气数据，你只需输出日常生活建议，尽量避免主观称呼，不要分点与换行且需简短"
                },
                {
                    "role": "user",
                    "content": f'今日最高温度是{jsonres["temp_max"]}°C，最低温度是{jsonres["temp_min"]}，紫外线指数是{jsonres["uv"]}，天气是{jsonres["weather"]}，风向是{jsonres["wind_direction"]}，体感温度是{jsonres["feels_like"]}'
                }
            ]
        }
        api_key = os.environ.get("GLM_API_KEY")
        header = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        req = requests.post("https://open.bigmodel.cn/api/paas/v4/chat/completions",json=data,headers=header)
        aisug = req.json()["choices"][0]["message"]["content"]
    jsonres["ai_suggestion"] = aisug
    return {"status": "SUCCESS","message": "成功","data": jsonres}
