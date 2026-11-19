from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait


class Page:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)

    def visible(self, selector, by=By.CSS_SELECTOR):
        return self.wait.until(
            ec.visibility_of_element_located((by, selector)),
            message=f"Elemento não ficou visível: {selector}",
        )

    def click(self, selector, by=By.CSS_SELECTOR):
        element = self.wait.until(
            ec.element_to_be_clickable((by, selector)),
            message=f"Elemento não ficou disponível para clique: {selector}",
        )
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center', inline: 'nearest'})",
            element,
        )
        element.click()

    def fill(self, selector, value):
        field = self.visible(selector)
        field.clear()
        field.send_keys(str(value))

    def heading(self, text):
        return self.visible(
            f"//*[self::h1 or self::h2 or self::div[@class='main-header']][normalize-space(.)='{text}']",
            By.XPATH,
        )


class DemoQA(Page):
    def open_from_home(self, base_url, menu, submenu):
        self.driver.get(base_url)
        self.click(
            f"//*[self::h2 or self::h5][normalize-space(.)='{menu}']",
            By.XPATH,
        )
        self.click(
            f"//*[self::a or self::span][normalize-space(.)='{submenu}']",
            By.XPATH,
        )
        self.heading(submenu)
