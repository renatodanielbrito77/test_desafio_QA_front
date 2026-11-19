from behave import then, when

from pages.browser_windows import BrowserWindows


@when("abro uma nova janela")
def abro_janela(context):
    context.windows = BrowserWindows(context.driver)
    context.original_window, context.new_window = context.windows.open_window()


@then('a nova janela exibe "{text}"')
def verifico_texto(context, text):
    assert context.windows.message() == text


@then('posso fechá-la e voltar à página "{heading}"')
def fecho_janela(context, heading):
    context.windows.close_window(context.original_window, context.new_window)
    context.windows.heading(heading)
