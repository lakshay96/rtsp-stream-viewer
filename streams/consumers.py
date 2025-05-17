import json
from channels.generic.websocket import AsyncWebsocketConsumer
from . import stream_manager

class StreamConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Each connection is for a specific stream, identified by stream_id in URL
        self.stream_id = self.scope['url_route']['kwargs']['stream_id']
        self.group_name = f"stream_{self.stream_id}"
        # Join the channel layer group for this stream
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

        # Register this client in stream manager and start stream if needed
        stream_info = stream_manager.streams.get(self.stream_id)
        if stream_info:
            stream_info['clients'] += 1
            stream_manager.start_stream(self.stream_id)
        else:
            # If for some reason stream_id is not found (not registered via REST), reject
            await self.close()

    async def disconnect(self, close_code):
        # Leave the group
        await self.channel_layer.group_discard(self.group_name, self.channel_name)
        # Decrement client count and possibly stop the stream
        stream_info = stream_manager.streams.get(self.stream_id)
        if stream_info:
            stream_info['clients'] -= 1
            if stream_info['clients'] <= 0:
                # No more viewers for this stream
                stream_manager.stop_stream(self.stream_id)

    async def receive(self, text_data=None, bytes_data=None):
        # We can handle messages from client if needed (e.g., pause commands)
        if text_data:
            try:
                data = json.loads(text_data)
            except ValueError:
                return
            if data.get('action') == 'pause':
                # Example: client pause command could be handled by closing the socket (stop stream)
                await self.close()
            # (In this simple app, we don't expect any messages from the client.)

    async def frame_message(self, event):
        # Handler for messages sent to the group by stream_manager._stream_video
        # event can contain 'frame' or 'error'
        if 'frame' in event:
            await self.send(text_data=json.dumps({"frame": event['frame']}))
        if 'error' in event:
            await self.send(text_data=json.dumps({"error": event['error']}))
