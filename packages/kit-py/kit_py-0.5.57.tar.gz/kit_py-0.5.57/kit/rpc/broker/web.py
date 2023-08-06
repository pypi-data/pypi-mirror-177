# -*- coding: utf-8 -*-
import threading
from queue import Queue, Empty

from fastapi import FastAPI, Response
import uvicorn

from kit.rpc.broker import Broker


class WebBroker(Broker):

    def __init__(self,
                 app: FastAPI,
                 host: str = "0.0.0.0",
                 port: int = 8090,
                 path: str = "/push", **kwargs):
        super().__init__()
        self.queue = Queue()
        self.app = app
        self.path = path
        self.host = host
        self.port = port
        self.kwargs = kwargs

        self._create_server()

    def _create_server(self):
        self.app.add_route(self.path, self.push, methods=["POST"])
        threading.Thread(target=self.run_server).start()

    def run_server(self):
        uvicorn.run(self.app, host=self.host, port=self.port, **self.kwargs)

    async def push(self, request):
        message = (await request.json()).get("message")
        if message is None:
            return Response(status_code=400)
        self.queue.put_nowait(message)
        return Response("ok")

    def consume(self, prefetch, timeout):
        return Consumer(self.queue, prefetch=prefetch, timeout=timeout)


class Consumer:

    def __init__(self, queue, prefetch, timeout):
        self.queue = queue
        self.prefetch = prefetch
        self.timeout = timeout

    def ack(self, *args, **kwargs):
        print("ack")

    def nack(self, *args, **kwargs):
        print("nack")

    def __next__(self):
        try:
            return self.queue.get(timeout=self.timeout / 1000)
        except Empty:
            return None

    def __iter__(self):  # pragma: no cover
        return self
