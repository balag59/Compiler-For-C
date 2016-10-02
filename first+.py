import sys
import itertools

P = ["expr->term expr'","expr'->+ term expr'|- term expr'|empty","term->factor term'","term'->* factor term'|/ factor term'|empty","factor->( expr )|num|name"]
T = {'+','-','*','/','name','num','(',')'}
empty = {'empty'}
eof = {'eof'}
NT = {'expr','term',"expr'","term'",'factor'}
S = 'expr'

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
      first[A] = first[A] | rhs
 if(prev_first == first):
       firstset_change = False
 prev_first = first.copy()



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

first_plus  = {}

for p in P:
        A = p.split("->")[0]
        beta = p.split("->")[1]
        beta = beta.split('|')
        for item in beta:
           b = item.split(' ')
           key = A + '->' + item
           if('empty' not in first[b[0]]):
               first_plus[key] = first[b[0]]
           else:
               first_plus[key] = first[b[0]] | follow[A]

for p in P:
        A = p.split("->")[0]
        beta = p.split("->")[1]
        beta = beta.split('|')
        if(len(beta)) > 1:
             for i, j in itertools.combinations(beta, 2):
                     k1 = A + '->' + i
                     k2 = A + '->' + j
                     if(first_plus[k1] & first_plus[k2]):
                         print('this grammar is not backtrack free')
                         exit()

print('this grammar is backtrack free')

table = {}

for nt in NT:
    for t in T:
        table[(nt,t)] = 'error'
    for p in P:
        A = p.split("->")[0]
        beta = p.split("->")[1]
        beta = beta.split('|')
        for item in beta:
            key = A + '->' + item
            for t in T:
             if t in first_plus[key]:
                 table[(A,t)] = key
             if('eof' in first_plus[key]):
                 table[(A,'eof')] = key
             else:
                table[(A,'eof')] = 'error'      

for key in table:
    print(key)
    print(table[key])
