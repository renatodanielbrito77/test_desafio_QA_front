from time import monotonic

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait

from pages.base import Page


class ProgressBar(Page):
    BAR = '[role="progressbar"]'
    TOGGLE = "#startStopButton"
    RESET = "#resetButton"

    def value(self):
        return int(self.visible(self.BAR).get_dom_attribute("aria-valuenow"))

    def start(self):
        button = self.visible(self.TOGGLE)
        assert button.text == "Start"
        button.send_keys(Keys.ENTER)

    def stop_before(self, limit):
        # Leave time for the click to reach the browser before the limit.
        WebDriverWait(self.driver, 5, poll_frequency=0.05).until(
            lambda _: self.value() >= limit // 2
        )
        before_click = self.value()
        assert before_click < limit, f"A barra já chegou a {before_click}% antes do clique."
        self.visible(self.TOGGLE).send_keys(Keys.ENTER)
        return before_click

    def verify_stopped(self, limit, before_click):
        assert self.visible(self.TOGGLE).text == "Start"
        stopped_at = self.value()
        assert 0 < stopped_at < limit, (
            f"Antes do clique: {before_click}%. Após parar: {stopped_at}%. "
            f"Esperado: entre 1% e {limit - 1}%."
        )
        started_checking = monotonic()

        def remains_stopped(_):
            current = self.value()
            assert current == stopped_at, (
                f"Antes do clique: {before_click}%. "
                f"Após parar, a barra mudou de {stopped_at}% para {current}%."
            )
            return monotonic() - started_checking >= 0.4

        WebDriverWait(self.driver, 2, poll_frequency=0.1).until(remains_stopped)

    def wait_until_complete(self):
        self.wait.until(lambda _: self.value() == 100)

    def reset(self):
        self.visible(self.RESET).send_keys(Keys.ENTER)
        self.wait.until(lambda _: self.value() == 0)
        assert self.visible(self.TOGGLE).text == "Start"
