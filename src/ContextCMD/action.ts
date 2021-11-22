import { ContextCMD } from "../Interfaces";

export const command: ContextCMD = {
    name: "actions",
    addContextCommand: async (client, guild) => {
        await guild.commands.create({
            name: "actions",
            type: "MESSAGE"
        })
    },
    run: (client, interaction) => {
        interaction.reply({content: "Test"});
    },
    init: (client) => {
    }
}