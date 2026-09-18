import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parents[1]))
from krypt.lexer import Lexer
from krypt.parser import Parser
from krypt.runtime import run_source

def test_lexer():
    kinds=[t.kind for t in Lexer('var x = 2 + 3;').tokenize()]
    assert kinds[:5]==['var','IDENT','=','NUMBER','+']

def test_parser_and_runtime(capsys):
    run_source('var x = 2 + 3; print(x);')
    assert capsys.readouterr().out.strip()=='5'

def test_function(capsys):
    run_source('fun add(a,b) { return a+b; } print(add(4,5));')
    assert capsys.readouterr().out.strip()=='9'

def test_condition(capsys):
    run_source('if (true) { print("yes"); } else { print("no"); }')
    assert capsys.readouterr().out.strip()=='yes'
