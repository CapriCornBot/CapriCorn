import { SlashCommandBuilder } from "@discordjs/builders";
import { SlashCMD } from "../Interfaces";
import Locale from "../Utils/Locale";

export const command: SlashCMD = {
    name: 'test',
    slashCommand: (client, guildId) => {
        const builder = new SlashCommandBuilder();
        builder.setName('test');
        builder.setDescription('test');
        return builder
    },
    init: (client) => {
        
    },
    run: async (client, interaction) => {
        let embed = await Locale.getString("de", "embed_creator.default_embed");
        interaction.reply({embeds: [embed]});
    }
}