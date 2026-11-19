from dataclasses import dataclass
from datetime import date
from pathlib import Path

from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import Select

from pages.base import Page


@dataclass(frozen=True)
class Student:
    first_name: str
    last_name: str
    email: str
    gender: str
    mobile: str
    birth_date: date
    subject: str
    hobby: str
    address: str
    state: str
    city: str
    attachment: Path

    @classmethod
    def generate(cls, rng):
        first_name = rng.choice(("Ana", "Bruno", "Carla", "Diego"))
        last_name = rng.choice(("Costa", "Lima", "Reis", "Souza"))
        state, city = rng.choice((("NCR", "Delhi"), ("Haryana", "Karnal")))
        attachment = Path(__file__).resolve().parents[1] / "fixtures" / "anexo-demoqa.txt"
        return cls(
            first_name=first_name,
            last_name=last_name,
            email=f"{first_name.lower()}.{last_name.lower()}.{rng.randrange(10000)}@example.com",
            gender=rng.choice(("Male", "Female", "Other")),
            mobile=str(rng.randint(1_000_000_000, 9_999_999_999)),
            birth_date=date(rng.randint(1985, 2005), rng.randint(1, 12), rng.randint(1, 28)),
            subject=rng.choice(("Maths", "English", "Physics")),
            hobby=rng.choice(("Sports", "Reading", "Music")),
            address=f"{rng.randint(1, 999)} Rua de Teste",
            state=state,
            city=city,
            attachment=attachment,
        )

    def confirmation(self):
        return {
            "Student Name": f"{self.first_name} {self.last_name}",
            "Student Email": self.email,
            "Gender": self.gender,
            "Mobile": self.mobile,
            "Date of Birth": self.birth_date.strftime("%d %B,%Y"),
            "Subjects": self.subject,
            "Hobbies": self.hobby,
            "Picture": self.attachment.name,
            "Address": self.address,
            "State and City": f"{self.state} {self.city}",
        }


class PracticeForm(Page):
    BIRTH_DATE = "#dateOfBirthInput"
    MODAL_TITLE = "#example-modal-sizes-title-lg"
    MODAL_ROWS = ".modal tbody tr"

    def submit_student(self, student):
        self.fill("#firstName", student.first_name)
        self.fill("#lastName", student.last_name)
        self.fill("#userEmail", student.email)
        self.click_label(student.gender)
        self.fill("#userNumber", student.mobile)
        self.select_option("#subjectsInput", student.subject)
        self.click_label(student.hobby)
        self.visible("#uploadPicture").send_keys(str(student.attachment))
        self.fill("#currentAddress", student.address)
        self.select_option("#state input[role='combobox']", student.state)
        self.select_option("#city input[role='combobox']", student.city)
        self.select_birth_date(student.birth_date)
        self.click("#submit")

    def click_label(self, text):
        self.click(f"//label[normalize-space(.)='{text}']", By.XPATH)

    def select_birth_date(self, birth_date):
        self.click(self.BIRTH_DATE)
        Select(self.visible(".react-datepicker__year-select")).select_by_value(str(birth_date.year))
        Select(self.visible(".react-datepicker__month-select")).select_by_value(str(birth_date.month - 1))
        day = f"{birth_date.day:03d}"
        self.click(f".react-datepicker__day--{day}:not(.react-datepicker__day--outside-month)")
        self.wait.until(ec.invisibility_of_element_located((By.CSS_SELECTOR, ".react-datepicker")))
        self.verify_birth_date_input(birth_date)

    def verify_birth_date_input(self, birth_date):
        expected = birth_date.strftime("%d %b %Y")
        self.wait.until(
            lambda _: self.visible(self.BIRTH_DATE).get_property("value") == expected,
            message=f"O campo de data não manteve o valor selecionado: {expected}",
        )

    def select_option(self, selector, text):
        self.click(selector)
        self.visible(selector).send_keys(text)
        self.click(f"//*[@role='option' and normalize-space(.)='{text}']", By.XPATH)

    def confirmation(self):
        assert self.visible(self.MODAL_TITLE).text == "Thanks for submitting the form"
        data = {}
        for row in self.driver.find_elements(By.CSS_SELECTOR, self.MODAL_ROWS):
            label, value = row.find_elements(By.TAG_NAME, "td")
            data[label.text] = value.text
        return data

    def close_confirmation(self):
        ActionChains(self.driver).send_keys(Keys.ESCAPE).perform()
        self.wait.until(ec.invisibility_of_element_located((By.CSS_SELECTOR, self.MODAL_TITLE)))
