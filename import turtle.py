const express = require('express');
const http = require('http');
const socketIo = require('socket.io');

const app = express();
const server = http.createServer(app);
const io = socketIo(server);

app.use(express.static('public'));

let waitingPlayer = null;
let rooms = {};

io.on('connection', (socket) => {
    console.log('Bir oyuncu bağlandı:', socket.id);
    
    if (waitingPlayer) {
        const room = `room-${waitingPlayer.id}-${socket.id}`;
        rooms[room] = { players: [waitingPlayer, socket], scores: {} };
        waitingPlayer.join(room);
        socket.join(room);
        io.to(room).emit('gameStart', { room });
        console.log(`Oyun başladı: ${room}`);
        waitingPlayer = null;
    } else {
        waitingPlayer = socket;
    }

    socket.on('answer', ({ room, answer, playerName }) => {
        if (rooms[room]) {
            if (!rooms[room].scores[playerName]) {
                rooms[room].scores[playerName] = 0;
            }
            rooms[room].scores[playerName] += answer.correct ? 3 : 0;
            io.to(room).emit('updateScores', rooms[room].scores);
        }
    });

    socket.on('disconnect', () => {
        console.log('Bir oyuncu ayrıldı:', socket.id);
        for (let room in rooms) {
            if (rooms[room].players.includes(socket)) {
                io.to(room).emit('opponentLeft');
                delete rooms[room];
            }
        }
    });
});

server.listen(3000, () => {
    console.log('Sunucu 3000 portunda çalışıyor');
});

// İstemci tarafı kodu
const socket = io();
let playerName;
let room;

function startGame() {
    playerName = document.getElementById("nameInput").value;
    if (playerName === "") {
        alert("Lütfen bir isim girin!");
        return;
    }
    document.getElementById("game").style.display = "block";
    generateQuestion();
}

socket.on('gameStart', (data) => {
    room = data.room;
    document.getElementById("game").style.display = "block";
    generateQuestion();
});

socket.on('updateScores', (scores) => {
    document.getElementById("score").textContent = scores[playerName] || 0;
});

socket.on('opponentLeft', () => {
    alert("Rakibiniz oyundan ayrıldı. Yeni bir rakip bekleyin.");
    location.reload();
});

function generateQuestion() {
    let num1 = Math.floor(Math.random() * 10) + 1;
    let num2 = Math.floor(Math.random() * 10) + 1;
    let correctAnswer = num1 * num2;
    document.getElementById("questionDisplay").textContent = `${num1} × ${num2} = ?`;
    document.getElementById("inputField").oninput = function () {
        let userAnswer = parseInt(this.value);
        if (userAnswer === correctAnswer) {
            socket.emit('answer', { room, answer: { correct: true }, playerName });
            this.value = "";
            generateQuestion();
        }
    };
}
