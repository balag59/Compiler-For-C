class Token(object):
    def __init__(self):
        self.type = ""
        self.name = ""

    def get_token_type(self):
        print(self.type)
        return self.type

    def get_token_name(self):
        print(self.name)
        return self.name

class Scanner(object):
    def __init__(self,prog_name):
        self.prog_name = prog_name
        global f
        f = open(self.prog_name,'r')

    def has_more_tokens(self):
        global current_ch
        current_ch = f.read(1)
        if current_ch != '':
            return True
        else:
            f.close()
            return False

    def get_next_token(self):
        global current_ch
        t = Token()
        if current_ch == '#':
            t.name = current_ch
            t.type  = "meta"
            while True:
              next_ch = f.read(1)
              if next_ch == '\n':
                  break
              else:
                t.name += next_ch
        elif current_ch == '/':
             next_ch = f.read(1)
             if next_ch == '/':
               t.name = "//"
               t.type  = "meta"
               while True:
                 next_ch = f.read(1)
                 if next_ch == '\n':
                     t.name += next_ch
                     break
                 else:
                     t.name += next_ch
        elif current_ch == '"':
             t.name = current_ch
             t.type  = "string"
             while True:
               next_ch = f.read(1)
               if next_ch == '"':
                   t.name += next_ch
                   while True:
                       next_ch = f.read(1)
                       if next_ch == '\n':
                           break                            
                   break
               else:
                 t.name += next_ch
        return t


scanner = Scanner("foo1.c")
while scanner.has_more_tokens():
    t = scanner.get_next_token()
    t.get_token_type()
    t.get_token_name()
