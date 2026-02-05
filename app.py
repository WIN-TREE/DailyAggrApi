from flask import Flask,request
import funcs.weather as weather
import funcs.hotboard as hb
import funcs.epicfreegame as efg
from datetime import datetime
import random
from lunar_python import Lunar
import requests
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)
limiter = Limiter(get_remote_address,default_limits=["30/minute"])
limiter.init_app(app)

@app.route("/v1")
@limiter.exempt
def index():
    return {"status": "SUCCESS","message": "服务正常运行","data": None}, 200

@app.route("/v1/weather",methods = ['GET'])
def Weather():
    resl = weather.GetWeather(request.args.get("ip"),request.args.get("indices"))
    if resl["status"] != "SUCCESS":
        return resl, 500
    return resl, 200

@app.route("/v1/hotboard",methods = ['GET'])
def HotBoard():
    typ = request.args.get("type","")
    if typ:
        resl = hb.GetHotBoard(request.args.get("type"))
    else:
        resl = hb.GetHotBoard()
    if resl["status"] != "SUCCESS":
        return resl, 500
    return resl, 200

@app.route("/v1/epicfreegame",methods = ['GET'])
def EpicFreeGame():
    resl = efg.GetEpicFreeGame()
    if resl["status"] != "SUCCESS":
        return resl, 500
    return resl, 200

@app.route("/v1/todayluck",methods = ['GET'])
def TodayLuck():
    luckseed = datetime.now().year + datetime.now().month + datetime.now().day
    random.seed(luckseed)
    return {"status": "SUCCESS","message": "成功","data": {"result": random.randint(0,100)}}, 200

@app.route("/v1/today",methods = ['GET'])
def AboutToday():
    resl = {"status": "SUCCESS","message": "成功","data": {"year": None,"month": None,"day": None,"lunartime": None,"yi": None,"ji": None}}
    resl["data"]["year"] = datetime.now().year
    resl["data"]["month"] = datetime.now().month
    resl["data"]["day"] = datetime.now().day
    lunartoday = Lunar.fromDate(datetime.now())
    resl["data"]["lunartime"] = lunartoday.toString()
    resl["data"]["yi"] = lunartoday.getDayYi()
    resl["data"]["ji"] = lunartoday.getDayJi()
    return resl, 200

@app.route("/v1/sentence",methods = ['GET'])
def OneSentence():
    req = requests.get("https://v1.hitokoto.cn")
    if req.json()["from_who"] == None:
        from_who = "匿名"
    else:
        from_who = req.json()["from_who"]
    return {"status": "SUCCESS","message": "成功","data": {"sentence": req.json()["hitokoto"],"from_who": from_who}}, 200

@app.route("/v1/aisug",methods = ['POST'])
@limiter.limit("5/minute")
def AiSuggest():
    sug = weather.AISug(request.json["data"])
    return {"status": "SUCCESS","message": "成功","data": {"content": sug}}, 200

if __name__ == '__main__':
    app.run()