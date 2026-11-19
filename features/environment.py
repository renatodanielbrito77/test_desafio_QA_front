import os
import random
import secrets
from pathlib import Path

from behave.model_core import Status
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService


def before_all(context):
    config = context.config.userdata
    context.base_url = config.get("base_url", "https://demoqa.com").rstrip("/")
    context.browser = config.get("browser", "chrome").lower()
    if context.browser not in {"chrome", "firefox"}:
        raise ValueError("Use -D browser=chrome ou -D browser=firefox.")
    context.suite_seed = int(config.get("seed", secrets.randbits(32)))
    print(f"Semente da suíte: {context.suite_seed}", flush=True)


def before_scenario(context, scenario):
    context.rng = random.Random(f"{context.suite_seed}:{scenario.name}")
    headed = context.config.userdata.getbool("headed", default=False)
    if context.browser == "firefox":
        browser = webdriver.Firefox
        options = webdriver.FirefoxOptions()
        service = FirefoxService(executable_path=os.environ.get("GECKODRIVER"))
        if not headed:
            options.add_argument("-headless")
    else:
        browser = webdriver.Chrome
        options = webdriver.ChromeOptions()
        service = ChromeService(executable_path=os.environ.get("CHROMEDRIVER"))
        if not headed:
            options.add_argument("--headless")
    options.page_load_strategy = "eager"
    context.driver = browser(options=options, service=service)
    context.add_cleanup(context.driver.quit)
    context.driver.set_window_size(1440, 1000)
    context.driver.set_page_load_timeout(30)


def after_scenario(context, scenario):
    if scenario.status not in (Status.failed, Status.error, Status.hook_error):
        return
    driver = getattr(context, "driver", None)
    if driver is None:
        return
    path = Path("artifacts") / context.browser / f"{Path(scenario.filename).stem}-{scenario.line}.png"
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        if driver.save_screenshot(str(path)):
            print(f"Captura da falha: {path}")
    except Exception as error:
        print(f"Falha ao capturar a tela: {error}")
