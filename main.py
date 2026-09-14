import random
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

app = FastAPI(title="Jeu de devinette")

# Nombre à deviner, généré une fois au démarrage de l'app.
NUMBER = random.randint(1, 100)


class GuessRequest(BaseModel):
    guess: int


@app.get("/", response_class=HTMLResponse)
def root():
    return """
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8" />
        <title>Jeu de devinette</title>
        <style>
            body { font-family: system-ui, sans-serif; max-width: 420px; margin: 60px auto; padding: 0 20px; }
            h1 { font-size: 22px; }
            input { font-size: 16px; padding: 8px 10px; width: 100px; }
            button { font-size: 16px; padding: 8px 16px; margin-left: 8px; cursor: pointer; }
            #result { margin-top: 20px; font-size: 15px; padding: 12px; border-radius: 6px; }
            .win { background: #dcfce7; color: #166534; }
            .low, .high { background: #fef3c7; color: #92400e; }
        </style>
    </head>
    <body>
        <h1>Devine un nombre entre 1 et 100</h1>
        <input type="number" id="guess" min="1" max="100" placeholder="Ton essai" />
        <button onclick="tryGuess()">Deviner</button>
        <div id="result"></div>

        <script>
            async function tryGuess() {
                const value = document.getElementById("guess").value;
                const resultDiv = document.getElementById("result");
                if (!value) return;

                const res = await fetch("/guess", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ guess: parseInt(value, 10) }),
                });
                const data = await res.json();

                resultDiv.textContent = data.result;
                resultDiv.className = data.correct ? "win" : (value < 50 ? "low" : "high");
            }
        </script>
    </body>
    </html>
    """


@app.post("/guess")
def guess(payload: GuessRequest):
    if payload.guess == NUMBER:
        return {"result": "Tu as deviné le nombre juste !", "correct": True}
    elif payload.guess < NUMBER:
        return {"result": "Il te reste un peu à ajouter pour deviner.", "correct": False}
    else:
        return {"result": "Ton entier est trop grand pour deviner la valeur juste.", "correct": False}


@app.get("/health")
def health():
    return {"status": "ok"}
