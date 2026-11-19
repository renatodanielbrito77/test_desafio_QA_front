# language: pt
Funcionalidade: Controle da barra de progresso

  @frontend
  Cenário: Parar a barra, concluir o progresso e resetar
    Dado que acesso "Progress Bar" pelo menu "Widgets"
    Quando inicio a barra e interrompo seu avanço antes de 25%
    Então a barra fica parada com valor abaixo de 25%
    Quando retomo o avanço da barra
    Então a barra chega a 100%
    E posso resetar a barra para 0%
