print('Start #################################################################');
db = db.getSiblingDB('udbank');
db.createUser(
    {
        user: "root",
        pwd: "root",
        roles: [
            {
                role: "root",
                db: "admin"
            }
        ]
    }
);
db.createUser(
    {
        user: "udbank",
        pwd: "udbank",
        roles: [
            {
                role: "root",
                db: "admin"
            }
        ]
    }
);
db.createCollection('metadata');
db.createCollection('markets');
db.createCollection('users');

// db.createCollection('token');