const mqtt = require('mqtt');
const fs = require("node:fs");

let [node, file, topic, message] = process.argv;
const MQTT_BROKER = 'accesscontrol.home';
// const MQTT_BROKER = 'MQTT';

if(message === 'timestamp'){
    message = (new Date()).getTime().toString();
}

// message = `${(new Date()).getTime().toString()}:${'a'.repeat(128)}`

console.log(topic, message);


console.log('Trying to connect to MQTT broker')
const client = mqtt.connect(`mqtt://${MQTT_BROKER}:1883`, {
    //TODO change to debug
    username: 'debug',
    password: 'admin'
});

const messages = {};
client.on('connect', async () => {
    console.log('connected to the broker');

    // client.subscribe('debug/debug', async (err) => {
    //     if(err){
    //         console.log('Error subsribing');
    //         console.log(err);
    //         return;
    //     }
    //     console.log(`subscribed to ${topic}`);

        for(let i = 0; i<25; i++){
            const timestamp = (new Date()).getTime().toString();
            messages[timestamp] = i + 14;

            client.publish(topic, `QWERTYUIOPLKJHGFDSAZXCVBNM`, {}, (err) => {
                err
                    ? console.error('Failed to publish message:', err)
                    : console.log(`message published: ${topic}: ${timestamp}`);
            });
            await delay(550);
        }

    // });

    // client.on('message', (topic, message) => {
    //     console.log(`message on ${topic}: ${message}`)
    //     const date = new Date();
    //
    //     const hours = `0${date.getHours()}`.slice(-2);
    //     const minutes = `0${date.getMinutes()}`.slice(-2);
    //     const seconds = `0${date.getSeconds()}`.slice(-2);
    //
    //     const [ message_timestamp, padding ] = message.toString().split('_');
    //
    //     const bytes = messages[message_timestamp];
    //     const latency =  date.getTime() - Number(message_timestamp);
    //
    //     fs.appendFileSync('log.txt', `[time: ${hours}:${minutes}:${seconds}][timestamp: ${date.getTime()}][topic: ${topic}][latency: ${latency}][bytes: ${bytes}B]\n`)
    // });

    // client.publish(topic, message, {}, (err) => {
    //     err
    //         ? console.error('Failed to publish message:', err)
    //         : console.log('message published');
    //     client.end();
    // });
});

function delay(ms){
    return new Promise(resolve => {
        setTimeout(() => {
            resolve()
        }, ms)
    })
}
