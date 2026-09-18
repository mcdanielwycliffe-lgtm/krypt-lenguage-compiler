from dataclasses import dataclass
from .lexer import Lexer, Token

@dataclass
class Program: statements:list
@dataclass
class Import: name:str
@dataclass
class ImportFile: path:str
@dataclass
class Block: statements:list
@dataclass
class Var: name:str; expr:object
@dataclass
class Assign: name:str; expr:object
@dataclass
class ExprStmt: expr:object
@dataclass
class If: cond:object; then:Block; otherwise:object
@dataclass
class While: cond:object; body:Block
@dataclass
class Fun: name:str; params:list; body:Block
@dataclass
class Return: expr:object
@dataclass
class Literal: value:object
@dataclass
class Name: value:str
@dataclass
class Unary: op:str; expr:object
@dataclass
class Binary: left:object; op:str; right:object
@dataclass
class Call: callee:object; args:list
@dataclass
class Member: obj:object; name:str
@dataclass
class ListExpr: items:list

class ParserError(Exception): pass
class Parser:
    def __init__(self, source): self.ts=Lexer(source).tokenize(); self.i=0
    def cur(self): return self.ts[self.i]
    def at(self,k): return self.cur().kind==k
    def take(self,k):
        if not self.at(k): raise ParserError(f"Esperado {k}, encontrado {self.cur().kind} na linha {self.cur().line}")
        t=self.cur(); self.i+=1; return t
    def match(self,k):
        if self.at(k): self.i+=1; return True
        return False
    def parse(self):
        ss=[]
        while not self.at('EOF'): ss.append(self.statement())
        return Program(ss)
    def statement(self):
        if self.match('import'):
            if self.match('<'):
                name=self.take('IDENT').value; self.take('>'); self.match(';'); return Import(name)
            if self.at('STRING'):
                path=self.take('STRING').value
            else:
                parts=[self.take('IDENT').value]
                while self.match('.'):
                    parts.extend(['.',self.take('IDENT').value])
                path=''.join(parts)
            self.match(';'); return ImportFile(path)
        if self.match('var'):
            n=self.take('IDENT').value; self.take('='); e=self.expr(); self.take(';'); return Var(n,e)
        if self.match('fun'):
            n=self.take('IDENT').value; self.take('('); ps=[]
            if not self.at(')'):
                while True:
                    ps.append(self.take('IDENT').value)
                    if not self.match(','): break
            self.take(')'); return Fun(n,ps,self.block())
        if self.match('if'):
            c=self.expr(); t=self.block(); o=self.block() if self.match('else') else None; return If(c,t,o)
        if self.match('while'): return While(self.expr(),self.block())
        if self.match('return'):
            e=Literal(None) if self.at(';') else self.expr(); self.take(';'); return Return(e)
        if self.at('{'): return self.block()
        if self.at('IDENT') and self.ts[self.i+1].kind=='=':
            n=self.take('IDENT').value; self.take('='); e=self.expr(); self.take(';'); return Assign(n,e)
        e=self.expr(); self.take(';'); return ExprStmt(e)
    def block(self):
        self.take('{'); ss=[]
        while not self.at('}'):
            if self.at('EOF'): raise ParserError('Bloco não terminado')
            ss.append(self.statement())
        self.take('}'); return Block(ss)
    PRE={'or':1,'||':1,'and':2,'&&':2,'==':3,'!=':3,'<':4,'>':4,'<=':4,'>=':4,'+':5,'-':5,'*':6,'/':6,'%':6}
    def expr(self,minp=0):
        t=self.cur()
        if self.match('!') or self.match('not') or self.match('-'):
            left=Unary(t.kind,self.expr(7))
        elif self.match('NUMBER') or self.match('STRING'): left=Literal(t.value)
        elif self.match('true'): left=Literal(True)
        elif self.match('false'): left=Literal(False)
        elif self.match('null'): left=Literal(None)
        elif self.match('IDENT'): left=Name(t.value)
        elif self.match('('): left=self.expr(); self.take(')')
        elif self.match('['):
            items=[]
            if not self.at(']'):
                while True:
                    items.append(self.expr())
                    if not self.match(','): break
            self.take(']'); left=ListExpr(items)
        else: raise ParserError(f"Expressão inválida na linha {t.line}")
        while True:
            if self.match('.'):
                member=self.cur()
                if member.kind not in ('IDENT','and','or','not'):
                    raise ParserError(f"Membro inválido após ponto na linha {member.line}")
                self.i+=1; left=Member(left,member.value); continue
            if self.match('('):
                args=[]
                if not self.at(')'):
                    while True:
                        args.append(self.expr())
                        if not self.match(','): break
                self.take(')'); left=Call(left,args); continue
            op=self.cur().kind; p=self.PRE.get(op,-1)
            if p<minp: break
            self.i+=1; left=Binary(left,op,self.expr(p+1))
        return left
