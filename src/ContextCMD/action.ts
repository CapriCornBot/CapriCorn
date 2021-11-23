import { Embed } from "@discordjs/builders";
import { MessageActionRow, MessageButton, MessageSelectMenu } from "discord.js";
import { ContextCMD } from "../Interfaces";
import Locale from "../Utils/Locale";

export const command: ContextCMD = {
    name: "actions",
    addContextCommand: async (client, guild) => {
        await guild.commands.create({
            name: "actions",
            type: "MESSAGE"
        })
    },
    run: async (client, interaction) => {

        let locale = await Locale.getLocale(interaction.guild.id);
        const embed: any = await Locale.getString(locale, "context.actions.selector.embed");
        let row = new MessageActionRow().addComponents(
            new MessageSelectMenu().setCustomId("ac:select")
            .setOptions([
                {label: "Embed Editor", value: "embed_editor", emoji: "📝"},
            ])
        )
        await interaction.reply({embeds: [embed], components: [row]});
    },
    init: (client) => {
    }
}