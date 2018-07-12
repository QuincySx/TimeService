import os
from config import getConfigValue, configWeather
from urllib import request
import json


# {
# "cloud":"0", 云量
# "cond_code":"104", 实况天气状况代码
# "cond_txt":"阴", 实况天气状况代码
# "fl":"29", 体感温度，默认单位：摄氏度
# "hum":"74", 相对湿度
# "pcpn":"0.0", 降水量
# "pres":"1008", 大气压强
# "tmp":"27", 温度，默认单位：摄氏度
# "vis":"3", 能见度，默认单位：公里
# "wind_deg":"199", 风向360角度
# "wind_dir":"西南风", 风向
# "wind_sc":"2", 风力
# "wind_spd":"11" 风速，公里/小时
# }
class heWeather:
    def getWeatherBy(self, location):
        longitude = location[0]
        latitude = location[1]

        key = getConfigValue(configWeather)
        url = "https://free-api.heweather.com/s6/weather/now?key=" + key + "&location=" + longitude + "," + latitude

        with request.urlopen(url) as f:
            data = f.read()
            print('Status:', f.status, f.reason)
            # for k, v in f.getheaders():
            #     print('%s: %s' % (k, v))
            print('Data:', data.decode('utf-8'))
            jsonObject = json.loads(data.decode("utf-8"))
            weatherStatus = jsonObject['HeWeather6'][0]['now']
        return weatherStatus

    def getCity(self, location):
        longitude = location[0]
        latitude = location[1]

        key = getConfigValue(configWeather)
        url = "https://search.heweather.com/find?key=" + key + "&location=" + longitude + "," + latitude

        print('Request:', url)
        with request.urlopen(url) as f:
            data = f.read()
            print('Status:', f.status, f.reason)
            # for k, v in f.getheaders():
            #     print('%s: %s' % (k, v))
            print('Data:', data.decode('utf-8'))
            jsonObject = json.loads(data.decode("utf-8"))

            basic = jsonObject['HeWeather6'][0]['basic'][0]

            cid = basic["cid"]
            location = basic["location"]
            parent_city = basic["parent_city"]
            admin_area = basic["admin_area"]
            cnty = basic["cnty"]

        return basic
