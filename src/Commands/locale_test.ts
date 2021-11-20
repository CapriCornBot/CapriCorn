import { Embed, SlashCommandBuilder } from "@discordjs/builders";
import { SlashCMD } from "../Interfaces";
import Locale from "../Utils/Locale";

export const command: SlashCMD = {
    name: 'test_locale',
    addSlashCommand: (client, guild) => {
        guild.commands.create({
            name: 'test_locale',
            type: "CHAT_INPUT",
            description: "Test locale",
            options: [
                {
                    name: "key",
                    type: "STRING",
                    description: "Key to test",
                    required: true,
                    autocomplete: true
                }
            ]
        })
    },
    init: (client) => {
        
    },
    run: async (client, interaction) => {
        new SlashCommandBuilder().toJSON
        let embed = await Locale.getString("de", "embed_creator.default_embed");
        let locale = await Locale.getLocale(interaction.guildId)
        let emb = new Embed();
        emb.setTitle("Sprachen Check!");
        emb.addField({name: "Key", value: interaction.options.getString("key")});
        let string = await Locale.getString(locale,  interaction.options.getString("key"));
        if(typeof string === "object") {
            try {
                string = JSON.stringify(string, null, 4);
            }catch(e) {
                string = "Error while parsing JSON";
            }
        }
        emb.addField({name: "Value", value: "```json\n" + string + "```"});
        interaction.reply({embeds: [emb.toJSON()]});
    },
    autoCompleteHandler: async (client, interaction) => {
        console.log(interaction.options.getString("key"))
        let json = await Locale.getFullLocale(await Locale.getLocale(interaction.guildId));
        let keys = Object.keys(json);
        // get all keys         
        function getDeepKeys(obj) {
            var keys = [];
            for(var key in obj) {
                keys.push(key);
                if(typeof obj[key] === "object") {
                    var subkeys = getDeepKeys(obj[key]);
                    keys = keys.concat(subkeys.map(function(subkey) {
                        return key + "." + subkey;
                    }));
                }
            }
            return keys;
        }
        let all_keys = getDeepKeys(json);
        //get all keys that match
        let matches = all_keys.filter(key => key.startsWith(interaction.options.getString("key")));
        // return the first 20 matches
        //convert matches to options
        let options = matches.map(key => {
            return {
                name: key,
                value: key
            }
        }).slice(0, 20);
        interaction.respond(options)
    }
}