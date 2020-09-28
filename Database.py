import redis
import random

from fastapi import HTTPException
from pydantic import typing
from db import PhraseInput
from db import PhraseOutput


class Database:
    """Our **fake** database."""

    def __init__(self):
        self.name = 'phrases'
        self.items = redis.Redis(db=1)

    def get_random(self) -> int:
        """Получение случайной фразы."""

        chosen = random.choice(self.items.keys(f'{self.name}*'))
        id = chosen.decode("utf-8").split(':')[1]
        return id

    def get(self, id: int) -> typing.Optional[PhraseOutput]:
        """Получение фразы по ID."""

        bin_dict = self.items.hgetall(f'{self.name}:{id}')
        data = dict()
        for k, v in bin_dict.items():
            data[k.decode("utf-8")] = v.decode("utf-8")
        return PhraseOutput(**data)

    def add(self, phrase: PhraseInput) -> PhraseOutput:
        """Добавление фразы."""

        keys = list(self.items.keys(f'{self.name}:*'))
        size = len(keys)
        if not size:
            id = 1
        else:
            keys = sorted(keys)
            id = int(keys[size - 1].decode("utf-8").split(':')[1]) + 1
        phrase_out = PhraseOutput(id=id, **phrase.dict())
        id = f'{self.name}:{id}'
        for k, v in phrase_out.dict().items():
            self.items.hset(id, k, v)
        return phrase_out

    def delete(self, id: int) -> int:
        """Удаляет ключ и связанное содержимое."""

        if self.items.exists(f'{self.name}:{id}'):
            return self.items.delete(f'{self.name}:{id}')
        else:
            raise HTTPException(404, 'Element is not exists')

    def update(self, id: int, phrase: PhraseInput) -> PhraseOutput:
        """Обновление фразы."""

        id = f'{self.name}:{id}'
        bin_dict = self.items.hgetall(id)
        data = dict()
        phrase = phrase.dict()
        if bin_dict:
            for k, v in bin_dict.items():
                k = k.decode("utf-8")
                data[k] = v.decode("utf-8")
                if k in phrase:
                    self.items.hset(id, k, phrase[k])
                    data[k] = phrase[k]
            return PhraseOutput(**data)
