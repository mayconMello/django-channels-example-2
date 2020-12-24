import json
from channels.generic.websocket import AsyncWebsocketConsumer


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Obtem o room_name do parêmatro da rota da URL chat/routing.py
        self.room_name = self.scope['url_route']['kwargs']['room_name']

        # Constroi um nome de grupo de channels a partir do nome da sala capturado
        self.room_group_name = 'chat_%s' % self.room_name

        # Entra no grupo criado a partir do room_group_name
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        # Aceita a conexão WebSocket do cliente, esta deve ser a ultima ação que dirá se a conexão será aceita ou não
        await self.accept()

    async def disconnect(self, code):
        # Sai do grupo criado
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data=None, bytes_data=None):
        # Captura a mensagem enviada pelo cliente, as mensagens chegam na estrutura JSON
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Envia um evento para o grupo
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    async def chat_message(self, event):
        message = event['message']

        await self.send(text_data=json.dumps({
            'message': message
        }))
