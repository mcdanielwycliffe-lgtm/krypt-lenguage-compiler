# Krypt para Windows

## Visão geral

A Krypt é uma linguagem de programação experimental distribuída no Windows como `krypt.exe`. O executável reúne a CLI, o parser e o runtime da linguagem. Ele executa arquivos `.krypt` diretamente e não requer uma instalação separada de Python para o usuário final.

O uso principal é:

```bat
krypt.exe -File "programa.krypt"
```

Esta edição é a distribuição Windows correspondente ao binário compilado com PyInstaller. O executável deve ser gerado em Windows para garantir compatibilidade com Windows; PyInstaller não faz compilação cruzada entre Linux e Windows.

## Instalação

Baixe `krypt.exe` do repositório e coloque-o em uma pasta permanente. Para usar o comando `krypt` de qualquer Prompt de Comando, adicione essa pasta à variável de ambiente `PATH`.

Teste no Prompt de Comando:

```bat
krypt.exe --version
krypt.exe --help
```

Se o executável estiver no `PATH`, o `.exe` pode ser omitido:

```bat
krypt --version
krypt -File "programa.krypt"
```

No PowerShell, para executar um binário da pasta atual, use `./` quando necessário:

```powershell
./krypt.exe --version
./krypt.exe -File ".\programa.krypt"
```

A biblioteca `window` cria janelas nativas. Portanto, programas gráficos devem ser executados em uma sessão Windows com desktop disponível.

## Comandos da CLI

```bat
krypt.exe -File "arquivo.krypt"
```

Lê, analisa e executa o arquivo Krypt indicado. `-File` é a forma oficial para executar um programa.

```bat
krypt.exe --version
```

Exibe a versão instalada, por exemplo `Krypt 0.1.0`.

```bat
krypt.exe --about
```

Exibe a versão e uma descrição da linguagem.

```bat
krypt.exe --help
```

Mostra a ajuda completa da interface de linha de comandos.

```bat
krypt.exe help
```

É um alias da ajuda geral.

```bat
krypt.exe check "arquivo.krypt"
```

Verifica a sintaxe sem executar o arquivo. Use-o em scripts de CI ou antes de publicar exemplos.

A documentação usa “CLI”, abreviação de Command-Line Interface. Caso materiais anteriores mencionem “CPI”, o termo correto para os comandos do executável é CLI.

## Formato de arquivo

Programas Krypt usam a extensão `.krypt`:

```krypt
print("Olá, Windows!");
```

Execute:

```bat
krypt.exe -File "hello.krypt"
```

## Sintaxe básica

### Comentários

```krypt
// Comentário de uma linha
```

### Variáveis

```krypt
var nome = "Krypt";
var idade = 18;
var ativo = true;
var itens = [1, 2, 3];

idade = idade + 1;
```

### Valores

A linguagem possui textos entre aspas simples ou duplas, números inteiros, números decimais, `true`, `false`, `null` e listas literais.

```krypt
var texto = "texto";
var outro = 'texto';
var inteiro = 42;
var decimal = 2.5;
var ligado = true;
var vazio = null;
```

### Operadores matemáticos

```krypt
var resultado = 10 + 2 * 3;
var resto = 10 % 3;
```

Operadores: `+`, `-`, `*`, `/` e `%`.

### Comparações

```krypt
if (idade >= 18) {
    print("Maior de idade");
}
```

Operadores: `==`, `!=`, `<`, `>`, `<=` e `>=`.

### Lógica

```krypt
if (idade >= 18 and possui_documento) {
    print("Permitido");
}
```

A Krypt aceita `and`, `or`, `not` e os equivalentes `&&`, `||`, `!`.

### Condicionais

```krypt
if (pontuacao >= 70) {
    print("Aprovado");
} else {
    print("Reprovado");
}
```

### Repetição

```krypt
var i = 0;
while (i < 10) {
    print(i);
    i = i + 1;
}
```

### Funções

```krypt
fun multiplicar(a, b) {
    return a * b;
}

print(multiplicar(6, 7));
```

Toda instrução termina com `;`. Declarações de função usam um bloco delimitado por `{` e `}`.

## Bibliotecas nativas

As bibliotecas são importadas com a sintaxe Krypt:

```krypt
import <window>;
import <iolib>;
```

O ponto e vírgula depois do `>` é opcional na implementação atual, mas é recomendado para manter os arquivos consistentes.

## Biblioteca `window`

`window` cria uma janela e uma área de desenho. A sequência recomendada é criar a janela, adicionar objetos, registrar eventos e chamar `window.show()`.

```krypt
import <window>;

window.create("Minha janela", 800, 500);
window.set_background("#172033");
window.show();
```

### Texto

```krypt
var titulo = window.text("KRYPT", 30, 30, 32, "#7dd3fc");
titulo.set_position(50, 45);
titulo.set_color("white");
titulo.set_font_size(36);
```

Assinatura: `window.text(valor, x, y, tamanho, cor)`.

### Segmento

O objeto `segment` representa uma linha:

```krypt
var linha = window.segment(20, 80, 700, 80, "cyan", 4);
linha.set_color("yellow");
linha.set_width(6);
linha.move(0, 20);
```

Assinatura: `window.segment(x1, y1, x2, y2, cor, espessura)`.

### Painel

O objeto `panel` representa um retângulo:

```krypt
var painel = window.panel(80, 120, 240, 140, "#2563eb", "white", 3);
painel.set_position(100, 130);
painel.set_size(300, 180);
painel.set_color("#22c55e");
```

Assinatura: `window.panel(x, y, largura, altura, preenchimento, contorno, espessura)`.

### Elipse

O objeto `ellipse` representa uma elipse ou círculo:

```krypt
var bola = window.ellipse(430, 120, 140, 140, "#f97316", "#fed7aa", 3);
bola.move(10, 0);
bola.set_size(160, 120);
```

Assinatura: `window.ellipse(x, y, largura, altura, preenchimento, contorno, espessura)`.

### Métodos dos objetos

Os objetos retornados podem ser guardados em variáveis. Métodos comuns:

| Método | Uso |
|---|---|
| `set_position(x, y)` | Define a posição |
| `move(dx, dy)` | Move relativamente |
| `set_color(cor)` | Altera a cor |
| `set_width(valor)` | Altera a espessura |
| `set_size(largura, altura)` | Redimensiona painel/elipse |
| `set_font_size(valor)` | Altera tamanho de texto |
| `hide()` | Oculta o objeto |
| `show()` | Exibe o objeto |
| `remove()` | Remove o objeto |

`set_size` deve ser usado em `panel` e `ellipse`. `set_font_size` deve ser usado em textos.

## Biblioteca `iolib`

### Teclado por evento

```krypt
import <window>;
import <iolib>;

fun pressionou(tecla) {
    print("Tecla:", tecla);
    if (tecla == "Escape") {
        window.close();
    }
}

window.create("Eventos", 640, 360);
iolib.on_key("Escape", pressionou);
window.show();
```

### Clique

```krypt
fun clicou(x, y) {
    print("Clique em", x, y);
}

iolib.on_click(clicou);
```

A callback recebe as coordenadas do clique.

### Estado de uma tecla

```krypt
iolib.track_key("Left");

if (iolib.key("Left")) {
    print("Left está pressionada");
}
```

`track_key` começa a acompanhar uma tecla. `key` retorna um booleano com o estado atual.

### Entrada do terminal

```krypt
var usuario = iolib.input("Usuário: ");
print("Olá", usuario);
```

## Funções integradas

A linguagem oferece `print`, `len`, `str`, `int` e `float`:

```krypt
print("valor", 42);
var quantidade = len([1, 2, 3]);
var texto = str(42);
var inteiro = int(3.9);
var decimal = float(10);
```

## Exemplo completo para Windows

```krypt
import <window>;
import <iolib>;

var cliques = 0;

fun registrar(x, y) {
    cliques = cliques + 1;
    print("Clique", cliques, "em", x, y);
}

fun tecla(key) {
    if (key == "Escape") {
        window.close();
    }
}

window.create("Exemplo Krypt Windows", 760, 420);
window.set_background("#0f172a");
window.text("KRYPT WINDOWS", 40, 30, 30, "#7dd3fc");
window.panel(40, 100, 240, 130, "#1d4ed8", "#93c5fd", 3);
window.ellipse(400, 100, 140, 140, "#f97316", "#fed7aa", 3);
window.segment(40, 280, 700, 280, "#38bdf8", 3);
iolib.on_click(registrar);
iolib.on_key("Escape", tecla);
window.show();
```

Execute com:

```bat
krypt.exe -File "exemplo.krypt"
```

## Como o executável foi produzido

O compilador da Krypt é escrito em Python e empacotado com PyInstaller em modo `--onefile`. A geração deve ser feita em Windows:

```bat
python -m pip install pyinstaller
python -m PyInstaller --clean --noconfirm --onefile --name krypt --paths . kryptc.py
```

O resultado fica em `dist\krypt.exe`. O executável Linux não substitui este binário e o binário Windows não deve ser tratado como portável para Linux.

## Solução de problemas

Se `krypt` não for encontrado, execute com o caminho completo ou adicione a pasta do executável ao `PATH`.

Se aparecer erro de sintaxe, rode:

```bat
krypt.exe check "arquivo.krypt"
```

Se uma janela não abrir, verifique se o programa chamou `window.create()` antes dos métodos gráficos e se terminou com `window.show()`.

Se um evento não funcionar, confirme que `iolib` foi importada, que a janela foi criada antes do registro e que a callback possui os parâmetros corretos.

## Versão e compatibilidade

Consulte a versão com `krypt --version` e fixe a versão usada nos exemplos publicados. Esta documentação corresponde à linha `0.1.x` da Krypt.

## Licença e contribuição

A Krypt é um projeto experimental e educacional. Ao contribuir, mantenha a documentação da CLI e das bibliotecas sincronizada com a implementação e inclua exemplos Krypt reproduzíveis.
