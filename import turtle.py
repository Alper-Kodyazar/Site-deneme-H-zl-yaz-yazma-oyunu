const BIN_ID = '67cd3f38ad19ca34f819048e';
const API_URL = `https://api.jsonbin.io/v3/b/${BIN_ID}`;
const API_KEY = '$2a$10$vNoOaSfyDIdCbPLyv6uUtOJsSsmhdzJDJBPs/26O9wfHNEtZoA4BK '; // 

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

document.addEventListener("DOMContentLoaded", () => {
    const nameInput = document.getElementById("nameInput");
    const startButton = document.getElementById("startButton");
    const gameContainer = document.getElementById("game");
    const questionDisplay = document.getElementById("questionDisplay");
    const inputField = document.getElementById("inputField");
    const scoreDisplay = document.getElementById("score");
    const leaderboard = document.getElementById("highScores");

    let playerName;
    let score = 0;

    startButton.addEventListener("click", () => {
        playerName = nameInput.value.trim();
        if (!playerName) {
            alert("Lütfen bir isim girin!");
            return;
        }
        gameContainer.style.display = "block";
        generateQuestion();
        loadLeaderboard();
    });

    function generateQuestion() {
        let num1 = Math.floor(Math.random() * 10) + 1;
        let num2 = Math.floor(Math.random() * 10) + 1;
        let correctAnswer = num1 * num2;
        questionDisplay.textContent = `${num1} × ${num2} = ?`;

        inputField.oninput = function () {
            let userAnswer = parseInt(this.value);
            if (userAnswer === correctAnswer) {
                score += 3;
                scoreDisplay.textContent = score;
                this.value = "";
                generateQuestion();
                saveScore();
            }
        };
    }

    async function saveScore() {
        let scores = await fetchScores();
        scores.push({ name: playerName, score });
        scores.sort((a, b) => b.score - a.score);
        scores = scores.slice(0, 10);
        await updateScores(scores);
        loadLeaderboard();
    }

    async function loadLeaderboard() {
        let scores = await fetchScores();
        leaderboard.innerHTML = "";
        scores.forEach((entry, index) => {
            const li = document.createElement("li");
            li.textContent = `${index + 1}. ${entry.name}: ${entry.score}`;
            leaderboard.appendChild(li);
        });
    }
});
