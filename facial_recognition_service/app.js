const mqtt = require('mqtt');

const [node, file, topic, message] = process.argv;

console.log(topic, message);

console.log('FRS Trying to connect to MQTT broker')
const client = mqtt.connect('mqtt://accesscontrol.home:1883', {
// const client = mqtt.connect('mqtt://localhost:1883', {
    username: 'facial_recognition_service',
    password: 'admin'
});

client.on('connect', () => {
   console.log('FRS connected to the broker')

    client.subscribe(topic, (err) => {
       if(err){
           console.log('FRS Error subsribing');
           console.log(err);
           return;
       }
       console.log(`FRS subscribed to ${topic}`);

       // setInterval(() => {
           client.publish(topic, message);
           console.log('FRS message published');
       // }, 2000);
    });

});

client.on('message', (topic, message) => {
    console.log(`message on ${topic}: ${message}`)
});
