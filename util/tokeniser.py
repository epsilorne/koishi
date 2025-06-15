from util.tokens import *

class Tokeniser:
    input: str
    pos: int = 0

    def __init__(self, input: str):
        self.input = input

    def consume(self):
        if self.pos >= len(self.input):
            return "\0"
        char = self.input[self.pos]
        self.pos += 1
        return char

    def consume_until(self, char: str):
        c: str = self.peek()
        msg: str = ""
        i: int = 0
        while(self.peek() not in char and c != "\0"):
            c = self.consume()
            msg += c
            i += 1
        return (msg, i)

    def consume_while(self, char: str):
        c: str = self.peek()
        msg: str = ""
        i: int = 0
        while(self.peek() in char and c != "\0"):
            c = self.consume()
            msg += c
            i += 1
        return (msg, i)

    def consume_n(self, n: int):
        if self.pos + n >= len(self.input):
            return "\0"
        char = self.input[self.pos + n]
        self.pos += n
        return char

    def peek(self):
        if self.pos >= len(self.input):
            return "\0"
        return self.input[self.pos]

    def peek_n(self, n: int):
        if self.pos + n >= len(self.input):
            return "\0"
        return self.input[self.pos + n]

    def eof(self):
        return self.peek() == "\0"

    def parse_richtext(self):
        txt: str = ""

        while (curr := self.peek()) != "\0":
            # A new line followed by whitespace is a new paragraph
            if curr == "\n" and self.peek_n(1).isspace():
                self.consume_while("\n\r\t ")
                break

            if curr == "*":
                # If whitespace exists after '*', treat as an unordered list
                if self.peek_n(1).isspace():
                    continue

                # TODO: fix because right now, it does not handle inline rich text, e.g
                # An **inline *rich text* test**!
                (_, n) = self.consume_while("*")
                (txt_new, _) = self.consume_until("*")
                self.consume_n(n)

                # TODO: use token objects
                if n == 2:
                    txt += f"<strong>{txt_new}</strong>"
                elif n == 1:
                    txt += f"<emph>{txt_new}</emph>"
                else:
                    # For more than three asterixes, just default to emph-strong
                    txt += f"<emph><strong>{txt_new}</strong></emph>"

            # TODO: inline code, lists, etc.

            txt += self.peek()
            self.consume()

        # TODO: create the token 
        print(f"<p>{txt}</p>\n")

    # The 'main' tokeniser function; reads the input stream and builds tokens
    def read_stream(self):
        while self.peek() != "\0":
            curr = self.peek()

            # Ignore leading whitespace
            if curr.isspace():
                self.consume()
                continue

            # HEADER
            if curr == "#":
                (_, n) = self.consume_while("#")
                (txt, _) = self.consume_until("\n")

                # TODO: make token object
                print(f"<h{n}>{txt.strip()}</h{n}>\n")
                continue

            # TODO: block quotes, code blocks, hrule, etc

            # Otherwise, parse as a rich text paragraph
            self.parse_richtext()
