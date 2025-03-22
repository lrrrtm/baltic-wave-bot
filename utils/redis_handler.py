import redis

from dotenv import load_dotenv
from os import getenv

load_dotenv()

class RedisHandler:
    def __init__(self, host=getenv('REDIS_HOST'), port=getenv('REDIS_PORT'), db=getenv('REDIS_DB')):
        self.host = host
        self.port = port
        self.db = db

    def get_connection(self):
        """
        Создает новое подключение к Redis
        """
        return redis.Redis(host=self.host, port=self.port, db=self.db)

    def get_value(self, key):
        """
        Получение значения по ключу
        """
        with self.get_connection() as redis_client:
            value = redis_client.get(key)
            if value:
                return value.decode('utf-8')
        return None

    def set_value(self, key, value, ttl=None):
        """
        Установка ключа, значения и TTL
        """
        with self.get_connection() as redis_client:
            result = redis_client.set(key, value, ex=ttl)
        return result


if __name__ == '__main__':
    r = RedisHandler()
    r.set_value('key', 'value')
    print(r.get_value('key'))