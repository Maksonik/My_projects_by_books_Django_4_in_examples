import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import async_to_sync
from django.utils import timezone


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        self.id = self.scope['url_route']['kwargs']['course_id']
        self.room_groop_name = f'chat_{self.id}'
        # присоединиться к группе чат-комнаты
        await self.channel_layer.group_add(
            self.room_groop_name,
            self.channel_name
        )
        # принять соединение
        await self.accept()

    async  def disconnect(self, close_code):
        # покинуть группу чат-комнаты
        await self.channel_layer.group_discard(
            self.room_groop_name,
            self.channel_name
        )

    # получить сообщение из WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        # отправить сообщение в группу чат-комнаты
        await self.channel_layer.group_send(
            self.room_groop_name,
            {
                'type' : 'chat_message',
                'message' : message,
                'user' : self.user.username,
                'datetime' : timezone.now().isoformat()
            }
        )

    #получить сообщение из группы чат-комнаты
    async def chat_message(self, event):
        #отправить сообщение в веб-сокет
        await self.send(text_data=json.dumps(event))