import yaml
from typing import List, Union, Optional, Dict
from nats.js import api
from pydantic import BaseModel

DEFAULT_JS_SUB_PENDING_MSGS_LIMIT = 512 * 1024
DEFAULT_JS_SUB_PENDING_BYTES_LIMIT = 256 * 1024 * 1024


class BaseConf(BaseModel):
    pass


class ConnConf(BaseConf):
    servers: Union[str, List[str]] = ["nats://localhost:4222"]
    options: Dict = {}


class KVConf(BaseConf):
    config: Optional[api.KeyValueConfig] = None
    params: Dict = {}


class PubConf(BaseConf):
    subject: str
    timeout: float = None
    stream: str = None
    headers: Dict = {}


class SubConf(BaseConf):
    subject: str
    mode: Optional[str] = None
    queue: Optional[str] = None
    durable: Optional[str] = None
    stream: Optional[str] = None
    config: Optional[api.ConsumerConfig] = {}
    manual_ack: bool = False
    ordered_consumer: bool = False
    idle_heartbeat: Optional[float] = None
    flow_control: bool = False
    pending_msgs_limit: Optional[int] = DEFAULT_JS_SUB_PENDING_MSGS_LIMIT
    pending_bytes_limit: Optional[int] = DEFAULT_JS_SUB_PENDING_BYTES_LIMIT
    # 拉取模式的超时时间
    pull_timeout: Optional[int] = 5


class NatsConf(BaseConf):
    conn_conf: ConnConf
    stream_opts: Dict = {}
    kv_conf: KVConf = {}
    pub_conf: PubConf = {}
    sub_conf: SubConf = {}
    los_conf: Dict = {}


class BaseNodeConf(BaseConf):
    params: Dict
    nats: NatsConf

    @staticmethod
    def load(conf_fp):
        with open(conf_fp, 'r') as f:
            conf = yaml.safe_load(f.read())
        return BaseNodeConf(**conf)


if __name__ == '__main__':
    fp = "/Users/lijianan/Documents/workspace/playground/learn_nats/box/conf/node_1.yml"
    cfg = BaseNodeConf.load(fp)
    print(dict(cfg))
    print(type(cfg))
    print(cfg.nats.pub_conf.subject)
    # print(BaseNodeConf.to_yaml(cfg))
    # print(cfg.nats.to_yaml())
