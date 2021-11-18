import { Event } from "../Interfaces";
import Client from "../Client";
import { Interaction } from "discord.js";
export const event: Event = {
    name: 'interactionCreate',
    run: (client: Client, interaction: Interaction) => {
        console.log(`Interaction created: ${interaction.id}`);
        if(interaction.isCommand()) {
            console.log(`Command: ${interaction.commandName}`);
        }
    }
}