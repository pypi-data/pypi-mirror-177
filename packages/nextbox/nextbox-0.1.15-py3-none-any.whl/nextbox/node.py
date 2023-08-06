import asyncio
import nats
import abc
from loguru import logger
import time
from nats.aio.msg import Msg
from nats.js.kv import KeyValue
from nats.errors import TimeoutError
from .module.los import los
from .conf import BaseNodeConf


class Node(metaclass=abc.ABCMeta):
    def __init__(self, conf: BaseNodeConf = None, conf_fp: str = None):
        logger.info("---NextBox---")
        if conf is None:
            conf = BaseNodeConf.load(conf_fp)
        self.conf = conf
        self._fps = 0
        self.js = None
        self.kv: KeyValue = None
        self.los = los(**conf.nats.los_conf)

    @property
    def fps(self):
        return self._fps

    @abc.abstractmethod
    async def process(self, msg: Msg = None):
        return

    async def _callback(self, msg: Msg = None):
        # if msg: logger.info(f'Received: {msg}')
        if msg:
            await msg.ack()
        _tic = time.time()
        pmsg = await self.process(msg)
        cost = time.time() - _tic
        self._fps = 1 / cost

        # 结果包装
        pmsg = self._warp(pmsg)

        # 发送消息
        if self.conf.nats.pub_conf.subject and pmsg is not None:
            _pmsg = bytes('{}'.format(pmsg), 'utf-8')
            ack = await self.js.publish(
                self.conf.nats.pub_conf.subject,
                payload=_pmsg,
                timeout=self.conf.nats.pub_conf.timeout,
                stream=self.conf.nats.pub_conf.stream,
                headers=self.conf.nats.pub_conf.headers
            )
            logger.debug(f"Pub[{ack}]: {pmsg}")

    async def async_start(self):
        # 建立链接
        nc = await nats.connect(servers=self.conf.nats.conn_conf.servers, **self.conf.nats.conn_conf.options)
        self.js = nc.jetstream(**self.conf.nats.stream_opts)
        # 创建js的回调
        await self.on_js_create(self.js)
        logger.debug("connect success!")

        # 构建kv
        self.kv = await self.js.create_key_value(config=self.conf.nats.kv_conf.config, **self.conf.nats.kv_conf.params)

        if self.conf.nats.sub_conf and self.conf.nats.sub_conf.subject:
            logger.debug("sub>>>")
            # 拉取模式
            if self.conf.nats.sub_conf.mode == "pull":
                osub = await self.js.pull_subscribe(
                    self.conf.nats.sub_conf.subject,
                    durable=self.conf.nats.sub_conf.durable,
                    stream=self.conf.nats.sub_conf.stream,
                    config=self.conf.nats.sub_conf.config,
                    pending_msgs_limit=self.conf.nats.sub_conf.pending_msgs_limit,
                    pending_bytes_limit=self.conf.nats.sub_conf.pending_bytes_limit
                )
                while True:
                    try:
                        msgs = await osub.fetch(timeout=self.conf.nats.sub_conf.pull_timeout)
                        msg = msgs[0]
                        await self._callback(msg)
                    except TimeoutError as e:
                        logger.exception(e)
                        continue
            else:
                # 推送模式
                osub = await self.js.subscribe(
                    self.conf.nats.sub_conf.subject,
                    queue=self.conf.nats.sub_conf.queue,
                    durable=self.conf.nats.sub_conf.durable,
                    stream=self.conf.nats.sub_conf.stream,
                    config=self.conf.nats.sub_conf.config,
                    manual_ack=self.conf.nats.sub_conf.manual_ack,
                    ordered_consumer=self.conf.nats.sub_conf.ordered_consumer,
                    idle_heartbeat=self.conf.nats.sub_conf.idle_heartbeat,
                    flow_control=self.conf.nats.sub_conf.flow_control,
                    pending_msgs_limit=self.conf.nats.sub_conf.pending_msgs_limit,
                    pending_bytes_limit=self.conf.nats.sub_conf.pending_bytes_limit
                )

                while True:
                    try:
                        msg = await osub.next_msg()
                        await self._callback(msg)
                    except TimeoutError as e:
                        logger.exception(e)
                        continue
        else:
            # 没订阅任何主题时
            while True:
                await self._callback()

    def start(self):
        asyncio.run(self.async_start())

    def _warp(self, pmsg):
        """
        对处理结果进行包装
        :param pmsg:
        :return:
        """
        return {"data": pmsg, "timeat": time.time()}

    # --------
    async def on_js_create(self, js: nats.js.JetStreamContext):
        """
        jetstream创建时回调
        :param js:
        :return:
        """
        pass
