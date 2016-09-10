class Token(object):
    def __init__(self):
        self.type = ""
        self.name = ""

    def get_token_type(self):
        #print('get_token_type')
        self.type = "ID"
        #print(self.type)

    def get_token_name(self):
        #print('get_token_name')
        self.name = "name"
        #print(self.name)

class Scanner(object):
    def __init__(self,prog_name):
        self.prog_name = prog_name
        global f
        f = open(self.prog_name,'r')

    def has_more_tokens(self):
        global ch
        ch = f.read(1)
        if ch != '':
            return True
        else:
            f.close()
            return False

    def get_next_token(self):
        if ch == '\n':
            print('end of line')


scanner = Scanner("foo1.c")
while scanner.has_more_tokens():
    scanner.get_next_token()
    t = Token()
    t.get_token_name()
    t.get_token_type()
