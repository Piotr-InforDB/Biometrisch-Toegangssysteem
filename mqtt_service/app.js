const mqtt = require('mqtt');
const { machineIdSync } = require('node-machine-id');

const identity = {
    type: 'HUB',
    name: 'Central HUB',
    id: machineIdSync(),
}
const broker = 'accesscontrol.home';
const topics = [ 'presence' ];


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
    switch (topic){
        case 'presence': await presence(message); break;
    }
});

// Callbacks
async function presence(){
    client.publish('presence/confirm', JSON.stringify(identity));
    console.log(identity);
}

