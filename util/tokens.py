from abc import ABC, abstractmethod

# TODO: doco, make a seperate to_string func instead

class Token(ABC):

    @abstractmethod
    def to_html(self) -> str:
        pass



class RawTextToken(Token):
    def __init__(self):
        self.text: str = ""

    def to_html(self):
        # return f"[{self.text}]"
        return f"[RAW TEXT: {repr(self.text)}]\n"

class HeaderToken(Token):
    def __init__(self):
        self.text: str = ""
        self.size: int = 0

    def to_html(self):
        # return f"<h{self.size}>{self.text}</h{self.size}>"
        return f"[HEADER: \"{repr(self.text)}\", SIZE: {self.size}]"

class InlineCodeToken(Token):
    text: str = ""

    def to_html(self):
        return f"<code>self.text</code>"



class ParagraphToken(Token):
    def __init__(self):
        self.children: list[Token] = []

    def to_html(self):
        # Apply to_html() to each child token
        child_html = [token.to_html() for token in self.children]
        # return f"<p>{''.join(child_html)}</p"
        return f"<p>\n{''.join(child_html)}</p"

class BoldToken(Token):
    def __init__(self):
        self.children: list[Token] = []

    # TODO: make this use child tokens instead
    def to_html(self):
        return f"<strong>SAMPLE</strong>"

class EmphToken(Token):
    def __init__(self):
        self.children: list[Token] = []

    # TODO: make this use child tokens instead
    def to_html(self):
        return f"<em>SAMPLE</em>"
