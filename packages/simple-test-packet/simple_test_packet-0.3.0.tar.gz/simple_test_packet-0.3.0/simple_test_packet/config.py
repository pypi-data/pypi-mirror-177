import sys

import redis


# Connect to Redis server
def redis_connect() -> redis.client.Redis:
    try:
        client = redis.Redis(
            host="redis",
            port=6379,
        )
        ping = client.ping()
        if ping is True:
            return client
    except redis.AuthenticationError:
        print("AuthenticationError")
        sys.exit(1)
