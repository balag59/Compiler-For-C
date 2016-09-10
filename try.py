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

    def has_more_tokens(self):
        if f.readline() != '':
            print('true')
            return True
        else:
            print('false')
            return False

    def get_next_token(self):
        #print('get_next_token')


scanner = Scanner("foo.c")
f = open(scanner.prog_name,'r')
while scanner.has_more_tokens():
    scanner.get_next_token()
    t = Token()
    t.get_token_name()
    t.get_token_type()
