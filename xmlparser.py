
class InvalidDataException(Exception):
    def __init__(self, invalid_str):
        super().__init__(invalid_str)

class Element:
    def __init__(self):
        self.header_open = False
        self.footer_open = False
        self.closed = False
        self.tag = None
        self.buf = ""
        self.keybuf = None
        self.valuebuf = None
        self.body = ""
        self.attributes = {}
        self.activeChild = None
        self.children = []
        self.escaped = False

    def push(self, char):
        if self.activeChild != None:
            self.activeChild.push(char)
            if self.activeChild.closed:
                self.children.append(self.activeChild)
                self.activeChild = None
        else:
            if self.escaped:
                self.buf += char
                self.escaped = False
            else:
                if char == "\\":
                    self.escaped = True
                elif char == "<":
                    if self.tag == None:
                        self.header_open = True
                    else:
                        if self.header_open or self.footer_open:
                            raise InvalidDataException("Attepted to open a new tag header or footer without closing the current one.")
                        else:
                            self.body += self.buf
                            self.buf = "<"
                elif char == ">":
                    if self.header_open:
                        self.header_open = False
                        if self.tag == None:
                            self.tag = self.buf
                        self.buf = ""
                    elif self.footer_open:
                        if self.buf == self.tag:
                            self.footer_open = False
                            self.closed = True
                        else:
                            raise InvalidDataException("Mismatched tag header and footer")
                elif char == "/":
                    if self.buf == "<":
                        self.footer_open = True
                        self.buf = ""
                    else:
                        self.buf += char
                elif char == " ":
                    if self.header_open:
                        if self.tag == None:
                            self.tag = self.buf
                            self.buf = ""
                    elif self.footer_open:
                        pass
                    else:
                        self.buf += char
                elif char == "=":
                    if self.header_open and self.keybuf == None:
                        self.keybuf = self.buf
                        self.buf = ""
                    else:
                        self.buf += char
                elif char == "\"":
                    if self.header_open and self.keybuf != None:
                        if len(self.buf) == 0:
                            pass
                        else:
                            self.attributes[self.keybuf] = self.buf
                            self.keybuf = None
                            self.buf = ""
                    else:
                        self.buf += char
                else:
                    if self.buf == "<":
                        self.activeChild = Element()
                        self.activeChild.push("<")
                        self.activeChild.push(char)
                    else:
                        self.buf += char
            