from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec

from pages.base import Page


class BrowserWindows(Page):
    NEW_WINDOW = "//button[normalize-space(.)='New Window']"

    def open_window(self):
        original = self.driver.current_window_handle
        previous = set(self.driver.window_handles)
        self.click(self.NEW_WINDOW, By.XPATH)
        self.wait.until(ec.new_window_is_opened(list(previous)))
        opened = set(self.driver.window_handles) - previous
        assert len(opened) == 1, f"Esperava uma nova janela, encontrei {len(opened)}"
        new_window = opened.pop()
        self.driver.switch_to.window(new_window)
        return original, new_window

    def message(self):
        return self.visible("h1").text

    def close_window(self, original, new_window):
        assert self.driver.current_window_handle == new_window
        self.driver.close()
        self.wait.until(lambda driver: new_window not in driver.window_handles)
        assert original in self.driver.window_handles
        self.driver.switch_to.window(original)
