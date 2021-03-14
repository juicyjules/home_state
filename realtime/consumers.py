import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from led_colors.models import Client
class RealtimeColorConsumer(WebsocketConsumer):
    def __init__(self, *args, **kwargs): 
        self.connections = {}
        super().__init__(*args,**kwargs)
    def connect(self):
        self.key = self.scope['url_route']['kwargs']['key']
        self.connections[self.key] = self.connections.get(self.key,0) + 1
        if self.scope["user"].is_authenticated:
            print(f'User {self.scope["user"]} connected!')
        async_to_sync(self.channel_layer.group_add)(
            self.key,
            self.channel_name
        )
        self.accept()
    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.key,
            self.channel_name
        )
        self.connections[self.key] = self.connections.get(self.key,1) - 1
        if self.scope["user"].is_authenticated:
            async_to_sync(self.channel_layer.group_send)(
                self.key,
                {
                    'type': 'send_color',
                    'color': "#000000",
                    'realtime': False
                }
            )
            Client.manager.set_realtime(self.scope["user"].id,False)

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        color = text_data_json["color"]
        async_to_sync(self.channel_layer.group_send)(
            self.key,
            {
                'type': 'send_color',
                'color': color,
                'realtime': True
            }
        )
    def send_color(self,event):
        color = event["color"]
        realtime = event["realtime"]
        self.send(text_data=json.dumps({'color':color,'realtime':realtime}))