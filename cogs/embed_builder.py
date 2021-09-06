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
    name = "Embedbuilder"
    description = "Create Embeds etc."
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
                Button("emb:edit:p1:author", locale.get_message("cog_embed_builder_component_labels_p1_author")),
                Button("emb:edit:p1:color", locale.get_message("cog_embed_builder_component_labels_p1_color")),
                Button("emb:edit:p1:image", locale.get_message("cog_embed_builder_component_labels_p1_image")),
            ],[
                Button("emb:edit:p1:thumbnail", locale.get_message("cog_embed_builder_component_labels_p1_thumbnail")),
                Button("emb:edit:p1:fields", locale.get_message("cog_embed_builder_component_labels_p1_fields"))
            ],
            [
                Button("emb:edit:p1:save", locale.get_message("cog_embed_builder_component_labels_p1_save"), color="green"),
                Button("emb:edit:p1:cancel", locale.get_message("cog_embed_builder_component_labels_p1_cancel"), color="red")
            ]
        ]
        author_components = [
            [
                Button("emb:edit:p2:name", locale.get_message("cog_embed_builder_component_labels_p2_author_name")),
                Button("emb:edit:p2:url", locale.get_message("cog_embed_builder_component_labels_p2_author_url")),
                Button("emb:edit:p2:icon", locale.get_message("cog_embed_builder_component_labels_p2_author_icon"))
            ],
            [
                Button("emb:edit:p2:back", locale.get_message("cog_embed_builder_component_labels_p2_back"), color="gray")
            ]
        ]
        def field_components(used_fields = 0, max_fields: int = 25):
            field_components_1 = [
                [
                    Button("emb:edit:p3:add", locale.get_message("cog_embed_builder_component_labels_p3_add", used=used_fields, max=max_fields), color="green"),
                    Button("emb:edit:p3:remove", locale.get_message("cog_embed_builder_component_labels_p3_remove"), color="red"),
                    Button("emb:edit:p3:edit", locale.get_message("cog_embed_builder_component_labels_p3_edit"), color="green")
                ],
                [
                    Button("emb:edit:p3:back", locale.get_message("cog_embed_builder_component_labels_p3_back"), color="gray"),
                ]
            ]
            if used_fields == max_fields:
                field_components_1[0][0].disabled = True
            if used_fields == 0:
                field_components_1[0][1].disabled = True
                field_components_1[0][2].disabled = True
            return field_components_1
        
        def field_edit_components(index, inline = True):
            cmpnts = [
                [
                    Button(f"emb:edit:p4:name:{index}", locale.get_message("cog_embed_builder_component_labels_p4_title")),
                    Button(f"emb:edit:p4:value:{index}", locale.get_message("cog_embed_builder_component_labels_p4_value")),
                    Button(f"emb:edit:p4:inline:{index}", locale.get_message("cog_embed_builder_component_labels_p4_inline"), color="green" if inline else "red"),
                ],
                [
                    Button("emb:edit:p4:back", locale.get_message("cog_embed_builder_component_labels_p4_back"), color="gray"),
                    Button("emb:edit:main", "\u200b", emoji="🏠", color="gray"),
                ]
            ]
            return cmpnts

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
                    embed = message.embeds[int(sel.selected_values[0].value)].copy()
                    embed_position = int(sel.selected_values[0].value)
                except asyncio.TimeoutError:
                    return await msg.edit(embed=embeds.fail(locale.get_message("cog_embed_builder_timeout")))

            else:
                embed = message.embeds[0].copy()
        if msg is not None:
            await msg.edit(locale.get_message("cog_embed_builder_you_can_edit_now"), components=components, embed=embed)
        else:
            msg: EphemeralMessage = await ctx.send(locale.get_message("cog_embed_builder_you_can_edit_now"), embed=embed, components=components, hidden=True)
            #await msg.edit(embed=embed)
        while True:
            set_components = (False, None)
            edit_after = True
            try:
                #actions += 1
                pressed_btn: PressedButton = await msg.wait_for("button", self.bot, by=ctx.author, timeout=60)
                #await w_f.delete()
                if pressed_btn.custom_id == "emb:edit:p1:title":
                    await pressed_btn.respond()
                    try:
                        actions +=1
                        
                        await msg.edit(content=locale.get_message("cog_embed_builder_wait_for_message"), component_state=False)
                        await msg.disable_components()

                        w_f = await self.bot.wait_for("message", check=lambda m: m.author.id == ctx.author.id, timeout=30)
                        if w_f.content == "none":
                            embed.title = ""
                        else:
                            embed.title = w_f.content
                        set_components = (True, components)
                    except asyncio.TimeoutError:
                        actions =- 1
                        await msg.edit(embeds=[embed, embeds.fail(locale.get_message("cog_embed_builder_timeout"))], components=components, content=locale.get_message("cog_embed_builder_you_can_edit_now"))
                        edit_after = False
                elif pressed_btn.custom_id == "emb:edit:p1:description":
                    await pressed_btn.respond()
                    try:
                        actions +=1
                        await msg.edit(content=locale.get_message("cog_embed_builder_wait_for_message"))
                        await msg.disable_components()
                        w_f = await self.bot.wait_for("message", check=lambda m: m.author.id == ctx.author.id, timeout=30)
                        if w_f.content == "none":
                            embed.description = ""
                        else:
                            embed.description = w_f.content
                        set_components = (True, components)
                    except asyncio.TimeoutError:
                        actions =- 1
                        await msg.edit(embeds=[embed, embeds.fail(locale.get_message("cog_embed_builder_timeout"))], components=components, content=locale.get_message("cog_embed_builder_you_can_edit_now"))
                        edit_after = False
                elif pressed_btn.custom_id == "emb:edit:p1:author":
                    await pressed_btn.respond()
                    await msg.edit(components=author_components)
                elif pressed_btn.custom_id == "emb:edit:p1:fields":
                    await pressed_btn.respond()
                    await msg.edit(components=field_components(len(embed.fields)))
                elif pressed_btn.custom_id == "emb:edit:p1:color":
                    await pressed_btn.respond()
                    try:
                        actions +=1
                        await msg.edit(content=locale.get_message("cog_embed_builder_wait_for_message"))
                        await msg.disable_components()
                        w_f: discord.Message = await self.bot.wait_for("message", check=lambda m: m.author.id == ctx.author.id, timeout=30)
                        try:
                            hex_int = int(w_f.content, 16)
                        except:
                            await msg.edit(embed=embeds.fail(locale.get_message("cog_embed_builder_edit_invalid_hex")))
                            break
                        embed.colour = hex_int
                        set_components = (True, components)
                    except asyncio.TimeoutError:
                        actions =- 1
                        await msg.edit(embeds=[embed, embeds.fail(locale.get_message("cog_embed_builder_timeout"))], components=components, content=locale.get_message("cog_embed_builder_you_can_edit_now"))
                        edit_after = False
                elif pressed_btn.custom_id == "emb:edit:p1:image":
                    await pressed_btn.respond()
                    try:
                        actions +=1
                        await msg.edit(content=locale.get_message("cog_embed_builder_wait_for_message"))
                        await msg.disable_components()
                        w_f: discord.Message = await self.bot.wait_for("message", check=lambda m: m.author.id == ctx.author.id, timeout=30)
                        if w_f.content == "none":
                            embed.set_image(url="")
                        else:
                            if not w_f.content.startswith("http://") and not w_f.content.startswith("https://"):
                                await msg.edit(embeds=[embed, embeds.fail(locale.get_message("cog_embed_builder_edit_invalid_url"))], components=components, content=locale.get_message("cog_embed_builder_you_can_edit_now"))
                                edit_after = False
                            else:
                                embed.set_image(url=w_f.content)
                        set_components = (True, components)
                    except asyncio.TimeoutError:
                        actions =- 1
                        await msg.edit(embeds=[embed, embeds.fail(locale.get_message("cog_embed_builder_timeout"))], components=components, content=locale.get_message("cog_embed_builder_you_can_edit_now"))
                        edit_after = False
                elif pressed_btn.custom_id == "emb:edit:p1:thumbnail":
                    await pressed_btn.respond()
                    try:
                        actions +=1
                        await msg.edit(content=locale.get_message("cog_embed_builder_wait_for_message"))
                        await msg.disable_components()
                        w_f: discord.Message = await self.bot.wait_for("message", check=lambda m: m.author.id == ctx.author.id, timeout=30)
                        if w_f.content == "none":
                            embed.set_thumbnail(url="")
                        else:
                            if not w_f.content.startswith("http://") and not w_f.content.startswith("https://"):
                                await msg.edit(embeds=[embed, embeds.fail(locale.get_message("cog_embed_builder_edit_invalid_url"))], components=components, content=locale.get_message("cog_embed_builder_you_can_edit_now"))
                                edit_after = False
                            else:
                                embed.set_thumbnail(url=w_f.content)
                        set_components = (True, components)
                    except asyncio.TimeoutError:
                        actions =- 1
                        await msg.edit(embeds=[embed, embeds.fail(locale.get_message("cog_embed_builder_timeout"))], components=components, content=locale.get_message("cog_embed_builder_you_can_edit_now"))
                        edit_after = False
                elif pressed_btn.custom_id == "emb:edit:p1:save":
                    await pressed_btn.respond()
                    try:
                        all_embeds = message.embeds
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
                elif pressed_btn.custom_id == "emb:edit:p2:name":
                    await pressed_btn.respond()
                    try:
                        actions +=1
                        await msg.edit(content=locale.get_message("cog_embed_builder_wait_for_message"))
                        await msg.disable_components()
                        w_f = await self.bot.wait_for("message", check=lambda m: m.author.id == ctx.author.id, timeout=30)
                        url = embed.author.url
                        icon = embed.author.icon_url
                        name = w_f.content
                        if name == "none":
                            name = ""
                            icon = ""
                            url = ""
                        embed.set_author(name=name, url=url, icon_url=icon)
                        set_components = (True, author_components)
                    except asyncio.TimeoutError:
                        actions =- 1
                        await msg.edit(embeds=[embed, embeds.fail(locale.get_message("cog_embed_builder_timeout"))], components=author_components, content=locale.get_message("cog_embed_builder_you_can_edit_now"))
                        edit_after = False
                elif pressed_btn.custom_id == "emb:edit:p2:url":
                    await pressed_btn.respond()
                    try:
                        actions +=1
                        await msg.edit(content=locale.get_message("cog_embed_builder_wait_for_message"))
                        await msg.disable_components()
                        w_f = await self.bot.wait_for("message", check=lambda m: m.author.id == ctx.author.id, timeout=30)
                        url = w_f.content
                        if url == "none":
                            url = ""
                            embed.set_author(name=embed.author.name, url=url, icon_url=embed.author.icon_url)
                            set_components = (True, author_components)
                        elif url.startswith(("http://", "https://")):
                            embed.set_author(name=embed.author.name, url=url, icon_url=embed.author.icon_url)
                            set_components = (True, author_components)
                        else:
                            set_components = (True, author_components)
                    except asyncio.TimeoutError:
                        actions =- 1
                        await msg.edit(embeds=[embed, embeds.fail(locale.get_message("cog_embed_builder_timeout"))], components=author_components, content=locale.get_message("cog_embed_builder_you_can_edit_now"))
                        edit_after = False
                elif pressed_btn.custom_id == "emb:edit:p2:icon":
                    await pressed_btn.respond()
                    try:
                        actions +=1
                        await msg.edit(content=locale.get_message("cog_embed_builder_wait_for_message"))
                        await msg.disable_components()
                        w_f = await self.bot.wait_for("message", check=lambda m: m.author.id == ctx.author.id, timeout=30)
                        icon = w_f.content
                        if icon == "none":
                            icon = ""
                            embed.set_author(name=embed.author.name, url=embed.author.url, icon_url=icon)
                            set_components = (True, author_components)
                        elif icon.startswith(("http://", "https://")):
                            embed.set_author(name=embed.author.name, url=url, icon_url=icon)
                            set_components = (True, author_components)
                        else:
                            set_components = (True, author_components)
                    except asyncio.TimeoutError:
                        actions =- 1
                        await msg.edit(embeds=[embed, embeds.fail(locale.get_message("cog_embed_builder_timeout"))], components=author_components, content=locale.get_message("cog_embed_builder_you_can_edit_now"))
                        edit_after = False
                elif pressed_btn.custom_id == "emb:edit:p2:back":
                    await pressed_btn.respond()
                    set_components = (True, components)
                elif pressed_btn.custom_id == "emb:edit:p3:back":
                    await pressed_btn.respond()
                    set_components = (True, components)
                elif pressed_btn.custom_id == "emb:edit:p3:add":
                    await pressed_btn.respond()
                    embed.add_field(name=locale.get_message("cog_embed_builder_default_field_name"), value=locale.get_message("cog_embed_builder_default_field_value"), inline=False)
                    set_components = (True, field_components(len(embed.fields)))
                elif pressed_btn.custom_id == "emb:edit:p3:remove":
                    await pressed_btn.respond()
                    temp_embeds = [embed, embeds.info(locale.get_message("cog_embed_builder_info_select_field"))]
                    await msg.edit(embeds=temp_embeds, components=[SelectMenu("field", options=[SelectOption(i, label=locale.get_message("cog_embed_builder_component_labels_p3_field_select", name=_.name, number=i+1)) for i, _ in enumerate(embed.fields)])])
                    try:
                        selected = await msg.wait_for("select", self.bot, by=ctx.author, timeout=15)
                        await selected.respond()
                        sel = int(selected.selected_values[0].value)
                        embed.remove_field(sel)
                        set_components = (True, field_components(len(embed.fields)))
                    except asyncio.TimeoutError:
                        set_components = (True, field_components(len(embed.fields)))
                elif pressed_btn.custom_id == "emb:edit:p3:edit":
                    await pressed_btn.respond()
                    temp_embeds = [embed, embeds.info(locale.get_message("cog_embed_builder_info_select_field"))]
                    await msg.edit(embeds=temp_embeds, components=[SelectMenu("field", options=[SelectOption(i, label=locale.get_message("cog_embed_builder_component_labels_p3_field_select", name=_.name, number=i+1)) for i, _ in enumerate(embed.fields)])])
                    try:
                        selected = await msg.wait_for("select", self.bot, by=ctx.author, timeout=15)
                        await selected.respond()
                        sel = int(selected.selected_values[0].value)
                        set_components = (True, field_edit_components(sel, embed.fields[sel].inline))
                    except asyncio.TimeoutError:
                        set_components = (True, field_components(len(embed.fields)))
                elif pressed_btn.custom_id.startswith("emb:edit:p4:name:"):
                    await pressed_btn.respond()
                    field_index = int(pressed_btn.custom_id.split(":")[4])
                    try:
                        actions +=1
                        await msg.edit(content=locale.get_message("cog_embed_builder_wait_for_message"))
                        await msg.disable_components()
                        w_f = await self.bot.wait_for("message", check=lambda m: m.author.id == ctx.author.id, timeout=30)
                        embed.set_field_at(field_index, name=w_f.content, value=embed.fields[field_index].value, inline=embed.fields[field_index].inline)
                        set_components = (True, field_edit_components(sel, embed.fields[sel].inline))
                    except asyncio.TimeoutError:
                        actions =- 1
                        set_components = (True, field_edit_components(sel, embed.fields[sel].inline))
                elif pressed_btn.custom_id.startswith("emb:edit:p4:value:"):
                    await pressed_btn.respond()
                    field_index = int(pressed_btn.custom_id.split(":")[4])
                    try:
                        actions +=1
                        await msg.edit(content=locale.get_message("cog_embed_builder_wait_for_message"))
                        await msg.disable_components()
                        w_f = await self.bot.wait_for("message", check=lambda m: m.author.id == ctx.author.id, timeout=30)
                        embed.set_field_at(field_index, name=embed.fields[field_index].name, value=w_f.content, inline=embed.fields[field_index].inline)
                        set_components = (True, field_edit_components(sel, embed.fields[sel].inline))
                    except asyncio.TimeoutError:
                        actions =- 1
                        set_components = (True, field_edit_components(sel, embed.fields[sel].inline))
                elif pressed_btn.custom_id.startswith("emb:edit:p4:inline:"):
                    await pressed_btn.respond()
                    field_index = int(pressed_btn.custom_id.split(":")[4])
                    embed.set_field_at(field_index, name=embed.fields[field_index].name, value=embed.fields[field_index].value, inline=not embed.fields[field_index].inline)
                    set_components = (True, field_edit_components(sel, embed.fields[sel].inline))
                elif pressed_btn.custom_id == "emb:edit:p4:back":
                    await pressed_btn.respond()
                    set_components = (True, field_components(len(embed.fields)))
                elif pressed_btn.custom_id == "emb:edit:main":
                    await pressed_btn.respond()
                    set_components = (True, components)
                try:
                    if edit_after:
                        if set_components[0]:
                            await msg.edit(embed=embed, content=locale.get_message("cog_embed_builder_you_can_edit_now"), components=set_components[1])
                        else:
                            await msg.edit(embed=embed, content=locale.get_message("cog_embed_builder_you_can_edit_now"))
                except Exception as ex:
                    await ctx.channel.purge(limit=actions, check=lambda m: m.author.id == ctx.author.id, bulk=True)
                    await msg.edit(embed=embeds.fail(locale.get_message("cog_embed_builder_edit_failed")), components=None)
                    raise
            except asyncio.TimeoutError as ex:
                await msg.edit(embeds=[embeds.fail(locale.get_message("cog_embed_builder_timeout"))], components=None, content=None)

    @commands.Cog.listener("on_ready")
    async def on_ready(self):
        await self.bot.ui.slash.sync_commands(True)

def setup(bot):
    bot.add_cog(EmbedBuilder(bot))