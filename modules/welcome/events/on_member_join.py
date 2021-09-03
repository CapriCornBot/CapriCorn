import discord
def register(client):
    @client.listen("on_member_join")
    async def on_member_join(member: discord.Member):
        pass