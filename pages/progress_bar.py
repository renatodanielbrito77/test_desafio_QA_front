from time import monotonic

from selenium.webdriver.support.ui import WebDriverWait

from pages.base import Page


class ProgressBar(Page):
    BAR = '[role="progressbar"]'
    TOGGLE = "#startStopButton"
    RESET = "#resetButton"

    def value(self):
        return int(self.visible(self.BAR).get_dom_attribute("aria-valuenow"))

    def start(self):
        assert self.visible(self.TOGGLE).text == "Start"
        self.click(self.TOGGLE)

    def stop_before(self, limit):
        # Leave time for the click to reach the browser before the limit.
        WebDriverWait(self.driver, 5, poll_frequency=0.05).until(
            lambda _: self.value() >= limit // 2
        )
        before_click = self.value()
        assert before_click < limit, f"A barra já chegou a {before_click}% antes do clique."
        self.click(self.TOGGLE)

    def verify_stopped(self, limit):
        assert self.visible(self.TOGGLE).text == "Start"
        stopped_at = self.value()
        assert 0 < stopped_at <= limit, f"A barra parou em {stopped_at}%."
        started_checking = monotonic()

        def remains_stopped(_):
            current = self.value()
            assert current == stopped_at, f"A barra mudou de {stopped_at}% para {current}%."
            return monotonic() - started_checking >= 0.4

        WebDriverWait(self.driver, 2, poll_frequency=0.1).until(remains_stopped)

    def wait_until_complete(self):
        self.wait.until(lambda _: self.value() == 100)

    def reset(self):
        self.click(self.RESET)
        self.wait.until(lambda _: self.value() == 0)
        assert self.visible(self.TOGGLE).text == "Start"
