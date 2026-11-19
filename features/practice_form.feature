# language: pt
Funcionalidade: Cadastro de estudante

  @frontend
  Cenário: Enviar todos os dados de um estudante com um anexo
    Dado que acesso "Practice Form" pelo menu "Forms"
    Quando envio o formulário completo com dados aleatórios válidos e um arquivo TXT
    Então o modal confirma os dados enviados
    E posso fechar o modal de confirmação com Escape
