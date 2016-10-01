import sys

P = ["expr->term expr'","expr'->+ term expr'|- term expr'|empty","term->factor term'","term'->* factor term'|/ factor term'|empty","factor->( expr )|num|name"]
T = {'+','-','*','/','name','num','(',')'}
empty = {'empty'}
eof = {'eof'}
NT = {'expr','term',"expr'","term'",'factor'}

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
      if(rhs not in first[A]):
          first[A] = first[A] | rhs
 if(prev_first == first):
       firstset_change = False
 prev_first = first.copy()

for nt in NT:
    print(nt)
    print(first[nt])
