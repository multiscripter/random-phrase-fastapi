from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import Response
from db import PhraseInput
from db import PhraseOutput
from Database import Database

# run server:
# uvicorn controller:app

app = FastAPI(title="Random phrase")
db = Database()


@app.get(
    "/get",
    description="Get random phrase from database",
    response_description="Random phrase",
    response_model=PhraseOutput,
    status_code=200
)
async def get():
    try:
        phrase = db.get(db.get_random())
    except IndexError:
        raise HTTPException(404, "Phrase list is empty")
    return phrase


@app.post(
    "/add",
    response_description="Added phrase with *id* parameter",
    response_model=PhraseOutput,
    status_code=201
)
async def add(phrase: PhraseInput):
    phrase_out = db.add(phrase)
    return phrase_out


@app.delete(
    "/delete/{id}",
    response_description="Affected values",
    status_code=200
)
async def delete(id: int, response: Response):
    return db.delete(id)


@app.patch(
    "/update/{id}",
    response_description="Update phrase by id",
    response_model=PhraseOutput,
    status_code=205
)
async def update(id: int, phrase: PhraseInput):
    phrase_out = db.update(id, phrase)
    return phrase_out
