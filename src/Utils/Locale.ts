import Database from './Database';
import { readdirSync } from 'fs';
import path from 'path';
import { ExitStatus } from 'typescript';
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


    async getString(locale: string, key: string, ...replacements: string[]) {
        if(!this.json_loaded) {
            await this.loadJson();
            this.json_loaded = true;
        }
        let json = this.json.get(locale);
        let string = "";
        try {
            const splited_key = key.split(".");
            if(splited_key.length > 1) {
                for(let i = 0; i < splited_key.length; i++) {
                    json = json[splited_key[i]];
                }
            }else {
                string = json[key];
            }
        }catch(e) {
            return "String Not Found! " + key;
        }
        if(json) {
            string = json;
        }
        // console.log(typeof string);
        if(string == "" || string == undefined || string == null) {
            return "String Not Found! " + key;
        }

        if(replacements.length > 0) {
            for(let i = 0; i < replacements.length; i++) {
                string = string.replaceAll("{" + i + "}", replacements[i]);
            }
        }
        // get content betwen {}
        let s: string = String(string);
        // console.log(typeof s)
        let content = s.match(/\{.*?\}/g);
        // console.log(content);
        if(content) {
            content.forEach(async (c) => {
                let code = c.replace("{", "").replace("}", "");
                try {
                    let t = eval(code);
                    string = string.replace(c, t);
                }catch(e) {
                    console.log(e);
                }
            });
        }
        return string;
    }

    async getFullLocale(locale: string) {
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

    async getLocale(guildId: string) {
        const db = await Database.db;
        const entry = await db.collection("settings").findOne({guildId: guildId + ""});
        if(entry) {
            return entry.locale;
        }
        return "de";
    }

}

export default Locale.getInstance();