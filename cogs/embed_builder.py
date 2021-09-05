import asyncio
from re import M
import discord
from discord.ext import commands
from discord_ui.cogs import subslash_cog, context_cog, slash_cog  
from discord_ui import UI, SlashedSubCommand, EphemeralMessage, SlashOption, ActionRow, Button, PressedButton, SelectOption, SelectMenu
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
        await ctx.send(embed=embeds.success(locale.get_message("cog_embed_builder_default_embed_sent", channel=channel.mention)))
        await channel.send(embeds=[default_embed] * embed_count)

    @context_cog("message", "Edit Embed", guild_ids=[883465097283002439])
    async def edit_embed(self, ctx: SlashedSubCommand, message: discord.Message):
        locale = Locale.from_guild_id(self.bot, ctx.guild_id)
        embeds = Embeds.from_locale(self.bot, locale)
        await ctx.defer(False)
        if message.author.id != self.bot.user.id:
            return await ctx.respond(embed=embeds.fail(locale.get_message("cog_embed_builder_edit_not_own")), hidden=True)    

        components = [
            [
                Button("emb:edit:p1:title", locale.get_message("cog_embed_builder_component_labels_p1_title")),
                Button("emb:edit:p1:description", locale.get_message("cog_embed_builder_component_labels_p1_description")),
                Button("emb:edit:p1:author", locale.get_message("cog_embed_builder_component_labels_p1_author"))
            ],
            [
                Button("emb:edit:p1:save", locale.get_message("cog_embed_builder_component_labels_p1_save"), color="green"),
                Button("emb:edit:p1:cancel", locale.get_message("cog_embed_builder_component_labels_p1_cancel"), color="red")
            ]
        ]

        msg = None
        embed_position = 0
        actions = 0


        if len(message.embeds) == 0:
            embed = discord.Embed()
        else:
            if len(message.embeds) > 1:
                # select embed
                msg = await ctx.respond(embed=embeds.info(locale.get_message("cog_embed_builder_select_embed")))
                await msg.edit(components=[SelectMenu("embed", options=[SelectOption(i, label=locale.get_message("cog_embed_builder_component_labels_select_embed", number=i+1)) for i, _ in enumerate(message.embeds)], placeholder="select an embed")])
                try:
                    sel = await msg.wait_for("select", self.bot, by=ctx.author, timeout=15)
                    await sel.respond()
                    embed = message.embeds[int(sel.selected_values[0].value)]
                except asyncio.TimeoutError:
                    return await msg.edit(embed=embeds.fail(locale.get_message("cog_embed_builder_timeout")))

            else:
                embed = message.embeds[0]
        if msg is not None:
            await msg.edit(locale.get_message("cog_embed_builder_you_can_edit_now"), components=components, embed=embed)
        else:
            msg: EphemeralMessage = await ctx.send(locale.get_message("cog_embed_builder_you_can_edit_now"), embed=embed, components=components, hidden=True)
            #await msg.edit(embed=embed)
        while True:
            set_components = (False, None)
            try:
                #actions += 1
                pressed_btn: PressedButton = await msg.wait_for("button", self.bot, by=ctx.author, timeout=60)
                #await w_f.delete()
                if pressed_btn.custom_id == "emb:edit:p1:title":
                    await pressed_btn.respond()
                    try:
                        actions +=1
                        
                        await msg.edit(content=locale.get_message("com_embed_builder_wait_for_message"), component_state=False)
                        await msg.disable_components()

                        w_f = await self.bot.wait_for("message", check=lambda m: m.author.id == ctx.author.id, timeout=30)
                        embed.title = w_f.content
                        set_components = (True, components)
                    except asyncio.TimeoutError:
                        actions =- 1
                        await msg.edit(embed=embeds.fail(locale.get_message("cog_embed_builder_timeout")), components=None)
                        break
                elif pressed_btn.custom_id == "emb:edit:p1:description":
                    await pressed_btn.respond()
                    try:
                        actions +=1
                        await msg.edit(content=locale.get_message("com_embed_builder_wait_for_message"))
                        w_f = await self.bot.wait_for("message", check=lambda m: m.author.id == ctx.author.id, timeout=30)
                        embed.description = w_f.content
                    except asyncio.TimeoutError:
                        actions =- 1
                        await msg.edit(embed=embeds.fail(locale.get_message("cog_embed_builder_timeout")))
                        break
                elif pressed_btn.custom_id == "emb:edit:p1:author":
                    await pressed_btn.respond()
                    author_components = [
                        [
                            Button("emb:edit:p2:name", locale.get_message("cog_embed_builder_component_labels_p2_author_name")),
                            Button("emb:edit:p2:url", locale.get_message("cog_embed_builder_component_labels_p2_author_url")),
                            Button("emb:edit:p2:icon", locale.get_message("cog_embed_builder_component_labels_p2_author_icon"))
                        ],
                        [
                            Button("emb:edit:p2:back", locale.get_message("cog_embed_builder_component_labels_p2_back"), color="green")
                        ]
                    ]
                    await msg.edit(components=author_components)
                elif pressed_btn.custom_id == "emb:edit:p1:save":
                    await pressed_btn.respond()
                    try:
                        all_embeds =  message.embeds
                        all_embeds[embed_position] = embed
                        await message.edit(embeds=all_embeds)
                    except:
                        pass
                    await ctx.channel.purge(limit=actions, check=lambda m: m.author.id == ctx.author.id, bulk=True)
                    await msg.edit(embed=embeds.success(locale.get_message("cog_embed_builder_saved")), content=None, components=None)
                    break
                
                elif pressed_btn.custom_id == "emb:edit:p1:cancel":
                    await pressed_btn.respond()
                    await msg.edit(embed = embeds.success(locale.get_message("cog_embed_builder_canceled")), components=None)
                    break                
                elif pressed_btn.custom_id == "emb:edit:p2:back":
                    await pressed_btn.respond()
                    await msg.edit(components=components)

                try:
                    if set_components[0]:
                        await msg.edit(embed=embed, content=locale.get_message("cog_embed_builder_you_can_edit_now"), components=set_components[1])
                except Exception as ex:
                    await ctx.channel.purge(limit=actions, check=lambda m: m.author.id == ctx.author.id, bulk=True)
                    await msg.edit(embed=embeds.fail(locale.get_message("cog_embed_builder_edit_failed")), components=None)
                    raise
            except asyncio.TimeoutError as ex:
                pass

    @commands.Cog.listener("on_ready")
    async def on_ready(self):
        await self.bot.ui.slash.sync_commands(True)

def setup(bot):
    bot.add_cog(EmbedBuilder(bot))