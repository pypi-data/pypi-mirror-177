## Controle de alterações

Documentação das principais alterações sofridas por este repositório. Baseado na filosofia [Mantenha um Changelog](https://keepachangelog.com/pt-BR/1.0.0/).

### [0.3.1] - 2022-11-16

- Implementa flag --no-headless na busca do último contracheque

### [0.3.0] - 2022-11-13

- Refaz o processo para novo portal do servidor mg
- Somente função last period funcionando no momento

### [0.2.5] - 2022-03-09

- Melhora geração arquivo pdf

### [0.2.4] - 2022-03-09

- Corrige nome arquivo pdf

### [0.2.3] - 2022-03-09

- Cria flag para pdf para determinar download do contracheque (--pdf/--no-pdf)
- Melhora Readme.md

### [0.2.2] - 2022-03-09

- Flags --masp e --senha passados após subcomando mg
- Cria flag para determinar se Chrome ficará headless durante execução (--headless/--no-headless)
- Melhora Readme.md

### [0.2.1] - 2022-03-08

- Chrome headless durante execução

### [0.2.0] - 2021-12-27

- Inclusão comando `ate-periodo-inicial`
- Trocando print por click.echo para melhorar interface usuário no windows

### [0.1.1] - 2021-12-08

- Correção encoding utf-8 durante extração código fonte da página em sistema operacional windows


### [0.1.0] - 2021-12-06

- Versão inicial
  - Comando `contracheque mg mais-recente` para busca das informações do último contracheque disponível.
  - Comando `contracheque mg todos` para busca das informações de todos os contracheque disponíveis.

### [0.0.1.900] - 2021-11-27

- Versão para teste de setup do pacote
  - Criação de arquivos de configuração inicial do pacote:
    - README.md,
    - CHANGELOG.md,
    - Makefile,
    - Manifest.in
    - Requirements.txt
    - setup.py
