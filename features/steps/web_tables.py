from behave import then, when

from pages.web_tables import Record, WebTables


@when("crio um registro")
def crio_registro(context):
    context.tables = WebTables(context.driver)
    context.original_records = context.tables.snapshot()
    context.record = Record.generate(context.rng, "unico")
    context.tables.create(context.record)


@then("a tabela exibe os dados do novo registro")
@then("a tabela exibe os dados atualizados")
def verifico_registro(context):
    context.tables.verify(context.record)


@when("atualizo os dados desse registro")
def atualizo_registro(context):
    updated = context.record.updated()
    context.tables.update(context.record, updated)
    context.record = updated


@when("excluo esse registro")
def excluo_registro(context):
    context.tables.delete(context.record.email)


@then("a tabela volta a exibir somente os registros originais")
def verifico_exclusao(context):
    actual = context.tables.snapshot()
    assert actual == context.original_records, (
        f"Tabela após excluir {context.record.email}: {actual!r}; "
        f"esperado: {context.original_records!r}."
    )


@when("crio um registro distinto para cada item da tabela")
def crio_registros_do_bonus(context):
    context.tables = WebTables(context.driver)
    context.tables.show_all_test_records()
    context.original_records = context.tables.snapshot()
    context.records = [Record.generate(context.rng, row["item"]) for row in context.table]
    emails = {record.email for record in context.records}
    assert len(context.records) == len(emails) == 12
    assert not emails.intersection(context.original_records)
    for record in context.records:
        context.tables.create(record)


@then("encontro todos os registros criados com os dados esperados")
def verifico_registros_do_bonus(context):
    created = {record.email: record.cells() for record in context.records}
    actual = context.tables.snapshot()
    assert actual == context.original_records | created


@when("excluo todos os registros criados")
def excluo_registros_do_bonus(context):
    remaining = {record.email: record.cells() for record in context.records}
    for record in context.records:
        context.tables.delete(record.email)
        del remaining[record.email]
        actual = context.tables.snapshot()
        expected = context.original_records | remaining
        missing = sorted(expected.keys() - actual.keys())
        counts = f"Antes: {len(expected) + 1}; depois: {len(actual)}; esperado: {len(expected)}"
        print(f"Exclusão de {record.email}. {counts}.", flush=True)
        assert actual == expected, (
            f"Após excluir {record.email}, a tabela divergiu do esperado. "
            f"{counts}. "
            f"Registros que também sumiram: {missing}."
        )


@then("nenhum dos registros criados permanece na tabela")
def verifico_exclusoes_do_bonus(context):
    actual = context.tables.snapshot()
    assert not {record.email for record in context.records}.intersection(actual)


@then("os registros originais permanecem na tabela")
def verifico_registros_originais(context):
    assert context.tables.snapshot() == context.original_records
