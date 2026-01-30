#天气获取
import requests

def GetWeather(ip : str,get_indices : bool = False): #通过IP获取近4日天气
    req=requests.get("https://uapis.cn/api/v1/network/ipinfo",params={"ip": ip})
    if req.status_code != 200:
        return {"status": "ERR_IPINFO_API_ERROR","message": "IP地理位置API异常","data": None}
    jsonres = req.json()
    region = jsonres["region"]
    req=requests.get("https://uapis.cn/api/v1/misc/weather",params={"city": region,"extended": True,"forecast": True,"indices": get_indices})
    if req.status_code != 200:
        return {"status": "ERR_WEATHER_API_ERROR","message": "天气API异常","data": None}
    jsonres = req.json()
    return {"status": "SUCCESS","message": "成功","data": jsonres}
