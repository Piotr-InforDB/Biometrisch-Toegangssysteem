const express = require('express');
const mqtt = require('mqtt');
const http = require('http');
const socket = require('socket.io');

console.log('KS Trying to connect to MQTT broker')
//TODO Change ip
const client = mqtt.connect('mqtt://accesscontrol.home:1883', {
// const client = mqtt.connect('mqtt://localhost:1883', {
    username: 'kiosk_service',
    password: 'admin'
});

let last_frame;

// // MQTT
client.on('connect', () => {
    console.log('KS connected to the broker')

    client.subscribe('webcam/feed', (err) => {
        if(err){
            console.log('KS Error subsribing');
            console.log(err);
            return;
        }

        console.log(`KS subscribed to webcam/feed`);
    });

});
client.on('message', (topic, message) => {
    console.log(`message on ${topic}:`);
    // console.log(message)
    last_frame = message.toString('base64');
});

//HTTP Server
const app = express();
const hostname = 'localhost';
const port = 3000;
const server = http.createServer((app));

app.use(express.static('public'));
server.listen(port, hostname, () => {
    console.log(`Server running at http://${hostname}:${port}/`);
});

//Socketio
const io = new socket.Server(server);

io.on('connection', (socket) => {
    console.log('A user connected');

    socket.on('request_frame', (message) => {
        socket.emit('frame', last_frame)
        console.log(message)
    })

    socket.on('disconnect', () => {
        console.log('User disconnected');
    });
});
