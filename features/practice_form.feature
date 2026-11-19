# language: pt
Funcionalidade: Cadastro de estudante

  @frontend
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
