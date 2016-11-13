import sys
import itertools

#list of Terminals in the grammar
T = {';','{','}','ID','(',')','int','void','binary','decimal',',','[',']','{','}','read','write','string','=','&&','||','==','!=','>'
     ,'>=','<','<=','while','return','break','continue','+','-','*','/','number','print','if'}

#list of Non-Terminals in the grammar
NT = {'program','data_decls','func_list','func','func_decl','func1','type_name','parameter_list','non_empty_list','non_empty_list1','id_list','id_list1','id','id1','expression','block_statements','statements','statement','assignment','func_call','if_statement','while_statement','return_statement','break_statement'\
      ,'continue_statement','expr_list','non_empty_expr_list','non_empty_expr_list1','condition_expression','condition_expression1','condition_op','condition','comparison_op','return_statement1','expression1','term','factor','term1','mulop','factor1','addop','parameter_list1','program1','program2','program3','program4','assignment1','statement1'}

#start,empty and end of file symbols
S = 'program'
empty = {'empty'}
eof = {'eof'}

#open and read the grammar file to get all the production rules
f_grammar = open('grammar.txt','r')
P = []
for line in f_grammar:
    P.append(line.strip('\n'))

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


# a scanner object to help perform scanning
class Scanner(object):
    def __init__(self,prog_name):
        self.prog_name = prog_name         #the input test program to be scanned for tokens
        self.f_read= open(self.prog_name,'r')   #file pointer to read the input test program
        self.f_line= open(self.prog_name,'r')
        self.current_ch = ''
        temp_name = prog_name.split('.')
        global newprog_name
        newprog_name = " "
        newprog_name = temp_name[0] + '_gen' + '.' + temp_name[1]


    #checks if the input test program has any more input tokens left
    def has_more_tokens(self):
        self.current_ch = self.f_read.read(1) #self.current_ch stores the value of the current character being scanner
        if self.current_ch != '':
            return True
        else:
            self.f_read.close()   #close both the input and the output files if there are no more tokens left
            return False

    #retrieves the next valid token from the input file
    def get_next_token(self):
        t = Token()
        #Now we start checking each scanned character and create its corresponding Token

        #checking for # define meta statements
        if self.current_ch == '#':
            t.name = self.current_ch        #the token attributes are being populated
            t.type  = "meta statement"
            while True:
              next_ch = self.f_read.read(1)  #next_ch contains the next scanned character after the current character
              if next_ch == '\n':
                  current_pos = self.f_read.tell()
                  current_pos -= 1
                  self.f_read.seek(current_pos)
                  break
              else:
                t.name += next_ch
            return t

        #checking for //meta statements and the / operator
        elif self.current_ch == '/':
             next_ch = self.f_read.read(1)
             if next_ch == '/':        # if 2 consecutive // are found then its a meta statement
               t.name = "//"
               t.type  = "meta statement"
               while True:
                 next_ch = self.f_read.read(1)
                 if next_ch == '\n':
                     current_pos = self.f_read.tell()
                     current_pos -= 1
                     self.f_read.seek(current_pos)
                     break
                 else:
                     t.name += next_ch
             else:
                 t.type  = "symbol"       #if only a single / is found then its just a symbol
                 t.name = '/'
                 current_pos = self.f_read.tell()
                 current_pos -= 1
                 self.f_read.seek(current_pos)
             return t

        #checking for strings starting and ending with ""
        elif self.current_ch == '"':
             t.name = self.current_ch
             t.type  = "string"
             while True:
               next_ch = self.f_read.read(1)
               if next_ch == '"':
                   t.name += next_ch
                   break
               else:
                 t.name += next_ch
             return t

        #checking for identifiers that start with an alphabet and keywords
        elif self.current_ch.isalpha():
            t.name = self.current_ch
            t.type = "ID"
            while True:
                next_ch = self.f_read.read(1)
                if not(next_ch.isalnum() or next_ch == '_'):
                    current_pos = self.f_read.tell()
                    current_pos -= 1
                    self.f_read.seek(current_pos)
                    break
                else:
                    t.name += next_ch
            for w in reserve_word_list:
                if t.name == w:            #if the set of alphabets matches a valid reserved keyword
                    t.type = "reserved word"
            return t

        #checking for identifiers that start with an _
        elif self.current_ch == '_':
            t.name = self.current_ch
            t.type = "ID"
            while True:
                next_ch = self.f_read.read(1)
                if not(next_ch.isalnum() or next_ch == '_'):
                    current_pos = self.f_read.tell()
                    current_pos -= 1
                    self.f_read.seek(current_pos)
                    break
                else:
                    t.name += next_ch
            return t

        #checking for numbers
        elif self.current_ch.isdigit():
            t.name = self.current_ch
            t.type = "number"
            while True:
                next_ch = self.f_read.read(1)
                if not(next_ch.isdigit()):
                       current_pos = self.f_read.tell()
                       current_pos -= 1
                       self.f_read.seek(current_pos)
                       break
                else:
                    t.name += next_ch
            return t

        #checking for end of line or space characters
        elif ((self.current_ch == '\n') or (self.current_ch.isspace())):
            t.type = "delimiters"
            t.name = self.current_ch
            return t

        #checking the remaining possibilities i.e. it's either a symbol or an illegal token
        else:
              next_ch = self.f_read.read(1)
              for symbol in symbol_list:
                  if self.current_ch + next_ch == symbol:   #checks for symbols with 2 characters like && == >= etc
                      t.type = "symbol"
                      t.name = symbol
                      return t
                      break
                  elif self.current_ch == symbol:           #checks for symbols with one character like ( } ; etc
                      t.type = "symbol"
                      t.name = self.current_ch
                      current_pos = self.f_read.tell()
                      current_pos -= 1
                      self.f_read.seek(current_pos)
                      return t
                      break
              # if no valid token can be formed then report an error while scanning and quit the program
              t.type = "unknown"
              t.name  = "error"
              #print error message to terminal
              print('Error in Scanner:Invalid token in source file')
              exit()

#create a new scanner
scanner_LL = Scanner(sys.argv[1])
scanner_LR = Scanner('tempfile.txt')


#get the next word from the input program through the scanner
def NextWord(scanner):
    if scanner.has_more_tokens():           #while there are any more tokens left in the input test program
        t = scanner.get_next_token()           #fetch the next valid token
        #print(t.get_token_name())
        if (t.get_token_type() == "ID" or t.get_token_type() == "number" or t.get_token_type() == "string"):
             return t.get_token_type()
        elif(t.get_token_type() == "meta statement" or t.get_token_type() == "delimiters"):
             return 'error'
        elif (t.get_token_type() == "reserved word" or t.get_token_type() == "symbol"):
             return t.get_token_name()
        else:
            return 'error'
    else:
         return 'eof'

line_begin = []
printed_pos = []
num_lines = 0
prev_pos = -1

for line in scanner_LL.f_line:
    num_lines += 1

scanner_LL.f_line.seek(0)

for i in range(num_lines):
  line_begin.append(scanner_LL.f_line.tell())
  scanner_LL.f_line.readline()

def PrintLine():
 if not(scanner_LL.f_read.closed):
  temp_pos = scanner_LL.f_read.tell()
  seek_pos = scanner_LL.f_read.tell()
  for pos in line_begin:
      if(temp_pos < pos):
          temp_pos = prev_pos
          break
      prev_pos = pos
  if(prev_pos not in printed_pos):
     scanner_LL.f_read.seek(prev_pos)
     line = scanner_LL.f_read.readline()
     BottomUpParse(line)
     printed_pos.append(prev_pos)
     scanner_LL.f_read.seek(seek_pos)

def BottomUpParse(line):
    f_LR = open('tempfile.txt','w+')
    f_LR.write(line)
    LR_stack = []
    LR_stack.append('eof')
    LR_stack.append('s0')




#computing first sets for all the symbols in the grammar
first = {}
prev_first = {}

for t in (T | empty | eof):
    first[t] = {t}

for nt in NT:
    first[nt] = set()

firstset_change = True

while(firstset_change):
 for p in P:
   A = p.split("->")[0]
   beta = p.split("->")[1]
   if(beta.count("||") >=1):
     beta = beta.split('|',maxsplit=1)
   else:
     beta = beta.split('|')
   rhs = set()
   for b in beta:
      b = b.split(' ')
      k = len(b) - 1
      rhs  = first[b[0]] - empty
      i = 0
      while('empty' in first[b[i]] and i<= k - 1 ):
          rhs = rhs | (first[b[i+1]] - empty)
          i += 1
      if(i == k and 'empty' in first[b[k]]):
          rhs = rhs | empty
      first[A] = first[A] | rhs
 if(prev_first == first):
       firstset_change = False
 prev_first = first.copy()


#computing follow sets for all the symbols in the grammar
follow = {}
prev_follow = {}

for nt in NT:
    follow[nt] = set()

follow[S] = follow[S] | eof

followset_change = True

while(followset_change):
 for p in P:
        A = p.split("->")[0]
        beta = p.split("->")[1]
        if(beta.count("||") >=1):
          beta = beta.split('|',maxsplit=1)
        else:
          beta = beta.split('|')
        trailer = set()
        for b in beta:
           b = b.split(' ')
           k = len(b) - 1
           trailer = follow[A]
           for i in range(k,-1,-1):
               if(b[i] in NT):
                   follow[b[i]] = follow[b[i]] | trailer
                   if('empty' in first[b[i]]):
                       trailer = trailer | (first[b[i]] - empty)
                   else:
                       trailer = first[b[i]]
               else:
                   trailer = first[b[i]]
 if(prev_follow == follow):
      followset_change = False
 prev_follow = follow.copy()

#computing First+ sets using the first and follow sets
first_plus  = {}

for p in P:
        A = p.split("->")[0]
        beta = p.split("->")[1]
        if(beta.count("||") >=1):
          beta = beta.split('|',maxsplit=1)
        else:
          beta = beta.split('|')
        for item in beta:
           b = item.split(' ')
           key = A + '->' + item
           if('empty' not in first[b[0]]):
               first_plus[key] = first[b[0]]
           else:
               first_plus[key] = first[b[0]] | follow[A]

#checking for LL(1) grammar condition using First+ sets
for p in P:
        A = p.split("->")[0]
        beta = p.split("->")[1]
        if(beta.count("||") >=1):
          beta = beta.split('|',maxsplit=1)
        else:
          beta = beta.split('|')
        if(len(beta)) > 1:
             for i, j in itertools.combinations(beta, 2):
                     k1 = A + '->' + i
                     k2 = A + '->' + j
                     if(first_plus[k1] & first_plus[k2]):
                         print('this grammar is not LL(1)')
                         exit()

#creating the LL(1) parser table using the First+ sets
table = {}

for nt in NT:
    for t in T:
        table[(nt,t)] = 'error'
    for p in P:
        A = p.split("->")[0]
        beta = p.split("->")[1]
        if(beta.count("||") >=1):
          beta = beta.split('|',maxsplit=1)
        else:
          beta = beta.split('|')
        for item in beta:
            key = A + '->' + item
            for t in T:
             if t in first_plus[key]:
                 table[(A,t)] = key
             if('eof' in first_plus[key]):
                 table[(A,'eof')] = key


#creating a table driven LL(1) parser using LL(1) table and the next input token from the scanner
stack = []
word = NextWord(scanner_LL)
while(word == 'error'):
    word = NextWord(scanner_LL)
stack.append('eof')
stack.append(S)
while(True):
    if(stack[-1] == 'eof' and word == 'eof'):
        #print('pass variable' , num_variables ,'function' , num_functions , 'statement' , num_statements)
        exit()
    elif(stack[-1] in T or stack[-1] == 'eof'):
        if(stack[-1] == word):
            stack.pop()
            word = NextWord(scanner_LL)
            while(word == 'error'):
                word = NextWord(scanner_LL)
        else:
            print('error looking for symbol at top of the stack')
            exit()
    else:

        if(table[(stack[-1],word)] != 'error'):
            #print(table[(stack[-1],word)])
            if(stack[-1] == 'statement'):
                PrintLine()
            prod = table[(stack[-1],word)].split('->')
            beta = prod[1].split(' ')
            beta.reverse()
            stack.pop()
            for b in beta:
                if(b != 'empty'):
                   stack.append(b)

        else:
            print('fail:error parsing the program')
            exit()
