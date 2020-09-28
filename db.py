import typing
from pydantic import BaseModel
from pydantic import Field


class PhraseInput(BaseModel):
    """Phrase model"""

    # Имя автора. Если не передано - используется стандартное значение.
    author: str = "Anonymous"

    # Текст фразы. Максимальное значение - 200 символов.
    text: str = Field(..., title="Text", description="Text of phrase", max_length=200)


class PhraseOutput(PhraseInput):
    """Phrase output"""

    # ID фразы в нашей базе данных.
    id: typing.Optional[int] = None
