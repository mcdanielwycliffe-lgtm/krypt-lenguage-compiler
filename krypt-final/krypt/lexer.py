from dataclasses import dataclass
from typing import Any

@dataclass
class Token:
    kind: str
    value: Any
    line: int
    column: int

class LexerError(Exception): pass

class Lexer:
    KEYWORDS = {"import", "var", "fun", "if", "else", "while", "return", "true", "false", "null", "and", "or", "not"}
    def __init__(self, source: str):
        self.source, self.i, self.line, self.col = source, 0, 1, 1
    def tokenize(self):
        out=[]
        while self.i < len(self.source):
            c=self.source[self.i]
            if c in ' \t\r': self.i+=1; self.col+=1; continue
            if c=='\n': self.i+=1; self.line+=1; self.col=1; continue
            if self.source.startswith('//', self.i):
                while self.i<len(self.source) and self.source[self.i]!='\n': self.i+=1
                continue
            line,col=self.line,self.col
            if c=='"' or c=="'": out.append(self._string(c,line,col)); continue
            if c.isdigit(): out.append(self._number(line,col)); continue
            if c.isalpha() or c=='_':
                start=self.i
                while self.i<len(self.source) and (self.source[self.i].isalnum() or self.source[self.i]=='_'): self.i+=1; self.col+=1
                word=self.source[start:self.i]; out.append(Token(word if word in self.KEYWORDS else 'IDENT',word,line,col)); continue
            two=self.source[self.i:self.i+2]
            if two in ('==','!=','<=','>=','&&','||'):
                out.append(Token(two,two,line,col)); self.i+=2; self.col+=2; continue
            if c in '{}()[],;.+-*/%=<>!': out.append(Token(c,c,line,col)); self.i+=1; self.col+=1; continue
            raise LexerError(f"Caractere inesperado {c!r} na linha {line}, coluna {col}")
        out.append(Token('EOF','',self.line,self.col)); return out
    def _string(self, quote,line,col):
        self.i+=1; self.col+=1; chars=[]
        while self.i<len(self.source) and self.source[self.i]!=quote:
            if self.source[self.i]=='\\' and self.i+1<len(self.source):
                self.i+=1; self.col+=1; chars.append({'n':'\n','t':'\t','r':'\r'}.get(self.source[self.i],self.source[self.i]))
            else: chars.append(self.source[self.i])
            self.i+=1; self.col+=1
        if self.i>=len(self.source): raise LexerError(f"String não terminada na linha {line}")
        self.i+=1; self.col+=1; return Token('STRING',''.join(chars),line,col)
    def _number(self,line,col):
        start=self.i
        while self.i<len(self.source) and self.source[self.i].isdigit(): self.i+=1; self.col+=1
        if self.i<len(self.source) and self.source[self.i]=='.':
            self.i+=1; self.col+=1
            while self.i<len(self.source) and self.source[self.i].isdigit(): self.i+=1; self.col+=1
            return Token('NUMBER',float(self.source[start:self.i]),line,col)
        return Token('NUMBER',int(self.source[start:self.i]),line,col)
