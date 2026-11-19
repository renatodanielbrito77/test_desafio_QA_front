# language: pt
Funcionalidade: Gestão de registros na tabela

  @frontend @original
  Cenário: Criar, editar e excluir um registro
    Dado que acesso "Web Tables" pelo menu "Elements"
    Quando crio um registro
    Então a tabela exibe os dados do novo registro
    Quando atualizo os dados desse registro
    Então a tabela exibe os dados atualizados
    Quando excluo esse registro
    Então a tabela volta a exibir somente os registros originais

  @frontend @bonus
  Cenário: Criar e excluir doze registros gerados durante a execução
    Dado que acesso "Web Tables" pelo menu "Elements"
    Quando crio um registro distinto para cada item da tabela
      | item |
      | 01   |
      | 02   |
      | 03   |
      | 04   |
      | 05   |
      | 06   |
      | 07   |
      | 08   |
      | 09   |
      | 10   |
      | 11   |
      | 12   |
    Então encontro todos os registros criados com os dados esperados
    Quando excluo todos os registros criados
    Então nenhum dos registros criados permanece na tabela
    E os registros originais permanecem na tabela
