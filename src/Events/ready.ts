import { Event } from '../Interfaces';
import Client from '../Client';
import { SlashCommandBuilder } from '@discordjs/builders';
import { Options } from 'discord.js';


export const event: Event = {
    name: 'ready',
    run: async (client: Client, ...args) => {
        console.log(`Logged in as ${client.user.tag}!`);
        console.log(`Loading SlashCommands`)
        for (const guild of client.guilds.cache.values()) {
            console.log(guild);
            const cmds = await guild.commands.fetch();
            client.commands.forEach((value, key) => {
                guild.commands.create(value.slashCommand(client, guild.id).toJSON());
            });
        }
    }
}

