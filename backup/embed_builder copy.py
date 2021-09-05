import asyncio
import discord
from discord.ext import commands
from discord_ui.cogs import subslash_cog, context_cog, slash_cog  
from discord_ui import UI, SlashedSubCommand, EphemeralMessage, SlashOption, ActionRow, Button
from utils.locale import Locale
from utils.embeds import Embeds

class Info:
    version = "1.0.0"
    author = "CC Team"
    name = "Welcome"
    description = "Welcome Messages"
    dev_mode = True

class EmbedBuilder(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot
        self.ui: UI = self.bot.ui

    @slash_cog("create_embed", guild_ids=[883465097283002439], options=[SlashOption(discord.TextChannel, name="channel", required=True), SlashOption(int, "embed_count", required=False)])
    async def create_embed(self, ctx: commands.Context, channel: discord.TextChannel, embed_count: int = 1):
        """
        Create an embed.
        """
        locale = Locale.from_guild_id(self.bot, ctx.guild_id)
        embeds = Embeds.from_locale(self.bot, locale)
        default_embed = discord.Embed(title=locale.get_message("cog_embed_builder_default_embed_title"), description="Edit this with \"description\"", color=0x00ff00)
        await ctx.send(embed=embeds.success(locale.get_message("cog_embed_builder_default_embed_sent", {'channel': channel.mention})))
        await channel.send(embeds=[default_embed] * embed_count)

    @context_cog("message", "Edit Embed", guild_ids=[883465097283002439])
    async def edit_embed(self, ctx: SlashedSubCommand, message: discord.Message):
        locale = Locale.from_guild_id(self.bot, ctx.guild_id)
        embeds = Embeds.from_locale(self.bot, locale)
        await ctx.defer(True)
        if message.author.id != self.bot.user.id:
            return await ctx.respond(embed=embeds.fail(locale.get_message("cog_embed_builder_edit_not_own")), hidden=True)    

        msg = None
        embed_position = 0
        actions = 0
        if len(message.embeds) == 0:
            embed = discord.Embed()
        else:
            if len(message.embeds) > 1:
                # select embed
                msg = await ctx.respond(embed=embeds.info(locale.get_message("cog_embed_builder_select_embed")))
                try:
                    w_f_m: discord.Message = await self.bot.wait_for("message", check=lambda m: m.author.id == ctx.author.id, timeout=15)
                    if w_f_m.content.isnumeric():
                        # check if it's in range
                        if int(w_f_m.content) > len(message.embeds) or int(w_f_m.content) < 0:
                            return await msg.edit(embed=embeds.fail(locale.get_message("cog_embed_builder_edit_invalid_position"))) 
                        embed_position = int(w_f_m.content)-1
                        embed = message.embeds[embed_position]
                        await w_f_m.delete()
                    else:
                        return await ctx.respond(embed=embeds.fail(locale.get_message("cog_embed_builder_edit_invalid_position")))
                except asyncio.TimeoutError:
                    await w_f_m.delete()
                    return await msg.edit(embed=embeds.fail(locale.get_message("cog_embed_builder_timeout")))

            else:
                embed = message.embeds[0]
        if msg is not None:
            await msg.edit(locale.get_message("cog_embed_builder_you_can_edit_now"), embed=embed)
        else:
            components = [
                [
                    Button("emb:edit:title", locale.get_message("cog_embed_builder_component_labels_title")),
                    Button("emb:edit:description", locale.get_message("cog_embed_builder_component_labels_description"))
                ]
            ]
            msg: EphemeralMessage = await ctx.send(locale.get_message("cog_embed_builder_you_can_edit_now"), embed=embed, components=components, hidden=True)
            #await msg.edit(embed=embed)
        while True:
            try:
                actions += 1
                w_f: discord.Message = await self.bot.wait_for("message", check=lambda msg: msg.author.id == ctx.author.id, timeout=60)
                #await w_f.delete()
                cmd = w_f.content.split(" ")[0]
                msg_without_cmd = w_f.content.removeprefix(cmd + " ")

                embed = embed.to_dict()
                print(cmd, msg_without_cmd, embed[cmd])
                embed[cmd] = msg_without_cmd
                embed = discord.Embed.from_dict(embed)
                
                if cmd.lower() == "title":
                    embed.title = msg_without_cmd
                elif cmd.lower() == "save":
                    try:
                        if embed_position == 0:
                            await message.edit(embed=embed)
                        else:
                            all_embeds =  message.embeds
                            all_embeds[embed_position] = embed
                            await message.edit(embeds=all_embeds)
                    except:
                        pass
                    await ctx.channel.purge(limit=actions, check=lambda m: m.author.id == ctx.author.id, bulk=True)
                    await msg.edit(embed=embeds.success(locale.get_message("cog_embed_builder_saved")), content=None)
                    break
                elif cmd.lower() == "cancel":
                    await msg.edit(embed = embeds.success(locale.get_message("cog_embed_builder_canceled")))
                    break                

                try:
                    await msg.edit(embed=embed)
                except Exception as ex:
                    await ctx.channel.purge(limit=actions, check=lambda m: m.author.id == ctx.author.id, bulk=True)
                    await ctx.respond(embed=embeds.fail(locale.get_message("cog_embed_builder_edit_failed")))
                    raise
                    break
            except asyncio.TimeoutError as ex:
                actions =- 1


    @commands.Cog.listener("on_ready")
    async def on_ready(self):
        await self.bot.ui.slash.sync_commands(True)

def setup(bot):
    bot.add_cog(EmbedBuilder(bot))