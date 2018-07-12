import redis

from config import *

redisHost = getConfigValue(configRedisHost)
redisPort = getConfigValue(configRedisPort)
redisCli = redis.Redis(host=redisHost, port=redisPort, db=0)
