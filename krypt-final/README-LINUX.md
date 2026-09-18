# Krypt para Linux

## Visão geral

A Krypt é uma linguagem de programação experimental com compilador/runtime distribuído como um único executável. Esta edição é destinada a Linux 64-bit e oferece execução de arquivos `.krypt`, verificação de sintaxe, informações da versão e uma biblioteca gráfica nativa baseada em Tk.

O binário desta distribuição é chamado `krypt`. Ele não exige que o usuário instale Python para executar programas Krypt comuns, porque o runtime é empacotado pelo PyInstaller.

## Instalação

Baixe o arquivo executável `krypt-linux-x86_64`, torne-o executável e, opcionalmente, coloque-o no PATH:

```bash
chmod +x krypt-linux-x86_64
sudo install -m 755 krypt-linux-x86_64 /usr/local/bin/krypt
```

Confirme a instalação:

```bash
krypt --version
krypt --help
```

A biblioteca `window` precisa de um ambiente gráfico Linux com Tk disponível. Em distribuições Debian/Ubuntu, o pacote de desenvolvimento/runtime normalmente é instalado com:

```bash
sudo apt install python3-tk tk
```

Em um servidor sem display, programas de terminal funcionam, mas programas que chamam `window.create()` precisam de uma sessão gráfica ou de um display virtual.

## Uso básico

Execute um arquivo Krypt:

```bash
krypt -File "programa.krypt"
```

O caminho pode ser relativo ou absoluto:

```bash
krypt -File ./examples/hello.krypt
krypt -File /home/usuario/projeto/app.krypt
```

Verifique a versão:

```bash
krypt --version
```

Veja todos os comandos:

```bash
krypt --help
krypt help
```

Veja informações sobre o projeto:

```bash
krypt --about
```

Verifique a sintaxe sem executar:

```bash
krypt check "programa.krypt"
```

Uma verificação bem-sucedida exibe `Sintaxe OK`. Erros informam o token e a linha aproximada do problema.

## Comandos CLI

| Comando | Finalidade |
|---|---|
| `krypt -File arquivo.krypt` | Executa um programa Krypt |
| `krypt --version` | Mostra a versão |
| `krypt --about` | Mostra a versão e uma descrição curta |
| `krypt --help` | Mostra a ajuda da CLI |
| `krypt help` | Alias da ajuda |
| `krypt check arquivo.krypt` | Analisa a sintaxe sem executar |

Nesta documentação, “CLI” significa interface de linha de comandos. Se você encontrar a expressão “comandos CPI” em algum material antigo, ela deve ser entendida como “comandos CLI”.

## Estrutura de um programa

```krypt
import <window>;
import <iolib>;

var nome = "Krypt";

fun saudacao(pessoa) {
    print("Olá", pessoa);
}

saudacao(nome);
```

As instruções terminam com `;`, exceto declarações de função e blocos, que terminam com `}`.

## Comentários

```krypt
// Comentário de uma linha
print("Programa iniciado");
```

## Valores e variáveis

```krypt
var texto = "Krypt";
var inteiro = 42;
var decimal = 3.14;
var ligado = true;
var desligado = false;
var vazio = null;
var lista = [1, 2, 3];
```

Os valores disponíveis no runtime são textos, inteiros, números decimais, booleanos, `null` e listas literais.

Uma variável pode receber um novo valor:

```krypt
var total = 10;
total = total + 5;
print(total);
```

## Operadores

### Matemáticos

`+`, `-`, `*`, `/` e `%` representam soma, subtração, multiplicação, divisão e resto.

```krypt
var resultado = (10 + 2) * 3;
print(resultado);
```

### Comparação

`==`, `!=`, `<`, `>`, `<=` e `>=` comparam valores.

```krypt
if (idade >= 18) {
    print("Adulto");
}
```

### Lógicos

A Krypt aceita `and`, `or` e `not`, além de `&&`, `||` e `!`.

```krypt
if (idade >= 18 and possui_documento) {
    print("Acesso permitido");
}
```

## Condicionais

```krypt
if (temperatura > 30) {
    print("Quente");
} else {
    print("Agradável");
}
```

## Repetição

```krypt
var contador = 0;
while (contador < 5) {
    print(contador);
    contador = contador + 1;
}
```

## Funções

```krypt
fun somar(a, b) {
    return a + b;
}

var resposta = somar(20, 22);
print(resposta);
```

Funções podem receber zero ou mais parâmetros. Quando não há `return`, o resultado é `null`.

## Biblioteca nativa `window`

`window` fornece uma janela e uma área de desenho. Primeiro crie a janela; depois configure objetos e, ao final, chame `window.show()`.

```krypt
import <window>;

window.create("Minha aplicação", 800, 500);
window.set_background("#111827");
window.show();
```

### Texto

```krypt
var titulo = window.text("KRYPT", 30, 30, 32, "#7dd3fc");
titulo.set_position(50, 40);
titulo.set_color("white");
titulo.set_font_size(36);
```

A forma é `window.text(valor, x, y, tamanho, cor)`.

### Segmento

O nome Krypt para uma linha é `segment`:

```krypt
var linha = window.segment(20, 70, 700, 70, "cyan", 3);
linha.set_color("yellow");
linha.set_width(5);
linha.move(0, 10);
```

A forma é `window.segment(x1, y1, x2, y2, cor, espessura)`.

### Painel

`panel` cria um elemento retangular:

```krypt
var painel = window.panel(80, 100, 240, 140, "#2563eb", "white", 3);
painel.set_position(100, 120);
painel.set_size(300, 160);
painel.set_color("#22c55e");
```

A forma é `window.panel(x, y, largura, altura, preenchimento, contorno, espessura)`.

### Elipse

```krypt
var circulo = window.ellipse(420, 100, 140, 140, "#f97316", "white", 3);
circulo.move(10, 0);
circulo.set_size(160, 120);
```

A forma é `window.ellipse(x, y, largura, altura, preenchimento, contorno, espessura)`.

### Propriedades dos objetos

Objetos gráficos podem ser guardados em variáveis. Os métodos disponíveis são `set_position(x, y)`, `move(dx, dy)`, `set_color(cor)`, `set_width(valor)`, `set_size(largura, altura)`, `set_font_size(valor)` para texto, `hide()`, `show()` e `remove()`.

`set_size` é aplicável a painéis e elipses. `set_font_size` é aplicável a textos. `set_width` é útil para segmentos e contornos.

### Encerramento

```krypt
window.close();
```

## Biblioteca nativa `iolib`

`iolib` integra entrada de usuário ao runtime gráfico.

### Teclado por evento

```krypt
import <window>;
import <iolib>;

fun tecla_pressionada(tecla) {
    print("Tecla:", tecla);
    if (tecla == "Escape") {
        window.close();
    }
}

window.create("Teclado", 640, 360);
iolib.on_key("Escape", tecla_pressionada);
window.show();
```

### Clique do mouse

```krypt
fun clicou(x, y) {
    print("Clique em", x, y);
}

iolib.on_click(clicou);
```

### Estado contínuo de uma tecla

```krypt
iolib.track_key("Left");

if (iolib.key("Left")) {
    print("Esquerda pressionada");
}
```

`track_key` registra a tecla e `key` retorna `true` enquanto ela estiver pressionada e `false` depois da liberação.

### Entrada de terminal

```krypt
var nome = iolib.input("Nome: ");
print("Olá", nome);
```

## Funções integradas

O runtime disponibiliza `print`, `len`, `str`, `int` e `float`.

```krypt
print("texto", 10);
var tamanho = len([1, 2, 3]);
var texto = str(42);
var inteiro = int(3.9);
var decimal = float(10);
```

## Exemplo completo

```krypt
import <window>;
import <iolib>;

var cliques = 0;

fun registrar_clique(x, y) {
    cliques = cliques + 1;
    print("Clique", cliques, "em", x, y);
}

fun pressionar(tecla) {
    if (tecla == "Escape") {
        window.close();
    }
}

window.create("Exemplo Linux Krypt", 760, 420);
window.set_background("#0f172a");
window.text("KRYPT LINUX", 40, 30, 30, "#7dd3fc");
window.panel(40, 100, 240, 130, "#1d4ed8", "#93c5fd", 3);
window.ellipse(400, 100, 140, 140, "#f97316", "#fed7aa", 3);
window.segment(40, 280, 700, 280, "#38bdf8", 3);
iolib.on_click(registrar_clique);
iolib.on_key("Escape", pressionar);
window.show();
```

## Limitações atuais

A distribuição Linux é um binário `x86_64` produzido para o ambiente compatível com PyInstaller. Para outra arquitetura, como ARM64, é necessário gerar o binário nessa arquitetura. O executável não converte um programa Krypt em código nativo independente: ele empacota o parser e o runtime Krypt e interpreta o arquivo `.krypt` ao ser executado.

A janela exige um display gráfico disponível. O `krypt check` é recomendado antes de distribuir um programa. Os nomes da biblioteca são parte da API Krypt e podem evoluir entre versões.

## Licença e contribuição

Este projeto é experimental e educacional. Ao publicar em um repositório, mantenha este README junto do binário correspondente e informe a versão mostrada por `krypt --version`.
