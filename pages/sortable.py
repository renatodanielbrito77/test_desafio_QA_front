from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By

from pages.base import Page


class Sortable(Page):
    ITEMS = "#demo-tabpane-list .list-group-item"

    def items(self):
        self.visible(self.ITEMS)
        return self.driver.find_elements(By.CSS_SELECTOR, self.ITEMS)

    def order(self):
        return [item.text for item in self.items()]

    def sort_ascending(self, target_order):
        self.click("#demo-tab-list")
        assert sorted(self.order()) == sorted(target_order)

        # Move each item to the top, starting with the last item in the desired order.
        # This exercises drag and drop even when the initial list comes pre-sorted.
        for text in reversed(target_order):
            items = self.items()
            top = items[0]
            if top.text == text:
                continue
            source = next(item for item in items if item.text == text)
            drop_offset = -max(1, int(top.rect["height"] / 4))
            (
                ActionChains(self.driver, duration=200)
                .move_to_element(source)
                .click_and_hold()
                .move_by_offset(0, -8)
                .move_to_element_with_offset(top, 0, drop_offset)
                .release()
                .perform()
            )
            self.wait.until(lambda _: self.items()[0].text == text)
