import { Client, ClientOptions, Collection } from "discord.js";
import { Event } from "../Interfaces";
import config from "../config.json";
import path from "path";
import {readdirSync} from "fs";

class ExtendedClient extends Client {

    constructor(options: ClientOptions = null) {
        super(options);
    }

    public events: Collection<string, Event> = new Collection();

    public async init() {
        this.login(config.token);

        const eventPath = path.join(__dirname, "..", "Events");
        readdirSync(eventPath).forEach(async file => {
            const { event } = await import(`${eventPath}/${file}`)
            this.events.set(event.name, event);
            console.log(event);
            this.on(event.name, event.run.bind(null, this));
        });
    }

}

export default ExtendedClient;