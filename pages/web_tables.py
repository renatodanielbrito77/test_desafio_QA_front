from dataclasses import dataclass, replace

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import Select

from pages.base import Page


@dataclass(frozen=True)
class Record:
    first_name: str
    last_name: str
    age: int
    email: str
    salary: int
    department: str

    @classmethod
    def generate(cls, rng, item):
        return cls(
            first_name=rng.choice(("Ana", "Bruno", "Carla", "Diego")),
            last_name=rng.choice(("Costa", "Moura", "Nunes", "Silva")),
            age=rng.randint(21, 65),
            email=f"qa-{rng.randrange(10**9):09d}-{item}@example.com",
            salary=rng.randint(3000, 12000),
            department="Quality",
        )

    def updated(self):
        return replace(self, salary=self.salary + 500, department="Engineering")

    def cells(self):
        return (
            self.first_name, self.last_name, str(self.age), self.email,
            str(self.salary), self.department,
        )


class WebTables(Page):
    SEARCH = "#searchBox"
    ROWS = "table tbody tr"
    FIELD_IDS = ("firstName", "lastName", "age", "userEmail", "salary", "department")

    def create(self, record):
        self.click("#addNewRecordButton")
        self.save(record)

    def update(self, original, updated):
        self.search(original.email)
        self.click_action(original.email, "edit")
        self.save(updated)

    def delete(self, email):
        self.search(email)
        self.click_action(email, "delete")
        self.wait.until(lambda _: not self.find_row(email))

    def save(self, record):
        for field_id, value in zip(self.FIELD_IDS, record.cells(), strict=True):
            self.fill(f"#{field_id}", value)
        self.click("#submit")
        self.wait.until(ec.invisibility_of_element_located((By.CSS_SELECTOR, "#submit")))

    def search(self, email):
        field = self.visible(self.SEARCH)
        # Use keyboard input so React receives the change to an empty search.
        modifier = Keys.COMMAND if self.driver.capabilities["platformName"] == "mac" else Keys.CONTROL
        field.send_keys(modifier, "a", Keys.NULL, Keys.BACKSPACE)
        if email:
            field.send_keys(email)
        self.wait.until(
            lambda _: self.visible(self.SEARCH).get_property("value") == email,
            message=f"A busca não refletiu o valor {email!r}.",
        )

    def row_locator(self, email):
        return f"//table/tbody/tr[td[normalize-space(.)='{email}']]"

    def find_row(self, email):
        return self.driver.find_elements(By.XPATH, self.row_locator(email))

    def click_action(self, email, action):
        self.click(f"{self.row_locator(email)}//*[@id and starts-with(@id, '{action}-record-')]", By.XPATH)

    def row_data(self, row):
        return tuple(cell.text for cell in row.find_elements(By.TAG_NAME, "td")[:6])

    def snapshot(self):
        self.search("")
        rows = [self.row_data(row) for row in self.driver.find_elements(By.CSS_SELECTOR, self.ROWS)]
        records = {}
        for data in rows:
            if len(data) != 6 or not data[3]:
                continue
            email = data[3]
            assert email not in records, f"E-mail duplicado na tabela: {email}"
            records[email] = data
        return records

    def show_all_test_records(self):
        Select(self.visible("select")).select_by_visible_text("Show 20")

    def verify(self, record):
        self.search(record.email)
        row = self.visible(self.row_locator(record.email), By.XPATH)
        actual = self.row_data(row)
        assert actual == record.cells(), f"Linha para {record.email}: {actual!r}; esperado {record.cells()!r}"
