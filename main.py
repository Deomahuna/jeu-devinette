import random
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Jeu de devinette")

# Nombre à deviner, généré une fois au démarrage de l'app.
NUMBER = random.randint(1, 100)


class GuessRequest(BaseModel):
    guess: int


@app.get("/")
def root():
    return {"message": "Bienvenue dans le jeu de devinette ! Devine un nombre entre 1 et 100 via POST /guess."}


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
