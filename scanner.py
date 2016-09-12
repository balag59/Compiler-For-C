import sys

#list of valid reserved keywords supported
reserve_word_list = ["int","void","if","while","return","read","write","print","continue","break","binary","decimal"]

#list of all valid symbols supported(except / as its checked seperately)
symbol_list = ["(",")","{","}","[","]",",",";","+","-","*","==","!=",">=","<=","<",">","=","&&","||"]

# a Token class that stores each token as a token object
class Token(object):
    def __init__(self):
        self.type = "" #each token has a type and a name
        self.name = ""

    #returns the token type
    def get_token_type(self):
        return self.type

    #returns the token name
    def get_token_name(self):
        return self.name

    #prints non identifer and main identifier tokens to the output file
    def print_token(self):
        f_write.write(self.name)

    #prints all identifer tokens except main with cs512 attached
    def print_token_with_csc512(self):
        f_write.write("cs512" + self.name)

    #prints an error message to the output file if any errors are encountered while scanning
    def print_token_error(self):
        f_write.write("\n The input program contains errors for scanning and the execution will stop now!!!")

# a scanner object to help perform scanning
class Scanner(object):
    def __init__(self,prog_name):
        self.prog_name = prog_name         #the input test program to be scanned for tokens
        global f_read
        f_read= open(self.prog_name,'r')   #file pointer to read the input test program
        temp_name = prog_name.split('.')
        global newprog_name
        newprog_name = " "
        newprog_name = temp_name[0] + '_gen' + '.' + temp_name[1]
        global f_write
        f_write = open(newprog_name,'a')   #file pointer to write to the generated output program

    #checks if the input test program has any more input tokens left
    def has_more_tokens(self):
        global current_ch
        current_ch = f_read.read(1) #current_ch stores the value of the current character being scanned
        if current_ch != '':
            return True
        else:
            f_read.close()   #close both the input and the output files if there are no more tokens left
            f_write.close()
            return False

    #retrieves the next valid token from the input file
    def get_next_token(self):
        global current_ch
        t = Token()
        #Now we start checking each scanned character and create its corresponding Token

        #checking for # define meta statements
        if current_ch == '#':
            t.name = current_ch        #the token attributes are being populated
            t.type  = "meta statement"
            while True:
              next_ch = f_read.read(1)  #next_ch contains the next scanned character after the current character
              if next_ch == '\n':
                  current_pos = f_read.tell()
                  current_pos -= 1
                  f_read.seek(current_pos)
                  break
              else:
                t.name += next_ch
            return t

        #checking for //meta statements and the / operator
        elif current_ch == '/':
             next_ch = f_read.read(1)
             if next_ch == '/':        # if 2 consecutive // are found then its a meta statement
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
                 t.type  = "symbol"       #if only a single / is found then its just a symbol
                 t.name = '/'
                 current_pos = f_read.tell()
                 current_pos -= 1
                 f_read.seek(current_pos)
             return t

        #checking for strings starting and ending with ""
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

        #checking for identifiers that start with an alphabet and keywords
        elif current_ch.isalpha():
            t.name = current_ch
            t.type = "identifier"
            while True:
                next_ch = f_read.read(1)
                if not(next_ch.isalnum() or next_ch == '_'):
                    current_pos = f_read.tell()
                    current_pos -= 1
                    f_read.seek(current_pos)
                    break
                else:
                    t.name += next_ch
            for word in reserve_word_list:
                if t.name == word:            #if the set of alphabets matches a valid reserved keyword
                    t.type = "reserved word"
            return t

        #checking for identifiers that start with an _
        elif current_ch == '_':
            t.name = current_ch
            t.type = "identifier"
            while True:
                next_ch = f_read.read(1)
                if not(next_ch.isalnum() or next_ch == '_'):
                    current_pos = f_read.tell()
                    current_pos -= 1
                    f_read.seek(current_pos)
                    break
                else:
                    t.name += next_ch
            return t

        #checking for numbers
        elif current_ch.isdigit():
            t.name = current_ch
            t.type = "number"
            while True:
                next_ch = f_read.read(1)
                if not(next_ch.isdigit()):
                       current_pos = f_read.tell()
                       current_pos -= 1
                       f_read.seek(current_pos)
                       break
                else:
                    t.name += next_ch
            return t

        #checking for end of line or space characters
        elif ((current_ch == '\n') or (current_ch.isspace())):
            t.type = 'delimiters'
            t.name = current_ch
            return t

        #checking the remaining possibilities i.e. it's either a symbol or an illegal token
        else:
              next_ch = f_read.read(1)
              for symbol in symbol_list:
                  if current_ch + next_ch == symbol:   #checks for symbols with 2 characters like && == >= etc
                      t.type = "symbol"
                      t.name = symbol
                      return t
                      break
                  elif current_ch == symbol:           #checks for symbols with one character like ( } ; etc
                      t.type = "symbol"
                      t.name = current_ch
                      current_pos = f_read.tell()
                      current_pos -= 1
                      f_read.seek(current_pos)
                      return t
                      break
              # if no valid token can be formed then report an error while scanning and quit the program
              t.type = "unknown"
              t.name  = "error"
              #print error message to terminal
              print('Input program contains errors for scanning and the execution will stop now!!!')
              t.print_token_error()
              sys.exit()

#recommended interface
scanner = Scanner(sys.argv[1])             #initialze the scanner with the input test program
while scanner.has_more_tokens():           #while there are any more tokens left in the input test program
    t = scanner.get_next_token()           #fetch the next valid token
    if ((t.get_token_type() == "identifier") and (t.get_token_name() != "main")):
         t.print_token_with_csc512()       # adding cs512 to all identifiers except main and printing to output file
    else:
        t.print_token()                    #printing all other valid token to the output file
