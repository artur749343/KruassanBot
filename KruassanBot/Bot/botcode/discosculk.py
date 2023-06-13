import asyncio, time, copy, json, os
from discofunc import dir_fun, this
import discord
from discord.guild import Guild
from discord.channel import CategoryChannel, VoiceChannel, TextChannel
from discord.message import Message
dir={}

# dir_fun={"print": print}



def arrays(code: str): #str to array
   code=code.replace(" ", "")
   i,t,d=0,[],0
   while i<len(code):
      if code[i]==",":
         t.append(code[:i])
         code, i=code[i+1:], 0
      if code[i]=="[":
         d+=1
         while d!=0:
            i+=1
            if code[i]=="[":d+=1
            if code[i]=="]":d-=1
      if code[i]=="(":
         d+=1
         while d!=0:
            i+=1
            if code[i]=="(":d+=1
            if code[i]==")":d-=1
      i+=1
   t.append(code)
   if len(t)<2:
      if t[0][0] in "([" and t[0][-1] in "])":
         if len(arrays(t[0][1:-1]))>1:
            return arrays(t[0][1:-1])
         else:
            return [arrays(t[0][1:-1])]
      else:
         return CodeToTokens(t[0])
   return [arrays(x) for x in t]


async def whil(n1, row): #while
   x=[await Interpretator(tok, row) for tok in copy.deepcopy(n1[:-1])][1]
   while x:
         w=True
         for q in name.split("\n")[row+1:]:
            if CodeToTokens(q)[0]!=" ": w=False
            if w: await Interpretator(CodeToTokens(q)[1:], row)
         x=[await Interpretator(tok, row) for tok in copy.deepcopy(n1[1:])][0]

def oper(a, oper, b): #operations +, -
   if type(a) in [tuple, list] and oper!="=" and a[0] in dir.keys(): a, aArg=dir[a[0]], a[0]
   if type(b) in [tuple, list] and b[0] in dir.keys(): b=dir[b[0]]
   if oper=="+": return a+b
   elif oper=="-": return a-b
   elif oper=="*": return a*b
   elif oper=="/": return a/b
   elif oper=="^": return a**b
   elif oper=="=": dir.update({a[0]: b})
   elif oper=="==": return a==b
   elif oper=="!=": return a!=b
   elif oper=="<=": return a<=b
   elif oper==">=": return a>=b
   elif oper=="<": return a<b
   elif oper==">": return a>b
   elif oper=="+=": dir[aArg]+=b
   elif oper=="-=": dir[aArg]-=b
   elif oper=="*=": dir[aArg]*=b
   elif oper=="/=": dir[aArg]/=b

def Typizing(value, type): #str to type int or float
   if type=="int": return int(value)


def CodeToTokens(code: str): #code to tokens
   tokens, i=[], 0
   if code=="":
      return [None]
   while i<len(code):
         token, isarg="", True
         if code[i].isdigit(): #numbers
            while i<len(code) and code[i].isdigit():
               token+=code[i]
               i+=1
            i-=1
            tokens.append(Typizing(token, "int"))
         elif code[i:i+6]=="while ":
            i+=6
            while i<len(code) and code[i]!=":":
               token+=code[i]
               i+=1
            tokens.append("while")
            tokens.append([CodeToTokens(t) for t in token.split(", ")])
         elif code[i:i+4]=="this":
            i+=4
            if i>=len(code) or code[i]==".":
               while i<len(code) and code[i] not in "+-*/^=!<> ":
                  token+=code[i]
                  i+=1
               tokens.append(("this",)+tuple(token.split(".")[1:]))
         elif code[i] in [" "]:
            tokens.append(" ")
         elif code[i:i+2] in ["!=", "==", "+=", "-=", "*=", "/=", "<=", ">=", "++"]: #operation doubled
               tokens.append(code[i:i+2])
               i+=1
         elif code[i] in ["+", "-", "*", "/", "^", "=", "<", ">"]: #operation
               tokens.append(code[i])
         elif code[i]=='"' or code[i]=="'": #str
            i+=1
            while code[i]!="'" and code[i]!='"':
               token+=code[i]
               i+=1
            tokens.append(token)
         else: #args
            x=""
            while not (i>=len(code) or code[i] in "()[]<>+-=!"):
               x+=code[i]
               i+=1
            if i<len(code) and code[i]=="(":
               tokens.append((x, "func", (arrays(code[i:]), "tree")))
               return tokens
            elif i<len(code) and code[i]=="[":
               tokens.append((arrays(code[i:]), "tree"))
               return tokens
            else:
               tokens.append((x, "args"))
            i-=1
         i+=1
   return tokens

async def Interpretator(tokens, row):
   p=0
   if type(tokens[0]) in [list, tuple] and tokens[0][0]=="this": #this like in C
      return this(tokens[0])
   if type(tokens) not in [tuple, list]:
      return tokens
   if tokens[0]=="list": #interpretate array
      return [await Interpretator(q1, row) for q1 in tokens[1]]
   if len(tokens)<2:
      if type(tokens[0])!=tuple: return tokens[0]
      elif type(tokens[0])==tuple and tokens[0][1]=="args": return dir[tokens[0][0]] #get argument from cash
      elif type(tokens[0])==tuple and tokens[0][1]=="func": return await dir_fun[tokens[0][0]](*await treedeform(tokens[0][2][0], row)) #activate function
   if tokens[0]=="while":
      await whil(tokens[1], row)
      del tokens[0]
      del tokens[0]
   while 1<len(tokens):
      for n in [["*","/","^"], ["+","-"], ["=", "!=", "==", "+=", "-=", "*=", "/=", "<=", ">=", ">", "<"]]:
         while p<len(tokens):
            if tokens[p] in n:
               tokens[p]=oper(*tokens[p-1:p+2])
               del tokens[p-1]
               del tokens[p]
               p-=2
            elif tokens[p]==" ":
               del tokens[p]
            elif tokens[p]=="++":
               dir[tokens[p-1][0]]+=1
               del tokens[p]
            p+=1
         p=0
   row+=1
   if len(tokens)==1:
      return tokens[0]
   elif len(tokens)==0:
      return
   else:
      return tokens


async def treedeform(tree, row):
   if type(tree[0])==list:
      return [await treedeform(x, row) for x in tree]
   else:
      return await Interpretator(tree, row)

async def DiscoSculk(file: str, interpretate:bool=True): #activate
   global name
   name=open("\\".join(str(os.path.abspath(__file__)).split("\\")[:-2])+f"\\data\\discofiles\\{file}.txt", "r").read()
   for i, x in enumerate(name.split("\n")):
      if interpretate:await Interpretator(CodeToTokens(x), i)
      else:print(CodeToTokens(x))


if __name__=="__main__":
   start=time.time()
   asyncio.run(DiscoSculk("файл1", False))
   print(time.time()-start) #timer for tests