const fs = require('fs');
const { SerialPort } = require('serialport');
const { ReadlineParser } = require('@serialport/parser-readline');

const portName = 'COM4';
const baudRate = 115200;
const logFile = 'log.txt';
const topic = 'debug/debug';

const port = new SerialPort({ path: portName, baudRate });
const parser = port.pipe(new ReadlineParser({ delimiter: '\r\n' }));

const logStream = fs.createWriteStream(logFile, { flags: 'a' });

parser.on('data', (line) => {
    const [ rx_timestamp, message ] = line.split('_');

    const encoder = new TextEncoder();
    const bytes = encoder.encode(message);

    console.log(message)
    console.log(bytes)
    console.log(bytes.length + 14);

    const now = new Date();
    const time = now.toTimeString().split(' ')[0];
    const timestamp = now.getTime();
    const formatted = `[time: ${time}][timestamp: ${timestamp}][topic: ${topic}][latency: ${timestamp - Number(rx_timestamp)}][bytes: ${bytes.length + 14}B]\n`;
    // console.log(formatted);
    // logStream.write(formatted);

});

port.on('error', (err) => {
    console.error('Serial port error:', err.message);
});
