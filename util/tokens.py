from abc import ABC, abstractmethod

# TODO: doco

class Token(ABC):

    @abstractmethod
    def to_html(self) -> str:
        pass



class RawTextToken(Token):
    def __init__(self):
        self.text: str = ""

    def to_html(self):
        return self.text

class HeaderToken(Token):
    def __init__(self):
        self.text: str = ""
        self.size: int = 0

    def to_html(self):
        return f"<h{self.size}>{self.text}</h{self.size}>"

class InlineCodeToken(Token):
    text: str = ""

    def to_html(self):
        return f"<code>{self.text}</code>"



class ParagraphToken(Token):
    def __init__(self):
        self.children: list[Token] = []

    def to_html(self):
        # Apply to_html() to each child token
        child_html = [token.to_html() for token in self.children]
        return f"<p>{''.join(child_html)}</p>"

class BoldToken(Token):
    def __init__(self):
        self.children: list[Token] = []

    def to_html(self):
        child_html = [token.to_html() for token in self.children]
        return f"<strong>{''.join(child_html)}</strong>"

class EmphToken(Token):
    def __init__(self):
        self.children: list[Token] = []

    def to_html(self):
        child_html = [token.to_html() for token in self.children]
        return f"<em>{''.join(child_html)}</em>"
