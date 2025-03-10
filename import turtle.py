<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hızlı Çarp - Botlu</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            text-align: center;
            background-color: #121212;
            color: white;
        }
        #game {
            margin-top: 20px;
        }
        #questionDisplay {
            font-size: 24px;
            margin: 20px 0;
        }
        input {
            font-size: 18px;
            padding: 5px;
            text-align: center;
        }
        button {
            font-size: 18px;
            padding: 10px;
            margin-top: 10px;
        }
    </style>
</head>
<body>
    <h1>Hızlı Çarp</h1>
    <p>Lütfen isminizi girin:</p>
    <input type="text" id="nameInput" placeholder="İsminiz">
    <button onclick="startGame()">Başla</button>

    <div id="game" style="display:none;">
        <p id="timer">Süre: 60</p>
        <p id="questionDisplay"></p>
        <input type="number" id="inputField" placeholder="Sonucu yazın">
        <button onclick="checkAnswer()">Gönder</button>
        <p>Senin Skorun: <span id="playerScore">0</span></p>
        <p>Bot Skoru: <span id="botScore">0</span></p>
    </div>

    <script>
        let playerScore = 0;
        let botScore = 0;
        let correctAnswer = 0;
        let timeLeft = 60;
        let difficulty = 1;

        function startGame() {
            const playerName = document.getElementById("nameInput").value;
            if (!playerName) {
                alert("Lütfen bir isim girin!");
                return;
            }
            document.getElementById("game").style.display = "block";
            generateQuestion();
            startTimer();
            botTurn();
        }

        function generateQuestion() {
            let num1 = Math.floor(Math.random() * (10 * difficulty)) + 1;
            let num2 = Math.floor(Math.random() * (10 * difficulty)) + 1;
            correctAnswer = num1 * num2;
            document.getElementById("questionDisplay").textContent = `${num1} × ${num2} = ?`;
        }

        function checkAnswer() {
            const playerAnswer = parseInt(document.getElementById("inputField").value);
            if (playerAnswer === correctAnswer) {
                playerScore += 3;
                difficulty++;
            }
            document.getElementById("playerScore").textContent = playerScore;
            generateQuestion();
        }

        function botTurn() {
            setTimeout(() => {
                let botAnswer = correctAnswer + (Math.random() > 0.7 ? Math.floor(Math.random() * 10) - 5 : 0);
                if (botAnswer === correctAnswer) {
                    botScore += 3;
                }
                document.getElementById("botScore").textContent = botScore;
                generateQuestion();
                botTurn();
            }, Math.floor(Math.random() * 3000) + 2000);
        }

        function startTimer() {
            const timerDisplay = document.getElementById("timer");
            const interval = setInterval(() => {
                timeLeft--;
                timerDisplay.textContent = `Süre: ${timeLeft}`;
                if (timeLeft <= 0) {
                    clearInterval(interval);
                    alert(`Oyun Bitti! Skorun: ${playerScore}, Bot Skoru: ${botScore}`);
                }
            }, 1000);
        }
    </script>
</body>
</html>

