from util.tokeniser import *

# Test primitive tokeniser functionality
def test_consume():
    t = Tokeniser("hello world")
    assert t.consume() == "h"

def test_eof():
    t = Tokeniser("hello world")
    t.consume_until("\0")
    t.consume()
    assert t.eof() == True

def test_consume_while():
    t = Tokeniser("***test")
    assert t.consume_while("*") == ("***", 3)
    assert t.peek() == "t"

def test_consume_until():
    t = Tokeniser("test*")
    assert t.consume_until("*") == ("test", 4)
    assert t.peek() == "*"

def test_read_stream():
    t = Tokeniser('''
## This is a header!
And this is some **bold text**...
And some *emph text*...
And ***both...***
This should not be in a new paragraph...

But this should be a new paragraph!
What if we have *****five stars?***** What happens then?

What happens if we have a **multi
line bold** text?

Simple *inline **formatting** test*...

More **advanced *case***.
Or *another **weird case***.

How does markdown handle       many spaces?

* this should be treated as regular text so far...

This one is a *tricky and m**alform*ed case...

What about *something* *with lots* of **things**
### Fake new header...

### An actual new header.

And some `inline code`.

What about **bold `inline code`?** Does that work?
                  ''')
    t.read_stream()
