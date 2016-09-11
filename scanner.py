import sys

reserve_word_list = ["int","void","if","while","return","read","write","print","continue","break","binary","decimal"]
symbol_list = ["(",")","{","}","[","]",",",";","+","-","*","==","!=",">=","<=","<",">","=","&&","||"]

class Token(object):
    def __init__(self):
        self.type = ""
        self.name = ""

    def get_token_type(self):
        return self.type

    def get_token_name(self):
        return self.name

    def print_token(self):
        f_write.write(self.name)

    def print_token_with_csc512(self):
        f_write.write("csc512" + self.name)

    def print_token_error(self):
        f_write.write("\n The input program contains errors for scanning and the execution will stop now!!!")


class Scanner(object):
    def __init__(self,prog_name):
        self.prog_name = prog_name
        global f_read
        f_read= open(self.prog_name,'r')
        temp_name = prog_name.split('.')
        global newprog_name
        newprog_name = " "
        newprog_name = temp_name[0] + '_gen' + '.' + temp_name[1]
        global f_write
        f_write = open(newprog_name,'a')


    def has_more_tokens(self):
        global current_ch
        current_ch = f_read.read(1)
        if current_ch != '':
            return True
        else:
            f_read.close()
            f_write.close()
            return False

    def get_next_token(self):
        global current_ch
        t = Token()
        if current_ch == '#':
            t.name = current_ch
            t.type  = "meta statement"
            while True:
              next_ch = f_read.read(1)
              if next_ch == '\n':
                  current_pos = f_read.tell()
                  current_pos -= 1
                  f_read.seek(current_pos)
                  break
              else:
                t.name += next_ch
            return t
        elif current_ch == '/':
             next_ch = f_read.read(1)
             if next_ch == '/':
               t.name = "//"
               t.type  = "meta statement"
               while True:
                 next_ch = f_read.read(1)
                 if next_ch == '\n':
                     current_pos = f_read.tell()
                     current_pos -= 1
                     f_read.seek(current_pos)
                     break
                 else:
                     t.name += next_ch
             else:
                 t.type  = "symbol"
                 t.name = '/'
                 current_pos = f_read.tell()
                 current_pos -= 1
                 f_read.seek(current_pos)
             return t
        elif current_ch == '"':
             t.name = current_ch
             t.type  = "string"
             while True:
               next_ch = f_read.read(1)
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
                next_ch = f_read.read(1)
                if not(next_ch.isalnum()):
                    current_pos = f_read.tell()
                    current_pos -= 1
                    f_read.seek(current_pos)
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
                next_ch = f_read.read(1)
                if not(next_ch.isalnum()):
                    current_pos = f_read.tell()
                    current_pos -= 1
                    f_read.seek(current_pos)
                    break
                else:
                    t.name += next_ch
            return t
        elif current_ch.isdigit():
            t.name = current_ch
            t.type = "number"
            while True:
                next_ch = f_read.read(1)
                if not(next_ch.isdigit()):
                    if(next_ch.isalpha() or next_ch == '_'):
                       t.type = "unknown"
                       t.name  = "error"
                       print('Input program contains errors for scanning and the execution will stop now!!!')
                       t.print_token_error()
                       sys.exit()
                    else:
                       current_pos = f_read.tell()
                       current_pos -= 1
                       f_read.seek(current_pos)
                       break
                else:
                    t.name += next_ch
            return t

        elif ((current_ch == '\n') or (current_ch.isspace())):
            t.type = 'delimiters'
            t.name = current_ch
            return t
        else:
              next_ch = f_read.read(1)
              for symbol in symbol_list:
                  if current_ch + next_ch == symbol:
                      t.type = "symbol"
                      t.name = symbol
                      return t
                      break
                  elif current_ch == symbol:
                      t.type = "symbol"
                      t.name = current_ch
                      current_pos = f_read.tell()
                      current_pos -= 1
                      f_read.seek(current_pos)
                      return t
                      break
              t.type = "unknown"
              t.name  = "error"
              print('Input program contains errors for scanning and the execution will stop now!!!')
              t.print_token_error()
              sys.exit()


scanner = Scanner(sys.argv[1])
while scanner.has_more_tokens():
    t = scanner.get_next_token()
    if ((t.get_token_type() == "identifier") and (t.get_token_name() != "main")):
         t.print_token_with_csc512()
    else:
        t.print_token()
