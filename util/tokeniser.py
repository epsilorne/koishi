from util.tokens import *

class Tokeniser:
    input: str
    pos: int = 0
    in_bold: bool = False
    in_emph: bool = False
    in_code: bool = False

    # A 'stack' to store the order of emphs/strongs
    stack: list[str] = []

    def __init__(self, input: str):
        self.input = input

    def consume(self):
        if self.pos >= len(self.input):
            return "\0"
        char = self.input[self.pos]
        self.pos += 1
        return char

    def consume_until(self, delims: str):
        c: str = self.peek()
        msg: str = ""
        i: int = 0
        while(self.peek() not in delims and c != "\0"):
            c = self.consume()
            msg += c
            i += 1
        return (msg, i)

    def consume_while(self, delims: str):
        c: str = self.peek()
        msg: str = ""
        i: int = 0
        while(self.peek() in delims and c != "\0"):
            c = self.consume()
            msg += c
            i += 1
        return (msg, i)

    def consume_n(self, n: int):
        if self.pos + n >= len(self.input) or self.pos + n < 0:
            return "\0"
        char = self.input[self.pos + n]
        self.pos += n
        return char

    def peek(self):
        if self.pos >= len(self.input):
            return "\0"
        return self.input[self.pos]

    def peek_n(self, n: int):
        if self.pos + n >= len(self.input) or self.pos + n < 0:
            return "\0"
        return self.input[self.pos + n]

    def eof(self):
        return self.peek() == "\0"

    def parse_paragraph(self):
        self.in_bold = False
        self.in_emph = False
        token = ParagraphToken()
        
        # TODO: make paragraph token use child tokens
        txt: str = ""

        while (curr := self.peek()) != "\0":
            # A new line followed by whitespace is a new paragraph
            if curr == "\n" and self.peek_n(1).isspace():
                self.consume_while("\n\r\t ")
                break

            if curr == "*":
                # If whitespace exists before and after '*', treat as an unordered list
                if self.peek_n(1).isspace() and self.peek_n(-1).isspace():
                    # TODO: unordered list function
                    self.consume()
                    txt += self.consume_until("\n")[0].strip()
                    break

                # If character after is '*', we do some form of strong highlighting
                if self.peek_n(1) == "*":
                    # TODO: use proper tokens

                    # If the character AFTER that is '*', i.e. '***', we do strong emph
                    if self.peek_n(2) == "*":

                        # For the terminating '***' we base it on the order of strong/emphs
                        if self.in_bold and self.in_emph:
                            self.in_bold = False
                            self.in_emph = False
                            txt += self.stack.pop()
                            txt += self.stack.pop()

                        # Otherwise, the default '***' is strong-emph
                        else:
                            self.in_bold = True
                            self.in_emph = True

                            # TODO: this behaviour could be something like an 'add token(s) to stack',
                            # likewise for the rest of them
                            txt += "<strong><em>"
                            self.stack.append("</strong>")
                            self.stack.append("</em>")

                    # Otherwise, just do regular strong
                    else:
                        if self.in_bold:
                            self.in_bold = False
                            txt += self.stack.pop()
                        else:
                            self.in_bold = True
                            txt += "<strong>"
                            self.stack.append("</strong>")

                # Otherwise, it is just emphasised (italic)
                else:
                    if self.in_emph:
                        self.in_emph = False
                        txt += self.stack.pop()
                    else:
                        self.in_emph = True
                        txt += "<em>"
                        self.stack.append("</em>")

                self.consume_while("*")
                continue

            # TODO: lists, links, etc.
            if curr == "`":
                if self.in_code:
                    self.in_code = False
                    txt += "</code>"
                else:
                    self.in_code = True
                    txt += "<code>"
                self.consume()
                continue

            txt += self.peek()
            self.consume()

        # We 'empty' the stack for this paragraph, e.g. for the event of malformed markdown
        while self.stack:
            txt += self.stack.pop()

        token.text = txt
        return token

    def parse_header(self):
        token = HeaderToken()

        (_, n) = self.consume_while("#")
        (txt, _) = self.consume_until("\n")

        token.size = n
        token.text = txt.strip()
        return token

    # The 'main' tokeniser function; reads the input stream and builds tokens
    def read_stream(self):
        while self.peek() != "\0":
            curr = self.peek()
            token = Token()

            # Ignore leading whitespace
            if curr.isspace():
                self.consume()
                continue

            # HEADER
            if curr == "#":
                token = self.parse_header()

            # TODO: block quotes, code blocks, hrule, images, etc

            # Otherwise, parse as a rich text paragraph
            else:
                token = self.parse_paragraph()

            print(f"{token.text}\n")
