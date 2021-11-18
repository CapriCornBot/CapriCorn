import Client from "./Client";
import { Intents } from "discord.js";
new Client({intents: [Intents.FLAGS.GUILDS]}).init();