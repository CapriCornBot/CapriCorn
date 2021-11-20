// mongodb connector
import { Db, MongoClient } from 'mongodb';
import config from '../config.json';
class MongoDB {
    private static _instance: MongoDB;
    private _db: Db;
    private _client: MongoClient;
    private constructor() {
        this._client = new MongoClient(config.mongo.uri);
        this._client.connect(err => {
            if (err) {
                console.log(err);
                return;
            }
            this._db = this._client.db();
        });
    }
    public static getInstance(): MongoDB {
        if (!MongoDB._instance) {
            MongoDB._instance = new MongoDB();
        }
        return MongoDB._instance;
    }
    public get db(): Db {
        return this._db;
    }
}

export default MongoDB.getInstance();