# DemoQA · Desafio de QA Automation — Frontend

Suíte de testes ponta a ponta em **Python, Selenium WebDriver e Behave**. As especificações executáveis usam **Gherkin em português**. O Behave é a implementação BDD usada para executar os passos em Python.

## Cobertura

| Fluxo | Critério verificado |
| --- | --- |
| Practice Form | Preenche todos os campos com dados válidos gerados durante a execução, anexa um TXT, confere os dados do modal e fecha a confirmação. |
| Browser Windows | Abre uma janela real, valida “This is a sample page”, fecha a nova janela e retorna à original. |
| Web Tables | Cria, edita e exclui um registro, conferindo o estado da tabela a cada operação. |
| Progress Bar | Inicia, para até 25%, confirma a pausa, retoma até 100% e reseta para 0%. |
| Sortable | Usa arrastar e soltar na aba List e verifica a ordem One, Two, Three, Four, Five, Six. |
| Bônus de Web Tables | Gera e confere 12 registros a partir de uma tabela Gherkin e verifica a exclusão individual com preservação das demais linhas. A primeira exclusão revelou o defeito descrito abaixo. |

Cada cenário começa na página inicial e usa o menu e submenu do DemoQA. A automação cobre a Parte 2 do desafio.

## Executar

É necessário ter Python 3.10 ou superior, Google Chrome e acesso ao DemoQA. Na primeira execução, o Selenium Manager pode baixar a versão de ChromeDriver compatível com o navegador. Se o ambiente já disponibilizar um driver compatível, informe seu caminho na variável de ambiente `CHROMEDRIVER`.

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m behave --junit --junit-directory artifacts/junit
```

No PowerShell, use `.\.venv\Scripts\Activate.ps1` para ativar o ambiente virtual.

```sh
# Executar somente o cenário de janelas com o Chrome visível
python -m behave features/browser_windows.feature -D headed=true

# Executar somente o bônus
python -m behave --tags @bonus

# Executar os cinco cenários obrigatórios
python -m behave --tags 'not @bonus'

# Repetir os dados de uma execução
python -m behave -D seed=1729
```

O Chrome roda em modo headless por padrão e cada cenário usa uma sessão independente. A semente é exibida no início da suíte. Use o mesmo valor com `-D seed` para reproduzir os dados. Capturas de cenários com falha ficam em `artifacts/` quando a sessão do navegador ainda permite capturar a tela. Com `--junit`, os relatórios XML ficam em `artifacts/junit/`.

## Organização

- `features/` contém os cenários e os hooks de ciclo de vida do navegador.
- `features/steps/` associa os passos Gherkin às ações e verificações.
- `pages/` concentra seletores e operações da interface em Page Objects.
- `fixtures/anexo-demoqa.txt` é o arquivo de teste lido no upload.

A tabela é pesquisada por e-mail. O bônus configura 20 linhas por página para conferir os 12 registros criados junto com os originais. O teste da barra usa o progresso exibido para decidir quando clicar em **Stop**. O teste de janelas usa os identificadores de janela do WebDriver para fechar somente a janela de exemplo.

## Comportamentos observados no DemoQA

- **Practice Form.** O botão **Close** manteve o modal aberto e gerou `findDOMNode is not a function` no console do Chrome. O cenário usa **Escape**, que fecha o modal pela própria interface.
- **Web Tables, bônus.** Após criar e conferir os 12 registros, clicar em **Delete** em um deles remove também os outros 11 recém-criados. O cenário exige que cada exclusão preserve as demais linhas e registra os e-mails das linhas removidas indevidamente. Para reproduzir com a mesma massa, execute `python -m behave --tags @bonus -D seed=1729`. Enquanto o comportamento persistir, o bônus deixa a execução completa com status de falha.
