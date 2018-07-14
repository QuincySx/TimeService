# -*- coding: utf-8 -*-
import json

from flask import Flask, request

from config import *
from jsonType import obj2dict
from redisDB import redisCli
from weather import heWeather

app = Flask(__name__)
weather = heWeather()


@app.route('/')
def getWeather():
    global cid
    global weatherStatus
    global response

    args = request.args.get("location", '0,0')
    print(args)
    location = args.split(",")
    try:
        basic = weather.getCity(location)
        cid = basic["cid"]
        place = basic["location"]
        parent_city = basic["parent_city"]
        admin_area = basic["admin_area"]
        cnty = basic["cnty"]
    except BaseException:
        print("error:", "连接 Redis 异常")
        weatherStatus = None
        response = generateErrorResponse("获取城市失败")
        return json.dumps(obj2dict(response))

    try:
        weatherStatus = redisCli.get(cid)
    except BaseException as e:
        print("error:", "连接 Redis 异常", str(e))
        weatherStatus = None

    if weatherStatus is None:
        try:
            now = weather.getWeatherBy(location)
            time = getConfigValue(configRedisTimeOut)
            cloud = now['cloud']
            cond_code = now['cond_code']
            cond_txt = now['cond_txt']
            fl = now['fl']
            tmp = now['tmp']
            pcpn = now['pcpn']
            weatherResponse = {
                'place': place,
                'parent_city': parent_city,
                'admin_area': admin_area,
                'cloud': cloud,
                'cond_code': cond_code,
                'cond_txt': cond_txt,
                'fl': fl,
                'tmp': tmp,
                'pcpn': pcpn
            }

            weatherStatus = json.dumps(weatherResponse, ensure_ascii=False)
            redisCli.setex(cid, weatherStatus, time)
        except BaseException as e:
            print("error:", "连接 Redis 异常", str(e))
            if weatherStatus is None:
                response = generateErrorResponse("获取天气失败")

    if weatherStatus is not None:
        response = generateSuccessResponse(weatherStatus)

    print(response)
    return json.dumps(response, ensure_ascii=False)


def generateErrorResponse(message):
    return generateResponse(1, message, "")


def generateSuccessResponse(data):
    return generateResponse(0, "", data)


def generateResponse(error, message, data):
    return {
        'error': error,
        'message': message,
        'data': data,
    }


if __name__ == '__main__':
    debug = getConfigValue(configDebug)
    app.run(host='0.0.0.0', port=8011, debug=debug)
