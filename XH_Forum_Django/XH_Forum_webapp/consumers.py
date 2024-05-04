from channels.generic.websocket import AsyncWebsocketConsumer
from .models import WebSocketConnection
from .models import Notification
from channels.exceptions import StopConsumer
from asgiref.sync import async_to_sync
from channels.db import database_sync_to_async
import json
import uuid
class ChatConsumer(AsyncWebsocketConsumer):
    async def websocket_connect(self, message):
        print("有人来连接了。。。。")
        await self.accept()
        await self.save_websocket_connection()
        pending_messages = await database_sync_to_async(Notification.objects.filter)(
            receiver_id=self.scope['user'].username, is_sent=False
        )
        ordered_messages = await database_sync_to_async(list)(pending_messages.order_by('created_at'))
        if len(ordered_messages) > 0:
            for message in ordered_messages:
                # 构造要发送的消息内容
                forwarded_message = {
                    'sender_id': message.sender_id,
                    'content': message.message
                }
                await self.send_forwarded_message({
                    'type': 'send_forwarded_message',
                    'message': forwarded_message
                })
                # 更新消息的 is_sent 字段为 True
                message.is_sent = True
                await database_sync_to_async(message.save)()
        else:
            pass

    @database_sync_to_async
    def save_websocket_connection(self):
        receiver_id = self.scope['user'].username
        connection_id = self.channel_name
        # 创建或更新 WebSocketConnection 实例
        websocket_connection, _ = WebSocketConnection.objects.update_or_create(
            receiver_id=receiver_id,
            defaults={'connection_id': connection_id}
        )

    async def websocket_disconnect(self, message):
        await self.close()
        await self.delete_websocket_connection()
    @database_sync_to_async
    def delete_websocket_connection(self):
        # 从数据库中删除 WebSocket 连接信息
        receiver_id = self.scope['user'].username

        # 删除 WebSocketConnection 实例
        try:
            websocket_connection = WebSocketConnection.objects.get(receiver_id=receiver_id)
            websocket_connection.delete()
        except WebSocketConnection.DoesNotExist:
        # 处理找不到 WebSocketConnection 实例的情况
           pass

    async def websocket_receive(self, message):
        Message = json.loads(message['text'])
        receiver = Message.get('receiver_id')
        sender = Message.get('sender_id')
        content = Message.get('content')
        print(sender,"发给",receiver,":",content)
        await self.forward_message(sender, receiver, content)

    @database_sync_to_async
    def get_websocket_connection(self, receiver_id):
        return WebSocketConnection.objects.get(receiver_id=receiver_id)
    
    async def forward_message(self, sender_id, receiver_id, content):
    # 根据接收者 ID 查询对应的连接 ID
      try:
        receiver_connection = await self.get_websocket_connection(receiver_id)
        connection_id = receiver_connection.connection_id
        print(connection_id)
        # 构造要发送的消息内容
        forwarded_message = {
            'sender_id': sender_id,
            'content': content
        }
        notification = await database_sync_to_async(Notification.objects.create)(
            sender_id=sender_id,
            receiver_id=receiver_id,
            message=content,
            is_sent=True
        )
        await self.channel_layer.send(
            connection_id,
            {
                'type': 'send_forwarded_message',
                'message': forwarded_message
            }
        )

        # 向接收者的连接 ID 发送转发消息
      except WebSocketConnection.DoesNotExist:
        # 处理找不到接收者连接的情况
        notification = await database_sync_to_async(Notification.objects.create)(
            sender_id=sender_id,
            receiver_id=receiver_id,
            message=content,
            is_sent=False
        )
        print("找不到接收者连接")
      except Exception as e:
        # 处理其他异常情况
        notification = await database_sync_to_async(Notification.objects.create)(
            sender_id=sender_id,
            receiver_id=receiver_id,
            message=content,
            is_sent=False
        )
        # 添加适当的处理逻辑，例如记录日志等
        print(f"转发消息失败: {str(e)}")
    
    async def send_forwarded_message(self, event):
        message = event['message']
        await self.send(json.dumps(message))