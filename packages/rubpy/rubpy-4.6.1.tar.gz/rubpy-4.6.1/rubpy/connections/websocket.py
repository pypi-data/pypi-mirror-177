import websockets
from ujson import dumps, loads
from ..encryption import Encryption
from urllib.request import urlopen
from random import choice


class WebSocket(object):
    def __init__(self, auth):
        #self.auth: str = auth
        self.data = {'api_version': '4', 'auth': auth, 'data_enc': '', 'method': 'handShake'}
        self.enc = Encryption(auth)
        self.__WSaddress = list(loads(urlopen('https://getdcmess.iranlms.ir/').read().decode('utf-8')).get('data').get('socket').values())

    async def handShake(self, urI):
        async for websocket in websockets.connect(urI):
            try:
                await websocket.send(dumps(self.data))
                while True:
                    data = await websocket.recv()
                    if data != '{"status":"OK","status_det":"OK"}': yield loads(data)
                    else: continue
            except websockets.ConnectionClosed: continue

    async def handler(self, chat_updates=False, message_updates=True, show_notifications=False):
        async for message in self.handShake(choice(self.__WSaddress)):
            if message.get('type') == 'messenger':
                data = loads(self.enc.decrypt(message.get('data_enc')))
                if message_updates:
                    for m_u in data.get('message_updates'): yield m_u
                elif chat_updates:
                    for c_u in data.get('chat_updates'): yield c_u
                else:
                    for s_n in data.get('show_notifications'): yield s_n