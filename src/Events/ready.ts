import { Event } from '../Interfaces';
import Client from '../Client';
import { SlashCommandBuilder } from '@discordjs/builders';
import { Options } from 'discord.js';


export const event: Event = {
    name: 'ready',
    run: (client: Client, ...args) => {
        console.log(`Logged in as ${client.user.tag}!`);
        console.log(`Loading SlashCommands`)
        for (const guild of client.guilds.cache.values()) {
            const slash_command = new SlashCommandBuilder()
            .setName("create_embed")
            .setDescription("Creates an embed")
            .addIntegerOption((option) => option.setName("ammount").setDescription("Anzahl der Embeds").setRequired(true).addChoice("1", 1).addChoice("2", 2).addChoice("3", 3).addChoice("4", 4).addChoice("5", 5).addChoice("6", 6).addChoice("7", 7).addChoice("8", 8).addChoice("9", 9).addChoice("10", 10));
            guild.commands.create(slash_command.toJSON());
        }
    }
}

