import { Event } from '../Interfaces';
import Client from '../Client';

export const event: Event = {
    name: 'ready',
    run: (client: Client, ...args) => {
        console.log(`Logged in as ${client.user.tag}!`);
    }
}

