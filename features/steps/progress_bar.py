from behave import then, when

from pages.progress_bar import ProgressBar


@when("inicio a barra e interrompo seu avanço antes de 25%")
def inicio_e_paro(context):
    context.progress = ProgressBar(context.driver)
    context.progress.start()
    context.progress_before_click = context.progress.stop_before(25)


@then("a barra fica parada com valor abaixo de 25%")
def verifico_pausa(context):
    context.progress.verify_stopped(25, context.progress_before_click)


@when("retomo o avanço da barra")
def retomo_barra(context):
    context.progress.start()


@then("a barra chega a 100%")
def verifico_progresso_completo(context):
    context.progress.wait_until_complete()


@then("posso resetar a barra para 0%")
def reseto_barra(context):
    context.progress.reset()
