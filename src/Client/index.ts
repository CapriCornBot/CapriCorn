import { Client, ClientOptions, Collection } from "discord.js";
import { ComponentHandler, ContextCMD, Event, SlashCMD } from "../Interfaces";
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
    public context_commands: Collection<string, ContextCMD> = new Collection();
    public component_handler: Collection<string, ComponentHandler> = new Collection();

    public async init() {
        await this.login(config.token);
        await this.user.setActivity({type: "PLAYING", name: "mit Adminrechten"});
        const eventPath = path.join(__dirname, "..", "Events");
        readdirSync(eventPath).forEach(async file => {

            // event_path: "../Events/
            // file: "ready.ts"

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
        
        const contextCmdPath = path.join(__dirname, "..", "ContextCMD");
        readdirSync(contextCmdPath).forEach(async file => {
            const { command } = await import(`${contextCmdPath}/${file}`)
            this.context_commands.set(command.name, command);
            //console.log(command);
            command.init(this);
        });
        
        const componentPath = path.join(__dirname, "..", "ComponentHandler");
        readdirSync(componentPath).forEach(async file => {
            const { handler } = await import(`${componentPath}/${file}`)
            handler.init(this);
            this.component_handler.set(handler.prefix, handler);
        });
    }

}

export default ExtendedClient;