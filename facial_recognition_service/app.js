const mqtt = require('mqtt');


console.log('Trying to connect to MQTT broker')
const client = mqtt.connect('mqtt://accesscontrol.home:1883', {
// const client = mqtt.connect('mqtt://MQTT:1883', {
    username: 'facial_recognition_service',
    password: 'admin'
});

client.on('connect', () => {
   console.log('connected to the broker')

    client.subscribe('test/topic', (err) => {
       if(err){
           console.log('Error subsribing');
           console.log(err);
           return;
       }
       console.log('subscribed to test/topic');

       setInterval(() => {
           client.publish('test/topic', 'message test');
           console.log('message published');
       }, 2500);
    });

});

client.on('message', (topic, message) => {
    console.log(`message on ${topic}: ${message}`)
});
