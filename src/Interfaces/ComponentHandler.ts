import { MessageComponentInteraction } from "discord.js";
import Client from "../Client";

interface Run {
    (client: Client, interaction: MessageComponentInteraction);
}

interface Init {
    (client: Client): void;
}

export interface ComponentHandler {
    prefix: string;
    run: Run;
    init: Init;
}