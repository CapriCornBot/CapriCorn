
class Locale {
    static async getString(locale, key) {
        let json = await import(`../Locale/${locale}.json`);
        console.log(json);
        const splited_key = key.split(".");
        for(let i = 0; i < splited_key.length; i++) {
            json = json[splited_key[i]];
        }
        return json;
    }
}

export default Locale;