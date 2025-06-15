from abc import ABC

# TODO: make this useful, e.g. have a generate_html()?
class Token(ABC):
    pass

class ParagraphToken(Token):
    children: list[Token]
    text: str

class HeaderToken(Token):
    text: str
    size: int

class BoldToken(Token):
    text: str

class EmphToken(Token):
    text: str

class PlainTextToken(Token):
    text: str

