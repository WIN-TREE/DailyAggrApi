#今日热搜
import requests

def GetHotBoard(type : str = "sina-news"): #获取今日热搜
    req = requests.get("https://uapis.cn/api/v1/misc/hotboard",params={"type": type})
    if req.status_code != 200:
        return {"status": "ERR_HOTBOARD_API_ERROR","message": "热搜API异常","data": None}
    return {"status": "SUCCESS","message": "成功","data": req.json()["list"]}