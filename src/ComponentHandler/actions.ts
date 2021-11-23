import { ComponentHandler, SlashCMD } from "../Interfaces";
import Client from "../Client";
import { MessageComponentInteraction } from "discord.js";


export const handler: ComponentHandler = {
    prefix: "ac",
    run: (client: Client, interaction: MessageComponentInteraction) => {
        interaction.reply("Hello World!");
    },
    init: (client) => {

    } 
}