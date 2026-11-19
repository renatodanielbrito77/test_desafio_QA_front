# language: pt
Funcionalidade: Janelas do navegador

  @frontend
  Cenário: Abrir e fechar uma janela de exemplo
    Dado que acesso "Browser Windows" pelo menu "Alerts, Frame & Windows"
    Quando abro uma nova janela
    Então a nova janela exibe "This is a sample page"
    E posso fechá-la e voltar à página "Browser Windows"
