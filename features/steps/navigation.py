from behave import given

from pages.base import DemoQA


@given('que acesso "{submenu}" pelo menu "{menu}"')
def acesso_pelo_menu(context, submenu, menu):
    DemoQA(context.driver).open_from_home(context.base_url, menu, submenu)
