const mqtt = require('mqtt');
const fs = require("node:fs");

let [node, file, topic, message] = process.argv;
const MQTT_BROKER = 'accesscontrol.home';
// const MQTT_BROKER = 'MQTT';

if(message === 'timestamp'){
    message = (new Date()).getTime().toString();
}
console.log(topic, message);
console.log('Trying to connect to MQTT broker')

const client = mqtt.connect(`mqtt://${MQTT_BROKER}:1883`, {
    //TODO change to debug
    username: 'debug',
    password: 'admin'
});

client.on('connect', async () => {
    console.log('connected to the broker');
    client.publish(topic, message, {}, (err) => {
        err
            ? console.error('Failed to publish message:', err)
            : console.log('message published');
        client.end();
    });
});
