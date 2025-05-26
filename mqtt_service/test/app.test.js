jest.mock('mqtt');
jest.mock('node-machine-id', () => ({
    machineIdSync: jest.fn(() => 'mocked-id'),
}));

describe('MQTT Service', () => {
    let clientMock;

    beforeEach(() => {
        clientMock = {
            on: jest.fn(),
            subscribe: jest.fn((_, cb) => cb(null)),
            publish: jest.fn(),
        };

        require('mqtt').connect.mockReturnValue(clientMock);
    });

    test('connects to MQTT broker', () => {
        jest.isolateModules(() => {
            require('../app');
        });

        expect(require('mqtt').connect).toHaveBeenCalledWith('mqtt://accesscontrol.home:1883', {
            username: 'mqtt_service',
            password: 'admin',
        });
    });

    test('subscribes to presence and client/identity topics', () => {
        jest.isolateModules(() => {
            clientMock.on.mockImplementation((event, cb) => {
                if (event === 'connect') cb();
            });

            require('../app');
        });

        expect(clientMock.subscribe).toHaveBeenCalledWith('presence', expect.any(Function));
        expect(clientMock.subscribe).toHaveBeenCalledWith('client/identity', expect.any(Function));
    });

    test('publishes identity on presence', () => {
        jest.isolateModules(() => {
            clientMock.on.mockImplementation((event, cb) => {
                if (event === 'message') cb('presence', Buffer.from('anything'));
            });

            require('../app');
        });

        expect(clientMock.publish).toHaveBeenCalledWith(
            'presence/confirm',
            JSON.stringify({
                type: 'HUB',
                name: 'Central HUB',
                id: 'mocked-id',
            })
        );
    });

    test('publishes identity on client/identity with matching id', () => {
        jest.isolateModules(() => {
            clientMock.on.mockImplementation((event, cb) => {
                if (event === 'message') cb('client/identity', Buffer.from('mocked-id'));
            });

            require('../app');
        });

        expect(clientMock.publish).toHaveBeenCalledWith(
            'client/identity/mocked-id',
            JSON.stringify({
                type: 'HUB',
                name: 'Central HUB',
                id: 'mocked-id',
            })
        );
    });
});
