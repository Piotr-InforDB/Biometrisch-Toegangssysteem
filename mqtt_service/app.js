const mqtt = require('mqtt');
const { broker, identity, topics } = require('./vaiables')

console.log('Trying to connect to MQTT broker')
const client = mqtt.connect(`mqtt://${broker}:1883`, {
    username: 'mqtt_service',
    password: 'admin'
});

// MQTT Client
client.on('connect', () => {
    console.log('connected to the broker')
    topics.forEach(topic => {
        client.subscribe(topic, (err => {
            if(err){
                console.log(`Failed subscribing to ${topic}`);
                return;
            }

            console.log(`Subscribed to ${topic}`)
        }));
    });
});
client.on('message', async (topic, message) => {
    console.log(`Received ${topic}: ${message.toString()}`);
    switch (topic){
        case 'presence': await presence(message); break;
        case 'client/identity': await clientIdentity(message); break;
    }
});

// Callbacks
async function presence(){
    client.publish('presence/confirm', JSON.stringify(identity));
    console.log(identity);
}
async function clientIdentity(message){
    if(message.toString() !== identity.id){ return }
    client.publish(`client/identity/${identity.id}`, JSON.stringify(identity));
    console.log(identity);
}

