const {machineIdSync} = require("node-machine-id");

const broker = 'accesscontrol.home';
const identity = {
    type: 'HUB',
    name: 'Central HUB',
    id: machineIdSync(),
}
const topics = [
    'presence',
    'client/identity'
];

module.exports = { broker, identity, topics }
