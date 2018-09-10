import redis
import rediscluster
# StrictRedisCluster


class RedisClient(object):
    slots_error_msg = "ERROR sending 'cluster slots' command to redis server"

    def __init__(self, host, hosts = None, database = 0):
        """
        hosts is an array of host records eg [
            {"host": "127.0.0.1", "port": "6379"}
        ]
        """
        try:
            self.client = StrictRedisCluster(
                startup_nodes=hosts,
                decode_responses=False)
        except rediscluster.exceptions.RedisClusterException as e:
            if e.message.startswith(self.slots_error_msg):
                self.client = redis.StrictRedis(host='localhost', port=6379, db=database)
