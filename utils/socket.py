from discord import Forbidden, NotFound, embeds
import socketio
import discord
from discord.ext import commands 
class Socket:
    # socket io
    def __init__(self,client,  host):
        self.client: commands.Bot = client
        self.host = host
        self.socket = socketio.AsyncClient()
        self.register_events()
    
    async def connect(self):
        await self.socket.connect(self.host)


    def register_events(self):
        @self.socket.on('connect')
        async def on_connect():
            await self.socket.emit("auth", {"token": self.client.http.token })
            print('Connected')
        
        @self.socket.on('disconnect')
        async def on_disconnect():
            print('Disconnected')
        
        @self.socket.on('connect_error')
        async def on_connect_error(error):
            print('Connect Error: ' + str(error))
        
        @self.socket.on('cog_embed_builder_get_json')
        async def on_cog_embed_builder_get_json(data: dict):
            print('cog_embed_builder_get_json: ' + str(data))
            self.client.dispatch('cog_embed_builder_get_json', data)
            request_data: dict = data.get("data")
            if request_data == None:
                return
            to_socket_id = request_data.get("to_socket_id")
            if to_socket_id == None:
                return
            channel_id = request_data.get("channel_id", 0)
            message_id = request_data.get("message_id", 0)
            channel: discord.TextChannel = self.client.get_channel(channel_id)
            if channel == None:
                try:
                    channel = await self.client.fetch_channel(channel_id)
                except NotFound:
                    await self.socket.emit("cog_embed_builder_get_json_callback", {"code": 1, "data": {"to_socket_id": to_socket_id, "success": False, "json": {"message": "Channel not found"}}})
                    return
                except Forbidden:
                    await self.socket.emit("cog_embed_builder_get_json_callback",{"code": 1, "data": {"to_socket_id": to_socket_id, "success": False, "json": {"message": "I don't have permission to view this channel"}}})
                    return
            try:
                message: discord.Message = await channel.fetch_message(message_id)
                ms_dict = {
                    "content": message.system_content,
                    "embeds": [x.to_dict() for x in message.embeds]
                }
                #print(ms_dict)
                await self.socket.emit("cog_embed_builder_get_json_callback", {"code": 1,  "data": {"to_socket_id": to_socket_id, "success": True, "json": ms_dict}})
            except NotFound:
                await self.socket.emit("cog_embed_builder_get_json_callback", {"code": 1,  "data": {"to_socket_id": to_socket_id, "success": False, "json": {"message": "Message not found"}}})
                return
            except Forbidden:
                await self.socket.emit("cog_embed_builder_get_json_callback", {"code": 1,  "data": {"to_socket_id": to_socket_id, "success": False, "json": {"message": "I don't have permission to view this message"}}})
                return

            

