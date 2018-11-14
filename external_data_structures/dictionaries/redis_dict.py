import redis
from functools import wraps

from .prototype import ProtoTypeDict
from generic_encoders import ComposedEncoder, JsonEncoder, GzipEncoder, TextEncoder
from generic_encoders.encoders.no_op_encoder import NoOpEncoder


default_key_serializer = NoOpEncoder()
default_object_serializer = ComposedEncoder(JsonEncoder(), TextEncoder(), GzipEncoder())


class RedisDict(ProtoTypeDict):
  scan_count = 1000

  def __init__(
    self,
    prefix='',
    host = None,
    port = 6379,
    database = 0,
    redis_client = None,
    key_serializer=default_key_serializer,
    serializer=default_object_serializer):
    if redis_client is not None:
      self.redis_client = redis_client
    else:
      self.redis_client =redis.StrictRedis(
        host=host,
        port=port,
        db=database)
    super(RedisDict, self).__init__(
      prefix=prefix,
      key_serializer=key_serializer,
      serializer=serializer)

  def __getitem__(self, key):
    return self.serializer.decode(self.redis_client.get(self.make_key(key)))

  def __setitem__(self, key, value):
    value = self.serializer.encode(value)
    self.redis_client.set(self.make_key(key), value)

  def __contains__(self, key):
    return self.redis_client.exists(self.make_key(key))

  def iterkeys(self):
    for key in self.redis_client.scan_iter(self.prefix + '*', count=self.scan_count):
      key = self._strip_key_prefix_and_decode(key)
      yield key

  def iteritems(self):
    iterator = self.redis_client.scan_iter(self.prefix + '*', count=self.scan_count)
    for key in :
      key = self._strip_key_prefix_and_decode(key)
      yield key


