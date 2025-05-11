# encoding:utf-8
import requests

# 接口地址
url = "https://api.map.baidu.com/staticimage/v2"

# 此处填写你在控制台-应用管理-创建应用后获取的AK
ak = "aAxFCwZS6RWt6WtcefzDbCBTpRjdvFAx"

params = {
    "width":    "280",
    "height":    "140",
    "zoom":    "10",
    "ak":       ak,
}

response = requests.get(url=url, params=params)
if response:
    print(response.text)