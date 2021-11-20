import { Client, ClientOptions, Collection, GuildEmoji } from "discord.js";
import { Event, SlashCMD } from "../Interfaces";
import config from "../config.json";
import path from "path";
import {readdirSync} from "fs";
import { command } from "../Commands/create_embed";

class ExtendedClient extends Client {

    constructor(options: ClientOptions = null) {
        super(options);
    }

    public events: Collection<string, Event> = new Collection();
    public commands: Collection<string, SlashCMD> = new Collection();

    public async init() {
        this.login(config.token);

        const eventPath = path.join(__dirname, "..", "Events");
        readdirSync(eventPath).forEach(async file => {
            const { event } = await import(`${eventPath}/${file}`)
            this.events.set(event.name, event);
            //console.log(event);
            this.on(event.name, event.run.bind(null, this));
        });

        const commandPath = path.join(__dirname, "..", "Commands");
        readdirSync(commandPath).forEach(async file => {
            const { command } = await import(`${commandPath}/${file}`)
            this.commands.set(command.name, command);
            //console.log(command);
            command.init(this);
        });
    }

}

export default ExtendedClient;