# language: pt
Funcionalidade: Cadastro de estudante

  @frontend @original
  Cenário: Enviar todos os dados de um estudante com um anexo
    Dado que acesso "Practice Form" pelo menu "Forms"
    Quando envio o formulário completo com dados aleatórios válidos e um arquivo TXT
    Então o modal confirma os dados enviados
    E posso fechar o modal de confirmação com Escape

  @frontend @negative
  Cenário: Rejeitar cadastro sem preencher campos obrigatórios
    Dado que acesso "Practice Form" pelo menu "Forms"
    Quando tento enviar o formulário vazio
    Então o primeiro nome é identificado como obrigatório e o modal não abre

  @frontend @negative
  Esquema do Cenário: Rejeitar cadastro com e-mail ou telefone inválido
    Dado que acesso "Practice Form" pelo menu "Forms"
    Quando envio dados válidos exceto pelo campo "<campo>" preenchido com "<valor>"
    Então o campo "<campo>" é rejeitado por "<motivo>" e o modal não abre

    Exemplos:
      | campo    | valor         | motivo          |
      | e-mail   | qa.example.com | formato inválido |
      | telefone | 123456789      | comprimento curto |
      | telefone | 12345abcde     | formato inválido |

  @frontend
  Cenário: Aceitar cadastro sem selecionar uma matéria
    Dado que acesso "Practice Form" pelo menu "Forms"
    Quando envio dados válidos deixando Subjects vazio
    Então o modal confirma os dados enviados com Subjects vazio
    E posso fechar o modal de confirmação com Escape
