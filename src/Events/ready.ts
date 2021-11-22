import { Event } from '../Interfaces';
import Client from '../Client';


export const event: Event = {
    name: 'ready',
    run: async (client: Client, ...args) => {
        console.log(`Logged in as ${client.user.tag}!`);
        console.log(`Loading SlashCommands`);
        for (const guild of client.guilds.cache.values()) {
            //console.log(guild);
            //const cmds = await guild.commands.fetch();
            client.commands.forEach((value, key) => {
                value.addSlashCommand(client, guild);
            });

            client.context_commands.forEach((value, key) => {
                value.addContextCommand(client, guild);
            });
        }
    }
}

