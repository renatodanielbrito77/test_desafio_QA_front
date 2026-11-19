# Defeitos observados no DemoQA

## Practice Form · botão Close mantém o modal aberto

1. Acesse **Forms → Practice Form** na página inicial.
2. Preencha os campos obrigatórios e clique em **Submit**.
3. Com o modal aberto, clique em **Close** e consulte o console do navegador.

**Esperado.** O modal desaparece e o formulário volta a ficar acessível.

**Observado no Chrome.** O modal permanece aberto e o console registra `Uncaught TypeError: Lr.findDOMNode is not a function`. O cenário principal usa a tecla **Escape** e valida que o modal desaparece.

## Web Tables · excluir uma linha remove outras linhas recém-criadas

Execute `python -m behave --tags @bonus -D seed=1729`. O cenário cria 12 registros com e-mails distintos, verifica os dados das 15 linhas e clica em **Delete** apenas no primeiro registro criado.

**Esperado.** A tabela passa de 15 para 14 linhas. Os outros 11 registros criados e os três originais permanecem.

**Observado no Chrome.** A tabela passa de 15 para 3 linhas. Os 11 outros registros criados também somem. O teste falha e lista os e-mails afetados. Use `--junit --junit-directory artifacts/junit` para gravar o relatório, além da captura gerada em caso de falha.
