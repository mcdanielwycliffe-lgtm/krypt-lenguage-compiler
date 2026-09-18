# Krypt

Krypt é uma linguagem de programação pequena, em português/inglês neutro, criada para experimentos com automação e interfaces gráficas. O compilador é escrito em Python e transforma o código Krypt em um launcher Python executável. O runtime possui uma VM simples baseada em AST.

## Requisitos

- Python 3.10+
- Tkinter (normalmente incluído no Python; no Linux pode exigir `sudo apt install python3-tk`)
- PyInstaller para gerar `.exe`: `python -m pip install pyinstaller`

## Usando o compilador

No diretório do projeto:

```bash
python kryptc.py -File examples/hello.krypt
python kryptc.py --version
python kryptc.py run examples/hello.krypt
python kryptc.py compile examples/hello.krypt -o build/hello.py
```

O comando equivalente depois de gerar o compilador no Windows é:

```text
krypt.exe -File "arquivo.krypt"
```

Para gerar o próprio compilador, abra um Prompt de Comando neste diretório e execute `build_windows.bat`. Isso cria `dist\\krypt.exe`. O arquivo `krypt.exe` é o compilador/runtime da linguagem; ele lê o `.krypt` indicado por `-File` e executa o programa. PyInstaller não faz cross-compilation, portanto o `.exe` deve ser gerado em Windows.

## Sintaxe

```krypt
import <window>
import <iolib>

var nome = "Krypt";
fun saudacao(pessoa) {
    print("Olá", pessoa);
}
if (nome == "Krypt") { saudacao(nome); }
```

Incluídos: variáveis, funções, `if/else`, `while`, `return`, listas, operadores aritméticos/comparativos/lógicos, comentários com `//` e chamadas de membros com ponto.

## Bibliotecas próprias

`window` oferece `create(titulo, largura, altura)`, `set_background(cor)`, `text(valor, x, y, tamanho, cor)`, `show()` e `close()`.

`iolib` oferece `on_key(tecla, callback)`, `on_click(callback)`, `track_key(tecla)`, `key(tecla)` e `input(prompt)`. Eventos chamam funções Krypt, por exemplo `fun pressed(key) { print(key); }`. Depois de `track_key("Left")`, `key("Left")` retorna o estado atual da tecla.

## Arquitetura

1. `lexer.py` converte caracteres em tokens.
2. `parser.py` valida a gramática e cria uma AST.
3. `runtime.py` executa a AST e fornece as bibliotecas nativas.
4. `kryptc.py` é a CLI: executa, gera Python intermediário e chama PyInstaller.

## Licença

Projeto educacional; use e adapte livremente.

## Desenho na biblioteca `window`

A Krypt usa nomes próprios para seus elementos gráficos. As funções retornam um objeto visual que pode ser guardado em uma variável e alterado depois.

### Segmentos

```krypt
var linha = window.segment(20, 30, 300, 30, "cyan", 4);
linha.set_color("yellow");
linha.set_width(6);
linha.move(10, 20);
```

A assinatura é:

```text
window.segment(x1, y1, x2, y2, cor, espessura)
```

### Painéis retangulares

```krypt
var caixa = window.panel(50, 80, 220, 100, "#2563eb", "white", 3);
caixa.set_position(80, 100);
caixa.set_size(300, 120);
caixa.set_color("#22c55e");
```

A assinatura é:

```text
window.panel(x, y, largura, altura, cor, contorno, espessura)
```

### Elipses

```krypt
var bola = window.ellipse(100, 100, 80, 80, "red", "white", 2);
bola.move(30, 10);
bola.set_size(120, 90);
```

A assinatura é:

```text
window.ellipse(x, y, largura, altura, cor, contorno, espessura)
```

### Texto como objeto

```krypt
var titulo = window.text("KRYPT", 30, 30, 30, "white");
titulo.set_position(60, 40);
titulo.set_color("cyan");
titulo.set_font_size(38);
```

### Operações comuns dos objetos

| Operação | Efeito |
|---|---|
| `set_position(x, y)` | Define a posição inicial/superior esquerda |
| `move(dx, dy)` | Move relativamente |
| `set_color(cor)` | Altera a cor |
| `set_width(valor)` | Altera a espessura do contorno/segmento |
| `set_size(largura, altura)` | Altera o tamanho de painéis e elipses |
| `set_font_size(valor)` | Altera o tamanho de objetos de texto |
| `hide()` | Oculta o objeto |
| `show()` | Mostra o objeto novamente |
| `remove()` | Remove o objeto da janela |

Exemplo completo:

```krypt
import <window>
import <iolib>

window.create("Formas Krypt", 700, 400);
window.set_background("#111827");

var topo = window.segment(20, 20, 680, 20, "#38bdf8", 3);
var caixa = window.panel(80, 80, 240, 140, "#1d4ed8", "#93c5fd", 4);
var bola = window.ellipse(420, 90, 140, 140, "#f97316", "#fed7aa", 4);
var texto = window.text("Objetos Krypt", 210, 280, 28, "white");

fun clicar(x, y) {
    bola.move(5, 0);
    print("Clique:", x, y);
}

iolib.on_click(clicar);
window.show();
```

## Comandos da CLI

```text
krypt --help
```

Mostra todos os comandos disponíveis.

```text
krypt help
```

Também mostra a ajuda geral.

```text
krypt --version
```

Mostra a versão instalada.

```text
krypt --about
```

Mostra a versão e uma descrição da linguagem.

```text
krypt check "arquivo.krypt"
```

Verifica a sintaxe sem executar o programa.

```text
krypt -File "arquivo.krypt"
```

Executa o arquivo Krypt. Essa é a forma principal de uso.
