from util.tokens import *

class Tokeniser:
    input: str
    pos: int = 0
    in_code: bool = False

    # A 'stack' to store the order of emphs/strongs
    stack: list[ParagraphToken | EmphToken | BoldToken] = []

    # A buffer to temporarily store raw text
    buffer: str = ""

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

    # TODO: proper doco
    # Helper function to add a raw text token to a parent token
    def end_raw_text(self, paragraph_token: ParagraphToken | BoldToken | EmphToken):
        if self.buffer == "":
            return

        raw_text = RawTextToken()
        raw_text.text = self.buffer
        paragraph_token.children.append(raw_text)

        self.buffer = ""

    def parse_paragraph(self) -> ParagraphToken:
        paragraph_token = ParagraphToken()
        self.stack = []
        self.stack.append(paragraph_token)

        while (curr := self.peek()) != "\0":
            # A new line followed by whitespace is a new paragraph
            if curr == "\n" and self.peek_n(1).isspace():
                self.consume_while("\n\r\t ")
                self.end_raw_text(paragraph_token)
                break

            if curr == "*":
                # When encountering a 'special character', save to parent token (top of stack)
                self.end_raw_text(self.stack[-1])

                # If whitespace exists before and after '*', treat as an unordered list
                if self.peek_n(1).isspace() and self.peek_n(-1).isspace():
                    # TODO: unordered list function
                    self.consume()
                    # TODO: this gets the text up until the end of line; can populate list token with it
                    self.consume_until("\n")[0].strip()
                    break

                # If character after is '*', we do some form of strong highlighting
                if self.peek_n(1) == "*":

                    # If the character AFTER that is '*', i.e. '***', we do strong emph
                    if self.peek_n(2) == "*":

                        # For the terminating '***' we base it on the order of strong/emphs
                        # TODO: redo this statement
                        if isinstance(self.stack[-1], BoldToken | EmphToken) and isinstance(self.stack[-2], BoldToken | EmphToken):
                            self.stack.pop()
                            self.stack.pop()

                        # Otherwise, the default '***' is strong-emph
                        else:
                            parent = self.stack[-1]
                            self.stack.append(BoldToken())
                            parent.children.append(self.stack[-1])

                            parent = self.stack[-1]
                            self.stack.append(EmphToken())
                            parent.children.append(self.stack[-1])

                    # Otherwise, just do regular strong
                    else:
                        if isinstance(self.stack[-1], BoldToken):
                            self.stack.pop()
                        else:
                            parent = self.stack[-1]
                            self.stack.append(BoldToken())
                            parent.children.append(self.stack[-1])

                # Otherwise, it is just emphasised (italic)
                else:
                    if isinstance(self.stack[-1], EmphToken):
                        self.stack.pop()
                    else:
                        parent = self.stack[-1]
                        self.stack.append(EmphToken())
                        parent.children.append(self.stack[-1])

                self.consume_while("*")

            # TODO: lists, links, etc.
            elif curr == "`":
                if self.in_code:
                    self.in_code = False
                    # txt += "</code>"
                else:
                    self.in_code = True
                    # txt += "<code>"
                self.consume()

            # Otherwise, treat as raw text
            else:
                self.buffer += self.consume()

        return paragraph_token

    def parse_header(self) -> HeaderToken:
        header_token = HeaderToken()

        (_, n) = self.consume_while("#")
        (txt, _) = self.consume_until("\n")

        header_token.size = n
        header_token.text = txt.strip()
        return header_token

    # The 'main' tokeniser function; reads the input stream and builds tokens
    def read_stream(self):
        while self.peek() != "\0":
            curr = self.peek()
            curr_token: Token

            # Ignore leading whitespace
            if curr.isspace():
                self.consume()

            # HEADER
            elif curr == "#":
                curr_token = self.parse_header()
                print(f"{curr_token.to_html()}\n")

            # TODO: block quotes, code blocks, hrule, images, etc

            # Otherwise, parse as a rich text paragraph
            else:
                curr_token = self.parse_paragraph()
                print(f"{curr_token.to_html()}\n")
