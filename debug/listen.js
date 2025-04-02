const mqtt = require('mqtt');

const [node, file, topic] = process.argv;
const MQTT_BROKER = 'accesscontrol.home';
// const MQTT_BROKER = 'MQTT';


console.log('Trying to connect to MQTT broker')
const client = mqtt.connect(`mqtt://${MQTT_BROKER}:1883`, {
    //TODO change to debug
    username: 'debug',
    password: 'admin'
});

client.on('connect', () => {
    console.log('connected to the broker')

    client.subscribe(topic, (err) => {
        if(err){
            console.log('Error subsribing');
            console.log(err);
            return;
        }
        console.log(`subscribed to ${topic}`);
    });

});

client.on('message', (topic, message) => {
    console.log(`message on ${topic}: ${message}`)
});
