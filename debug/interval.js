const mqtt = require('mqtt');

const [node, file, topic, message, interval] = process.argv;
const MQTT_BROKER = 'accesscontrol.home';
// const MQTT_BROKER = 'MQTT';

console.log(topic, message);


console.log('Trying to connect to MQTT broker')
const client = mqtt.connect(`mqtt://${MQTT_BROKER}:1883`, {
    //TODO change to debug
    username: 'debug',
    password: 'admin'
});

client.on('connect', () => {
    console.log('connected to the broker');
    setInterval(() => {
        client.publish(topic, message, {}, (err) => {
            err
                ? console.error('Failed to publish message:', err)
                : console.log('message published');
            // client.end();
        });
    }, interval || 2000);
});
