import Database from './Database';
import { readdirSync } from 'fs';
import path from 'path';
class Locale {

    private json = new Map();
    private static _instance: Locale;
    private json_loaded = false;

    constructor() {
    }

    async loadJson() {
        await readdirSync(path.join(__dirname, "..", "Locale")).forEach(async file => {
            if(file.endsWith(".json")) {
                let json = await import(`../Locale/${file}`);
                //console.log("JSON File");
                //console.log(json);
                this.json.set(file.replace(".json", ""), json);
            }
        });
    }

    public static getInstance() {
        if (!Locale._instance) {
            Locale._instance = new Locale();
        }
        return Locale._instance;
    }


    async getString(locale, key) {
        if(!this.json_loaded) {
            await this.loadJson();
            this.json_loaded = true;
        }
        let json = this.json.get(locale);
        //console.log(json);
        const splited_key = key.split(".");
        //console.log(splited_key);
        if(splited_key.length > 1) {
            for(let i = 0; i < splited_key.length; i++) {
                json = json[splited_key[i]];
            }
        }
        return json;
    }

    async getFullLocale(locale) {
        if(!this.json_loaded) {
            await this.loadJson();
            this.json_loaded = true;
        }
        let json = this.json.get(locale);
        //console.log(this.json);
        //console.log("Full Locale")
        //console.log(json);
        return json;
    }

    async getLocale(guildId) {
        const db = await Database.db;
        const entry = await db.collection("settings").findOne({guildId: guildId + ""});
        if(entry) {
            return entry.locale;
        }
        return "de";
    }

}

export default Locale.getInstance();