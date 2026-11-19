from behave import then, when

from pages.sortable import Sortable


ASCENDING = ("One", "Two", "Three", "Four", "Five", "Six")


@when("ordeno os itens da lista por arrastar e soltar")
def ordeno_lista(context):
    context.sortable = Sortable(context.driver)
    context.sortable.sort_ascending(ASCENDING)


@then('vejo a lista na ordem "{order}"')
def verifico_ordem(context, order):
    expected = order.split(", ")
    actual = context.sortable.order()
    assert actual == expected, f"Ordem exibida: {actual!r}; esperada: {expected!r}"
