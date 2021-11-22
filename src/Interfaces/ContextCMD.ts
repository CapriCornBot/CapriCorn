import { AutocompleteInteraction, ContextMenuInteraction, Guild } from "discord.js";
import Client from "../Client";

interface Run {
    (client: Client, interaction: ContextMenuInteraction);
}

interface Init {
    (client: Client): void;
}

interface ContextCommand {
    (client: Client, guild: Guild): void;
}

export interface ContextCMD {
    name: string;
    addContextCommand: ContextCommand;
    run: Run;
    init: Init;
}