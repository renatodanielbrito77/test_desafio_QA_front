# DemoQA · Desafio de QA Automation — Frontend

Suíte de testes ponta a ponta em **Python, Selenium WebDriver e Behave**. As especificações executáveis usam **Gherkin em português**. O Behave é a implementação BDD usada para executar os passos em Python.

## Como avaliar a entrega

Após instalar as dependências e ativar o ambiente virtual, execute **`./testar-desafio`**. O comando roda somente os cinco cenários obrigatórios do enunciado no Chrome, com semente 1729. O bônus, as validações negativas e o cenário de Subjects vazio ficam fora dessa execução.

Execute o bônus com `python -m behave --tags @bonus -D seed=1729`. Enquanto o defeito persistir, a saída será de falha após a primeira exclusão. O teste informa as contagens e as linhas afetadas. Veja os [passos para reproduzir os defeitos](docs/defeitos-demoqa.md).

## Cobertura

| Fluxo | Critério verificado |
| --- | --- |
| Practice Form | Preenche todos os campos com dados válidos gerados durante a execução, anexa um TXT, confere os dados do modal e fecha a confirmação. |
| Practice Form negativo | Verifica a rejeição do formulário vazio, de um e-mail sem arroba e de telefones com nove dígitos ou com letras. Em todos os casos, a suíte confere que o modal permanece fechado. |
| Practice Form sem matéria | Envia dados válidos com **Subjects** vazio e confere que o modal aceita o cadastro com esse campo em branco. |
| Browser Windows | Abre uma janela real, valida “This is a sample page”, fecha a nova janela e retorna à original. |
| Web Tables | Cria, edita e exclui um registro, conferindo a criação e a edição e comparando a tabela sem filtro com o estado inicial após excluir. |
| Progress Bar | Inicia, para abaixo de 25%, confirma a pausa, retoma até 100% e reseta para 0%. |
| Sortable | Usa arrastar e soltar na aba List e verifica a ordem One, Two, Three, Four, Five, Six. |
| Bônus de Web Tables | Gera e confere 12 registros a partir de uma tabela Gherkin e verifica a exclusão individual com preservação das demais linhas. A primeira exclusão revelou o defeito descrito abaixo. |

Cada cenário começa na página inicial e usa o menu e submenu do DemoQA. A automação cobre a Parte 2 do desafio.

## Executar

É necessário ter Python 3.10 ou superior, Google Chrome ou Firefox e acesso ao DemoQA. Na primeira execução, o Selenium Manager pode baixar o driver compatível com o navegador. Se o ambiente já disponibilizar um driver compatível, informe seu caminho em `CHROMEDRIVER` para Chrome ou `GECKODRIVER` para Firefox.

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
./testar-desafio
```

O comando usa a tag `@original`. Para executar o mesmo recorte pelo PowerShell ou gerar JUnit, rode `python -m behave --tags @original -D seed=1729 --junit --junit-directory artifacts/junit`.

No PowerShell, use `.\.venv\Scripts\Activate.ps1` para ativar o ambiente virtual.

```sh
# Executar somente o cenário de janelas com o Chrome visível
python -m behave features/browser_windows.feature -D headed=true

# Executar somente o bônus
python -m behave --tags @bonus

# Executar as validações negativas do formulário
python -m behave --tags @negative -D seed=1729

# Executar a cobertura Firefox validada
python -m behave --tags 'not @bonus and not @sortable' -D browser=firefox -D seed=1729

# Repetir os dados de uma execução
python -m behave -D seed=1729
```

O Chrome é o navegador padrão. A execução é headless por padrão e cada cenário usa uma sessão independente. A semente é exibida no início da suíte. Use o mesmo valor com `-D seed` para reproduzir os dados. Capturas de cenários com falha ficam em `artifacts/<navegador>/` quando a sessão do navegador ainda permite capturar a tela. Com `--junit`, os relatórios XML ficam em `artifacts/junit/`.

## Organização

- `features/` contém os cenários e os hooks de ciclo de vida do navegador.
- `features/steps/` associa os passos Gherkin às ações e verificações.
- `pages/` concentra seletores e operações da interface em Page Objects.
- `fixtures/anexo-demoqa.txt` é o arquivo de teste lido no upload.

A tabela é pesquisada por e-mail. O bônus configura 20 linhas por página para conferir os 12 registros criados junto com os originais. O teste da barra usa o progresso exibido para decidir quando clicar em **Stop**. O teste de janelas usa os identificadores de janela do WebDriver para fechar somente a janela de exemplo.

## Integração contínua

O workflow [Testes frontend](.github/workflows/frontend.yml) executa os fluxos principais e as variações do formulário no Chrome em cada push na main e pull request. O Firefox cobre os mesmos fluxos, com o Sortable em uma etapa não bloqueante e com JUnit próprio. Os relatórios e capturas disponíveis ficam nos artefatos da execução. O bônus pode ser acionado manualmente com a opção `run_bonus`.

### Investigação do Sortable no Firefox

Com Firefox 159.0.1 e geckodriver 0.37.1 no Linux, o cenário completo passou em **0 de 2 sessões headless** e **1 de 2 sessões com display virtual**. Em duas falhas, o gesto moveu **Five** quando deveria mover **Six**.

Em uma página mínima de controle, o Firefox iniciou o arraste e chegou ao alvo. A captura após o gesto registrou `dragstart` e `dragover`, sem `drop` ou `dragend`. O Chrome registrou os eventos de encerramento e moveu o item. No DemoQA, o Firefox chegou a reordenar a lista durante o arraste. Os resultados apontam para uma limitação na automação do gesto via Firefox/WebDriver, com causa exata ainda em aberto. [Registro relacionado da Mozilla](https://bugzilla.mozilla.org/show_bug.cgi?id=1515879) · [Execução do Firefox no CI](https://github.com/renatodanielbrito77/test_desafio_QA_front/actions/runs/44570323470/job/135723261549)

O Sortable permanece obrigatório no Chrome pelo comando `./testar-desafio`. O Firefox continua como verificação de compatibilidade não bloqueante no CI.
