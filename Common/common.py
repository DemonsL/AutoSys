# coding: utf-8
import random
import redis
from Config import db


class RedisClient:
    # 代理分数
    MAX_SCORE = 100
    MIN_SCORE = 0
    INITIAL_SCORE = 10

    REDIS_KEY = 'proxies'

    def __init__(self, host=db.REDIS_HOST, port=db.REDIS_PORT, password=db.REDIS_PASS):
        """
        初始化
        :param host: Redis 地址
        :param port: Redis 端口
        :param password: Redis密码
        """
        self.db = redis.StrictRedis(host=host, port=port, password=password, decode_responses=True)

    def random(self):
        """
        随机获取有效代理，首先尝试获取最高分数代理，如果不存在，按照排名获取，否则异常
        :return: 随机代理
        """
        result = self.db.zrangebyscore(self.REDIS_KEY, self.MAX_SCORE, self.MAX_SCORE)
        if len(result):
            return random.choice(result)
        else:
            result = self.db.zrevrange(self.REDIS_KEY, 0, 100)
            if len(result):
                return random.choice(result)
            else:
                raise repr('代理IP池已经枯竭')




# Test
if __name__ == '__main__':

    redis_cli = RedisClient()
    ip = redis_cli.random()
    print(ip)
    # >>> 27.109.117.242:8080
