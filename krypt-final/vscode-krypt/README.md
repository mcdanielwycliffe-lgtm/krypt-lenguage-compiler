# Krypt Language Support para VS Code

Extensão de realce de sintaxe para a linguagem Krypt.

## Recursos

- Reconhecimento de arquivos `.krypt`.
- Realce de `import`, `var`, `fun`, `if`, `else`, `while` e `return`.
- Realce de `true`, `false` e `null`.
- Realce de `and`, `or`, `not`, operadores matemáticos, lógicos e de comparação.
- Realce de strings com aspas simples e duplas, escapes, números e comentários `//`.
- Destaque de funções, funções integradas e métodos após `.`.
- Auto-fechamento de parênteses, colchetes, chaves e strings.
- Tema de ícones com ícone próprio para arquivos `.krypt`.

## Instalação rápida a partir da pasta do projeto

### Linux

Copie a extensão para o diretório de extensões do usuário:

```bash
mkdir -p ~/.vscode/extensions/krypt-lang.krypt-language-support-0.1.0
cp -r . ~/.vscode/extensions/krypt-lang.krypt-language-support-0.1.0/
```

Se usar VSCodium, o diretório normalmente é `~/.vscode-oss/extensions/`.

### Windows PowerShell

```powershell
$dest = "$env:USERPROFILE\\.vscode\\extensions\\krypt-lang.krypt-language-support-0.1.0"
New-Item -ItemType Directory -Force $dest
Copy-Item -Recurse -Force * $dest
```

Depois, reinicie o VS Code e abra um arquivo com extensão `.krypt`. O identificador de linguagem aparecerá como `Krypt` no canto inferior direito.

## Instalação pelo arquivo VSIX

O arquivo `krypt-language-support-0.1.0.vsix` pode ser instalado pela interface do VS Code em **Extensions → ⋯ → Install from VSIX...** ou pela CLI:

```bash
code --install-extension krypt-language-support-0.1.0.vsix
```

Depois de instalar, abra ou reabra um arquivo `.krypt`.

Para ativar o ícone no Explorer, abra **Preferences: File Icon Theme** na Command Palette e selecione **Krypt Icons**. O tema associa automaticamente o ícone Krypt à extensão `.krypt`.

## Observação

Esta extensão fornece realce e configuração de edição. Ela não executa o compilador, não implementa autocomplete e não fornece depuração. Para executar um arquivo, use o binário da Krypt:

```bash
krypt -File "programa.krypt"
```

No Windows:

```bat
krypt.exe -File "programa.krypt"
```
