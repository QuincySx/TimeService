import os
import configparser

cur_path = os.path.dirname(os.path.realpath(__file__))
config_path = os.path.join(cur_path, '../static/config.ini')
cf = configparser.ConfigParser()
cf.read(config_path)

configWeather = 'weatherKey'
configDebug = 'debug'
configRedisHost = 'redis-host'
configRedisPort = 'redis-port'
configRedisTimeOut = 'redis-time'

logTag = "debug"


def getConfigValue(name):
    value = cf.get("config", name)
    return value


def getLogValue(name):
    value = cf.get("log", name)
    return value
