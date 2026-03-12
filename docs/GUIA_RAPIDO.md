# Guia Rápido - Processamento de XMLs em Python

## 🚀 Início Rápido

### 1. Instalar Dependências

```bash
pip install -r requirements.txt
```

### 2. Configurar Caminhos (Opcional)

Copie o arquivo de exemplo:
```bash
copy .env.example .env
```

Edite o `.env` com seus caminhos:
```
SOURCE_DIR=C:\seu\caminho\de\origem
DESTINATION_DIR=C:\seu\caminho\de\destino
DAYS_BACK=7
CNF_CODES=046005,046006,046007
```

### 3. Executar Comandos

```bash
# Ver ajuda
python main.py --help

# Ver configuração atual
python main.py config-show
```

---

## 📋 Comandos Principais

### Copiar Arquivos por Código CNF

```bash
python main.py copy-cnf \
    --source "C:\caminho\origem" \
    --destination "C:\caminho\destino" \
    --cnf-codes "046005,046006,046007" \
    --days-back 7
```

**Ou usando o script individual:**
```bash
python copy_cnf_files.py \
    --source "C:\caminho\origem" \
    --destination "C:\caminho\destino"
```

---

### Procurar String em Arquivos

```bash
python main.py find-string \
    --path "C:\caminho\pesquisa" \
    --string "TAIBA"
```

**Exemplo com regex:**
```bash
python main.py find-string \
    --path "C:\XMLs" \
    --string "^600019[0-9]{2}$" \
    --regex
```

---

### Procurar Múltiplas Strings

**Opção 1 - Incluir na linha de comando:**
```bash
python main.py find-strings \
    --path "C:\caminho\pesquisa" \
    --strings "60002496,60002497,80008482"
```

**Opção 2 - Usar arquivo (melhor para listas grandes):**

Crie um arquivo `meus_numeros.txt`:
```
60002496
60002497
80008482
60002505
60002507
```

Depois execute:
```bash
python main.py find-strings \
    --path "C:\caminho\pesquisa" \
    --file meus_numeros.txt
```

---

### Atualizar Arquivos XML

Aplica as seguintes modificações:
- Atualiza declaração XML com UTF-8
- Remove quebras de linha
- Remove tags específicas (SendBillHeader, SendBillProfiles, etc.)
- Renomeia cmfdailyItens → CmfdailyItens
- Compacta em ZIP (opcional)

```bash
# Cria novos arquivos modificados e compactados
python main.py update-xml \
    --path "C:\XMLs" \
    --compress

# Sem compactação
python main.py update-xml \
    --path "C:\XMLs" \
    --no-compress

# Sobrescrever originais
python main.py update-xml \
    --path "C:\XMLs" \
    --overwrite
```

---

## 🪟 No Windows

### Usar o Executável em Lote

```bash
# Apenas execute
run.bat

# Ou passar comando diretamente
run.bat copy-cnf
```

### Menu Interativo

```bash
python quickstart.py
```

---

## 📊 Visualizar Logs

Os logs ficam em `logs/`:

```bash
# Ver log principal (Windows)
type logs\app.log

# Ver log de cópias (Windows)
type logs\file_copier.log

# Ver log de buscas (Windows)
type logs\file_finder.log

# Ver log de modificações (Windows)
type logs\xml_modifier.log

# Acompanhar em tempo real (PowerShell)
Get-Content logs\app.log -Wait
```

---

## ⚙️ Exemplos Práticos

### Exemplo 1: Copiar Cupons Recentes

```bash
python main.py copy-cnf ^
    --source "C:\Users\Windows\CMFlexScheduller\ItensEnviados\Magna" ^
    --destination "C:\Users\jadson.morais\Projects\Analise_01\result" ^
    --cnf-codes "046005,046006,046007" ^
    --days-back 7
```

### Exemplo 2: Encontrar Checks em Falta

Crie `checks_pendentes.txt`:
```
60002496
60002497
80008482
60002505
60002507
60002508
80008496
20003232
80008499
80008479
```

Execute:
```bash
python main.py find-strings ^
    --path "C:\NFCe\src\cmflex\ItensEnviados\Taiba" ^
    --file checks_pendentes.txt
```

Resultado:
```
Found:     7 string(s)
Not found: 3 string(s)

⚠ Strings NOT found:
  ✗ 80008499
  ✗ 80008497
  ✗ 20003243
```

### Exemplo 3: Processar XMLs Completos

```bash
# Atualizar e compactar todos os XMLs
python main.py update-xml ^
    --path "C:\Processing\XMLs" ^
    --compress

# Resultado: Arquivos _modificado.xml e _modificado.xml.zip
```

---

## 🐛 Solução de Problemas

### "Python não encontrado"

Instale Python 3.8+ de https://www.python.org/

Verifique:
```bash
python --version
```

### "ModuleNotFoundError: No module named 'click'"

Instale as dependências:
```bash
pip install -r requirements.txt
```

### "Diretório não encontrado"

Verifique a configuração:
```bash
python main.py config-show
```

Atualize o `.env` com os caminhos corretos.

### Erros de codificação

Alguns arquivos podem usar codificação diferente. Tente:
```bash
set FILE_ENCODING=latin-1
python main.py find-string --path "C:\path" --string "test"
```

---

## 📖 Documentação Completa

Para informações detalhadas, veja:

- **[README.md](README.md)** - Documentação completa
- **[MIGRATION_GUIDE.md](MIGRATION_GUIDE.md)** - Como migrar dos scripts antigos
- **[REFACTORING_SUMMARY.md](REFACTORING_SUMMARY.md)** - O que foi refatorado

---

## 💡 Dicas Úteis

### Usar Variáveis de Ambiente

```bash
# Definir para a sessão
set SOURCE_DIR=C:\minha\origem
set DESTINATION_DIR=C:\meu\destino

# Executar (usa variáveis)
python main.py copy-cnf
```

### Salvar Resultados em Arquivo

```bash
# Salvar em arquivo
python main.py find-string --path "C:\path" --string "TAIBA" > resultados.txt

# Ver depois
type resultados.txt
```

### Criar Alias no PowerShell

```powershell
# Adicione ao seu perfil do PowerShell
function copy-cnf { python main.py copy-cnf @args }
function find-str { python main.py find-string @args }
function find-strs { python main.py find-strings @args }
function update-xml { python main.py update-xml @args }

# Depois use:
copy-cnf --source "C:\path"
```

---

## 🔄 Equivalência com Scripts Antigos

| Antes (PowerShell) | Agora (Python) |
|---|---|
| `.\analise_cupons.ps1` | `python main.py copy-cnf` ou `python copy_cnf_files.py` |
| `.\find_filename.ps1` | `python main.py find-string` ou `python find_string.py` |
| `.\find_string_on_folder.ps1` | `python main.py find-string` ou `python find_string.py` |
| `.\find_string_on_folder_list.ps1` | `python main.py find-strings` ou `python find_strings.py` |
| `.\AtualizarXML.ps1` | `python main.py update-xml` ou `python update_xml.py` |
| `python copy_files_contains.py` | `python main.py copy-cnf` ou `python copy_cnf_files.py` |

---

## 📞 Suporte Rápido

```bash
# Ver todos os comandos disponíveis
python main.py --help

# Ver ajuda de um comando específico
python main.py copy-cnf --help
python main.py find-string --help
python main.py find-strings --help
python main.py update-xml --help
python main.py config-show --help

# Ver versão
python main.py --version
```

---

## ✅ Checklist Inicial

- [ ] Python 3.8+ instalado
- [ ] Dependências instaladas: `pip install -r requirements.txt`
- [ ] Arquivo `.env` criado e configurado (copiar de `.env.example`)
- [ ] Testou `python main.py config-show`
- [ ] Testou um comando simples de busca
- [ ] Consultou logs em `logs/` se houve problemas

---

**Tudo pronto? Comece com:**
```bash
python main.py find-string --path "C:\seu\caminho" --string "algo"
```

Bom uso! 🎉
