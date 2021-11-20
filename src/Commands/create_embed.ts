import { BaseGuildTextChannel, CommandInteraction, Interaction, TextChannel } from "discord.js";
import { SlashCMD } from "../Interfaces";
import Client from "../Client";
import { Embed, SlashCommandBuilder} from "@discordjs/builders";

import { ChannelType } from "discord-api-types/v9";

export const command: SlashCMD = {
    name: "create_embed",
    slashCommand: (client, guildId) => {
        let d: SlashCommandBuilder = new SlashCommandBuilder();
        d.setName("create_embed");
        d.setDescription("Creates an embed");
        // add 10 choices
        d.addChannelOption((option) => option.setName("channel").setRequired(true).setDescription("Channel").addChannelType(ChannelType.GuildText));
        d.addIntegerOption((option) => option.setName("amount").setDescription("Anzahl"). addChoice("1", 1).addChoice("2", 2).addChoice("3", 3).addChoice("4", 4).addChoice("5", 5).addChoice("6", 6).addChoice("7", 7).addChoice("8", 8).addChoice("9", 9).addChoice("10", 10));
        return d;
    },
    init: (client: Client) => {
        console.log("running init from slash command")
    },
    run(client, interaction: CommandInteraction) {
        let channel = interaction.options.getChannel("channel", true) as TextChannel;
        let amount = interaction.options.getInteger("amount", false);
        if (amount === undefined) {
            amount = 1;
        }
        let embed = new Embed()
        embed.setTitle("Test");
        
            

    }

}