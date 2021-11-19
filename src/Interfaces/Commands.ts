import { CommandInteraction } from "discord.js";
import Client from "../Client";
import { } from "discord.js"
import { SlashCommandBuilder } from "@discordjs/builders";

interface Run {
    (client: Client, interaction: CommandInteraction);
}

interface Init {
    (client: Client): void;
}

interface SlashCommand {
    (client: Client, guildId: string): SlashCommandBuilder;
}

export interface SlashCMD {
    name: string;
    slashCommand: SlashCommand;
    run: Run;
    init: Init;
}