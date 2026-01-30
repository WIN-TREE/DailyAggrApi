#Epic Games免费游戏
import requests

def GetEpicFreeGame():
    req = requests.get("https://uapis.cn/api/v1/game/epic-free")
    if req.status_code != 200:
        return {"status": "ERR_EPIC_API_ERROR","message": "游戏查询API异常","data": req.json()}
    sdata = req.json()["data"]
    tgdata = []
    for i in sdata:
        req = requests.post("https://uapis.cn/api/v1/translate/text",params={"to_lang": "zh-CHS"},json={"text": i["description"]})
        i["description"] = req.json()["translate"]
        req = requests.post("https://uapis.cn/api/v1/translate/text",params={"to_lang": "zh-CHS"},json={"text": i["title"]})
        i["title"] = req.json()["translate"]
        tgdata.append(i)
    
    return {"status": "SUCCESS","message": "成功","data": tgdata}