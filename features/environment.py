import os
import random
import secrets
from pathlib import Path

from behave.model_core import Status
from selenium import webdriver
from selenium.webdriver.chrome.service import Service


def before_all(context):
    config = context.config.userdata
    context.base_url = config.get("base_url", "https://demoqa.com").rstrip("/")
    context.suite_seed = int(config.get("seed", secrets.randbits(32)))
    print(f"Semente da suíte: {context.suite_seed}", flush=True)


def before_scenario(context, scenario):
    context.rng = random.Random(f"{context.suite_seed}:{scenario.name}")
    options = webdriver.ChromeOptions()
    if not context.config.userdata.getbool("headed", default=False):
        options.add_argument("--headless")
    options.add_argument("--window-size=1440,1000")
    options.page_load_strategy = "eager"
    driver_path = os.environ.get("CHROMEDRIVER")
    service = Service(executable_path=driver_path)
    context.driver = webdriver.Chrome(options=options, service=service)
    context.add_cleanup(context.driver.quit)
    context.driver.set_page_load_timeout(30)


def after_scenario(context, scenario):
    if scenario.status not in (Status.failed, Status.error, Status.hook_error):
        return
    driver = getattr(context, "driver", None)
    if driver is None:
        return
    path = Path("artifacts") / f"{Path(scenario.filename).stem}-{scenario.line}.png"
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        if driver.save_screenshot(str(path)):
            print(f"Captura da falha: {path}")
    except Exception as error:
        print(f"Falha ao capturar a tela: {error}")
