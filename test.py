import requests

req=requests.get("https://uapis.cn/api/v1/network/ipinfo",params={"ip": "120.229.67.75"})
jsonres = req.json()
region = jsonres["region"]
print(region)