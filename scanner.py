reserve_word_list = ["int","void","if","while","return","read","write","print","continue","break","binary","decimal"]
symbol_list = ["(",")","{","}","[","]",",",";","+","-","*","==","!=",">",">=","<","<=","=","&&","||"]

class Token(object):
    def __init__(self):
        self.type = ""
        self.name = ""

    def get_token_type(self):
        if self.type != "delimiters":
           print(self.type)
        return self.type

    def get_token_name(self):
        if self.type != "delimiters":
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
            t.type  = "meta statement"
            while True:
              next_ch = f.read(1)
              if next_ch == '\n':
                  current_pos = f.tell()
                  current_pos -= 1
                  f.seek(current_pos)
                  break
              else:
                t.name += next_ch
            return t
        elif current_ch == '/':
             next_ch = f.read(1)
             if next_ch == '/':
               t.name = "//"
               t.type  = "meta statement"
               while True:
                 next_ch = f.read(1)
                 if next_ch == '\n':
                     current_pos = f.tell()
                     current_pos -= 1
                     f.seek(current_pos)
                     break
                 else:
                     t.name += next_ch
             else:
                 t.type  = "symbol"
                 t.name = '/'
                 current_pos = f.tell()
                 current_pos -= 1
                 f.seek(current_pos)
             return t
        elif current_ch == '"':
             t.name = current_ch
             t.type  = "string"
             while True:
               next_ch = f.read(1)
               if next_ch == '"':
                   t.name += next_ch
                   break
               else:
                 t.name += next_ch
             return t
        elif current_ch.isalpha():
            t.name = current_ch
            t.type = "identifier"
            while True:
                next_ch = f.read(1)
                if not(next_ch.isalnum()):
                    current_pos = f.tell()
                    current_pos -= 1
                    f.seek(current_pos)
                    break
                else:
                    t.name += next_ch
            for word in reserve_word_list:
                if t.name == word:
                    t.type = "reserved word"
            return t
        elif current_ch == '_':
            t.name = current_ch
            t.type = "identifier"
            while True:
                next_ch = f.read(1)
                if not(next_ch.isalnum()):
                    current_pos = f.tell()
                    current_pos -= 1
                    f.seek(current_pos)
                    break
                else:
                    t.name += next_ch
            return t
        elif ((current_ch == '\n') or (current_ch.isspace())):
            t.type = 'delimiters'
            t.name = current_ch
            return t
        else:
              for symbol in symbol_list:
                  if current_ch == symbol:
                      t.name = current_ch
                      t.type = "symbol"
                      next_ch = f.read(1)
                      for sym in symbol_list:
                          if(current_ch + next_ch == sym):
                              t.name = sym
                      return t
                      break
              t.type = "unknown"
              t.name  = "error"
              return t

scanner = Scanner("foo1.c")
while scanner.has_more_tokens():
    t = scanner.get_next_token()
    t.get_token_type()
    t.get_token_name()
