import { Event } from "../Interfaces";
import Client from "../Client";
import { Interaction, MessageActionRow, MessageButton } from "discord.js";
export const event: Event = {
    name: 'interactionCreate',
    run: async (client: Client, interaction: Interaction) => {
        console.log(`Interaction created: ${interaction.id}`);
        if(interaction.isCommand()) {
            console.log(`Command: ${interaction.commandName}`);
            if(interaction.commandName === 'test') {
                const data = new MessageActionRow().addComponents(new MessageButton().setLabel('Test').setCustomId('test').setStyle('PRIMARY'));
                await interaction.reply({content: "Test", components: [data]});
            }
        }else if(interaction.isContextMenu()) {
            console.log(`Context Menu: ${interaction.commandName}`);
        }else if(interaction.isButton()) {
            console.log(`Button: ${interaction}`);
            console.log(interaction.component)
            let button: MessageButton = interaction.component as MessageButton;
            interaction.reply({content: "Button mit Label: `" + button.label + "` gedrückt"});
        }
    }
}