# language: pt
Funcionalidade: Ordenação de itens

  @frontend @original @sortable
  Cenário: Ordenar a lista por arrastar e soltar
    Dado que acesso "Sortable" pelo menu "Interactions"
    Quando ordeno os itens da lista por arrastar e soltar
    Então vejo a lista na ordem "One, Two, Three, Four, Five, Six"
