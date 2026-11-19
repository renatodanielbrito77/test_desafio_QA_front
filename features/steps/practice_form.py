from behave import then, when

from pages.practice_form import PracticeForm, Student


@when("envio o formulário completo com dados aleatórios válidos e um arquivo TXT")
def envio_formulario(context):
    context.form = PracticeForm(context.driver)
    context.student = Student.generate(context.rng)
    context.form.submit_student(context.student)


@then("o modal confirma os dados enviados")
def verifico_confirmacao(context):
    expected = context.student.confirmation()
    actual = context.form.confirmation()
    assert actual == expected, f"Dados do modal: {actual!r}. Esperado: {expected!r}"


@then("posso fechar o modal de confirmação com Escape")
def fecho_confirmacao(context):
    context.form.close_confirmation()
