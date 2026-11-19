from dataclasses import replace

from behave import then, when

from pages.practice_form import PracticeForm, Student

FIELDS = {"e-mail": ("email", "#userEmail"), "telefone": ("mobile", "#userNumber")}
VALIDITY_FLAGS = {"formato inválido": "patternMismatch", "comprimento curto": "tooShort"}


@when("envio o formulário completo com dados aleatórios válidos e um arquivo TXT")
def envio_formulario(context):
    context.form = PracticeForm(context.driver)
    context.student = Student.generate(context.rng)
    context.form.submit_student(context.student)


@then("o modal confirma os dados enviados")
@then("o modal confirma os dados enviados com Subjects vazio")
def verifico_confirmacao(context):
    expected = context.student.confirmation()
    actual = context.form.confirmation()
    assert actual == expected, f"Dados do modal: {actual!r}. Esperado: {expected!r}"


@then("posso fechar o modal de confirmação com Escape")
def fecho_confirmacao(context):
    context.form.close_confirmation()


@when("tento enviar o formulário vazio")
def envio_formulario_vazio(context):
    context.form = PracticeForm(context.driver)
    context.form.submit()


@then("o primeiro nome é identificado como obrigatório e o modal não abre")
def verifico_rejeicao(context):
    context.form.verify_rejection("#firstName", "valueMissing")


@when('envio dados válidos exceto pelo campo "{field}" preenchido com "{value}"')
def envio_dado_invalido(context, field, value):
    context.form = PracticeForm(context.driver)
    student = Student.generate(context.rng)
    attribute, selector = FIELDS[field]
    context.form.submit_student(replace(student, **{attribute: value}))
    actual = context.form.visible(selector).get_property("value")
    assert actual == value, f"Valor digitado em {field}: {actual!r}; esperado: {value!r}."


@then('o campo "{field}" é rejeitado por "{reason}" e o modal não abre')
def verifico_dado_invalido(context, field, reason):
    _, selector = FIELDS[field]
    context.form.verify_rejection(selector, VALIDITY_FLAGS[reason])


@when("envio dados válidos deixando Subjects vazio")
def envio_sem_materia(context):
    context.form = PracticeForm(context.driver)
    context.student = replace(Student.generate(context.rng), subject="")
    context.form.submit_student(context.student)
