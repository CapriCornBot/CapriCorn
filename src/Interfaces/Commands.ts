import { AutocompleteInteraction, CommandInteraction, Guild } from "discord.js";
import Client from "../Client";

import { SlashCommandBuilder } from "@discordjs/builders";

interface Run {
    (client: Client, interaction: CommandInteraction);
}

interface Init {
    (client: Client): void;
}

interface SlashCommand {
    (client: Client, guild: Guild): void;
}

interface AutoCompleteHandler {
    (client: Client, interaction: AutocompleteInteraction): void;
}

export interface SlashCMD {
    name: string;
    addSlashCommand: SlashCommand;
    run: Run;
    init: Init;
    autoCompleteHandler?: AutoCompleteHandler;
}