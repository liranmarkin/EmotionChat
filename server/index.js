// Setup basic express server
const express = require('express');
const app = express();
const server = require('http').createServer(app);
const io = require('socket.io')(server);
const PythonShell = require('python-shell');
const port = process.env.PORT || 3000;

server.listen(port, function () {
    console.log('Server listening at port %d', port);
});

// Routing
app.use(express.static(__dirname + '/public'));

// Start python_scripts

const pyshell = new PythonShell('../python_scripts/use_model.py', {mode: 'text'});

const awaited = {};

pyshell.on('message', function (message) {
    message = Buffer.from(message, 'base64').toString().split(" ");
    message_id = message[0];
    const emotion = message[1];
    if (!awaited[message_id]) return;
    awaited[message_id](emotion);
    Reflect.deleteProperty(awaited, message_id);
});

function send_message_pyshell(id, data) {
    const encoded = Buffer.from(`${id} ${data}`).toString('base64');
    pyshell.send(encoded);
    return new Promise((resolve, reject) => {
        awaited[id] = resolve;
        setTimeout(reject, 1000);
    });
}


// Chatroom
let numUsers = 0;
let message_id = 0;
io.on('connection', function (socket) {
    let addedUser = false;

    // when the client emits 'new message', this listens and executes
    socket.on('new message', async function (data) {
        // we tell the client to execute 'new message'
        //data = message
        const id = ++message_id;
        console.log(`${socket.username}: ${data.message}`);
        const emotion = await send_message_pyshell(id, data.message);
        socket.broadcast.emit('new message', {
            username: socket.username,
            message: data.message,
            emotion,
            id
        });
        socket.emit('emotion', {
            local_id: data.local_id,
            emotion
        });
    });

    // when the client emits 'add user', this listens and executes
    socket.on('add user', function (username) {
        if (addedUser) return;

        // we store the username in the socket session for this client
        socket.username = username;
        ++numUsers;
        addedUser = true;
        socket.emit('login', {
            numUsers
        });
        // echo globally (all clients) that a person has connected
        socket.broadcast.emit('user joined', {
            username: socket.username,
            numUsers
        });
    });

    // when the client emits 'typing', we broadcast it to others
    socket.on('typing', function () {
        socket.broadcast.emit('typing', {
            username: socket.username
        });
    });

    // when the client emits 'stop typing', we broadcast it to others
    socket.on('stop typing', function () {
        socket.broadcast.emit('stop typing', {
            username: socket.username
        });
    });

    // when the user disconnects.. perform this
    socket.on('disconnect', function () {
        if (addedUser) {
            --numUsers;

            // echo globally that this client has left
            socket.broadcast.emit('user left', {
                username: socket.username,
                numUsers: numUsers
            });
        }
    });
});