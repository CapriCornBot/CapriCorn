import { BaseGuildTextChannel, CommandInteraction, Interaction, TextChannel } from "discord.js";
import { SlashCMD } from "../Interfaces";
import Client from "../Client";
import { Embed, SlashCommandBuilder} from "@discordjs/builders";

import { ChannelType } from "discord-api-types/v9";
import Locale from "../Utils/Locale";

export const command: SlashCMD = {
    name: "create_embed",
    addSlashCommand: (client, guild) => {
        let d: SlashCommandBuilder = new SlashCommandBuilder();
        d.setName("create_embed");
        d.setDescription("Creates an embed");
        // add 10 choices
        d.addChannelOption((option) => option.setName("channel").setRequired(true).setDescription("Channel").addChannelType(ChannelType.GuildText));
        d.addIntegerOption((option) => option.setName("amount").setRequired(true).setDescription("Anzahl"). addChoice("1", 1).addChoice("2", 2).addChoice("3", 3).addChoice("4", 4).addChoice("5", 5).addChoice("6", 6).addChoice("7", 7).addChoice("8", 8).addChoice("9", 9).addChoice("10", 10));
        guild.commands.create(d.toJSON())
    },
    init: (client: Client) => {
        console.log("running init from slash command")
    },
    async run(client, interaction: CommandInteraction) {
        await interaction.deferReply({ephemeral: true})
        let channel = interaction.options.getChannel("channel", true) as TextChannel;
        let amount = interaction.options.getInteger("amount", true);
        if (amount === undefined) {
            amount = 1;
        }
        //biger than 10
        if (amount > 10) {
            amount = 10;
        }
        let locale = await Locale.getLocale(interaction.guildId);
        let emb = await Locale.getString(locale, "embed_creator.default_embed");
        let embeds = [];
        for (let i = 0; i < amount; i++) {
            embeds.push(emb);
        }
        await channel.send({embeds: embeds})
        interaction.editReply(await Locale.getString(locale, "embed_creator.embed_created"));
    }

}