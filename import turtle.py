const express = require('express');
const http = require('http');
const socketIo = require('socket.io');

const app = express();
const server = http.createServer(app);
const io = socketIo(server);

app.use(express.static('public'));

const BIN_ID = '67cd3f38ad19ca34f819048e';
const API_URL = `https://api.jsonbin.io/v3/b/${BIN_ID}`;
const API_KEY = '67cd4112acd3cb34a8f77dbc; // Buraya kendi API anahtarını eklemelisin

async function fetchScores() {
    const response = await fetch(API_URL, {
        headers: { 'X-Master-Key': API_KEY }
    });
    const data = await response.json();
    return data.record.scores;
}

async function updateScores(newScores) {
    await fetch(API_URL, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            'X-Master-Key': API_KEY
        },
        body: JSON.stringify({ scores: newScores })
    });
}

io.on('connection', (socket) => {
    console.log('Bir oyuncu bağlandı:', socket.id);
    
    fetchScores().then(scores => {
        socket.emit('leaderboard', scores);
    });

    socket.on('submitScore', async ({ playerName, score }) => {
        let scores = await fetchScores();
        scores.push({ name: playerName, score });
        scores.sort((a, b) => b.score - a.score);
        scores = scores.slice(0, 10); // İlk 10 skoru tut
        await updateScores(scores);
        io.emit('leaderboard', scores);
    });

    socket.on('disconnect', () => {
        console.log('Bir oyuncu ayrıldı:', socket.id);
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

socket.on('leaderboard', (scores) => {
    const leaderboard = document.getElementById("highScores");
    leaderboard.innerHTML = "";
    scores.forEach((entry, index) => {
        const li = document.createElement("li");
        li.textContent = `${index + 1}. ${entry.name}: ${entry.score}`;
        leaderboard.appendChild(li);
    });
});

function submitScore(score) {
    socket.emit('submitScore', { playerName, score });
}

function generateQuestion() {
    let num1 = Math.floor(Math.random() * 10) + 1;
    let num2 = Math.floor(Math.random() * 10) + 1;
    let correctAnswer = num1 * num2;
    document.getElementById("questionDisplay").textContent = `${num1} × ${num2} = ?`;
    document.getElementById("inputField").oninput = function () {
        let userAnswer = parseInt(this.value);
        if (userAnswer === correctAnswer) {
            submitScore(3);
            this.value = "";
            generateQuestion();
        }
    };
}
