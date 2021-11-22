import { Event } from "../Interfaces";
import Client from "../Client";
import { AutocompleteInteraction, ContextMenuInteraction, Interaction, MessageActionRow, MessageButton } from "discord.js";
import { Embed } from "@discordjs/builders";
export const event: Event = {
    name: 'interactionCreate',
    run: async (client: Client, interaction: Interaction) => {
        console.log(`Interaction created: ${interaction.id}`);
        if(interaction.isCommand()) {
            // console.log(`Command: ${interaction.commandName}`);
            // if(interaction.commandName === 'test') {
            //     const data = new MessageActionRow().addComponents(new MessageButton().setLabel('Test').setCustomId('test').setStyle('PRIMARY'));
            //     await interaction.reply({content: "Test", components: [data]});
            // }
            let d = client.commands.find(c => c.name === interaction.commandName);
            if(d) {
                d.run(client, interaction);
            }else {
                console.log(`Command not found: ${interaction.commandName}`);
                let content_emb = new Embed()
                content_emb.setTitle(`Command not found: ${interaction.commandName}`)
                content_emb.setDescription(`Please contact the developer of this bot.`)
                content_emb.setColor(15158332)
                interaction.reply({ephemeral: true, embeds: [content_emb]});
            }
        }else if(interaction.isContextMenu()) {
            console.log(`Context Menu: ${interaction.commandName}`);
            let d = client.context_commands.find(c => c.name === interaction.commandName);
            if(d) {
                d.run(client, interaction);
            }else {
                console.log(`Context Menu not found: ${interaction.commandName}`);
                let content_emb = new Embed()
                content_emb.setTitle(`Context Menu not found: ${interaction.commandName}`)
                content_emb.setDescription(`Please contact the developer of this bot.`)
                content_emb.setColor(15158332)
                interaction.reply({ephemeral: true, embeds: [content_emb]});
            }
        }else if(interaction.isButton()) {
            console.log(`Button: ${interaction}`);
            //console.log(interaction.component)
            let button: MessageButton = interaction.component as MessageButton;
            interaction.reply({content: "Button mit Label: `" + button.label + "` gedrückt"});
        }else if(interaction.isAutocomplete()) {
            console.log(`Autocomplete: ${interaction.commandName}`);
            let d = client.commands.find(c => c.name === interaction.commandName)
            if(d) {
                try {
                    d.autoCompleteHandler(client, interaction as AutocompleteInteraction);
                }catch(e) {
                    //console.log(e);
                }
            }
        }
    }
}