# -*- coding: utf-8 -*-
from ..message import Message


class Broker:

    def __init__(self, queue=None, backend_store=None, middlewares=None):
        self.backend_store = backend_store
        self.queue = queue
        self.middlewares = []
        self.job = None

        if middlewares:
            for middleware in middlewares:
                self.add_middleware(middleware)

    def add_middleware(self, middleware):
        self.middlewares.append(middleware)

    def send(self, message):
        """
        如果当前Broker是Job的to_broker, 则必须实现此方法
        """

    def consume(self, *args, **kwargs):
        """
        如果当前Broker是Job的from_broker, 则必须实现此方法
        """

    def format_message(self, message):
        return message

    def before_emit(self, signal, *args, **kwargs):
        signal = "before_" + signal
        for middleware in self.middlewares:
            if hasattr(middleware, signal):
                getattr(middleware, signal)(self, *args, **kwargs)

    def after_emit(self, signal, *args, **kwargs):
        signal = "after_" + signal
        for middleware in self.middlewares:
            if hasattr(middleware, signal):
                getattr(middleware, signal)(self, *args, **kwargs)

    @property
    def message_class(self):
        """
        每个消息应当有自己的消息解析类，默认为Message
        消息解析类应当继承自Message，并约定`message`属性的解析方式，默认为json解析
        """
        return Message

    def __repr__(self):
        return f"<Broker {self.queue}>"
